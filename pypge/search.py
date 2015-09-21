import model
import expand
import memoize
import evaluate

import numpy
import sympy
import lmfit
import selection as emo
from deap import base, creator

import networkx as nx
import multiprocessing as mp

numpy.random.seed(23)
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))



def unwrap_self_peek_model_queue(this):
	while True:
		try:
			val = this.peek_in_queue.get()
			if val is None:
				break;
			pos = val[0]
			modl = val[1]

			passed = PGE.peek_model(this, modl)
			if not passed:
				this.peek_out_queue.send( (pos, modl.error, modl.exception) )
			else:
				vals = [ (str(c),modl.params[str(c)].value) for c in modl.cs ]
				ret_data = {
					'score': modl.score,
					'r2': modl.r2,
					'evar': modl.evar,
					'params': vals,
					'nfev': modl.fit_result.nfev
				}
				this.peek_out_queue.put( (pos, None, ret_data) )
		except Exception, e:
			print "breaking!", e
			break

def unwrap_self_eval_model_queue(this):
	while True:
		try:
			val = this.eval_in_queue.get()
			if val is None:
				break;
			pos = val[0]
			modl = val[1]

			passed = PGE.eval_model(this, modl)
			if not passed:
				this.eval_out_queue.send( (pos, modl.error, modl.exception) )
			else:
				vals = [ (str(c),modl.params[str(c)].value) for c in modl.cs ]
				ret_data = {
					'score': modl.score,
					'r2': modl.r2,
					'evar': modl.evar,
					'params': vals,
					'nfev': modl.fit_result.nfev
				}
				this.eval_out_queue.put( (pos, None, ret_data) )
		except Exception, e:
			print "breaking!", e
			break


class PGE:
	
	def __init__(self,**kwargs):
		# default values
		self.workers = 1
		self.max_iter = 100
		self.pop_count = 3
		self.peek_count = 2*self.pop_count
		self.peek_npts = 16

		self.min_size = 1
		self.max_size = 64
		self.min_depth = 1
		self.max_depth = 6

		self.max_power = 5

		self.zero_epsilon = 1e-6  ## still need to use
		self.err_method = "mse"

		self.system_type = None
		self.search_vars = None
		self.usable_vars = None
		self.usable_funcs = None

		# number of function evaluations 
		self.peek_nfev = 0 # mul by peek_npts
		self.eval_nfev = 0

		# override with kwargs
		for key, value in kwargs.items():
			# print key, value
			setattr(self, key, value)

		self.vars = sympy.symbols(self.usable_vars)
		if type(self.vars) is sympy.Symbol:
			self.vars = [self.vars]

		if not self.check_config():
			print "ERROR: config missing values"
			return

		# evaluation pools
		self.peek_in_queue = mp.Queue(256)
		self.peek_out_queue = mp.Queue(256)
		self.peek_procs = [mp.Process(target=unwrap_self_peek_model_queue, args=(self,) ) for i in range(self.workers)]

		self.eval_in_queue = mp.Queue(256)
		self.eval_out_queue = mp.Queue(256)
		self.eval_procs = [mp.Process(target=unwrap_self_eval_model_queue, args=(self,) ) for i in range(self.workers)]

		# memoizer & grower
		self.memoizer = memoize.Memoizer(self.vars)
		self.grower = expand.Grower(self.vars, self.usable_funcs)

		# Pareto Front stuff
		self.nsga2_peek = []
		self.spea2_peek = []
		self.nsga2_list = []
		self.spea2_list = []

		# list of all finalized models
		self.final = []

		# Root node for the graph
		r = sympy.Symbol("root")
		self.root_model = model.Model(r)
		R = self.root_model
		R.id = -1
		R.score = 9999999999999.
		R.r2 = -100.
		R.evar = -100.

		# Relationship Graph
		self.iter_expands = []
		self.iter_expands.append([R])
		self.graph = nx.MultiDiGraph()
		self.graph.add_node(R, modl=R)

		print self


	# sklearn estimator interface functions
	def fit(self, X_train,Y_train):

		self.set_data(X_train,Y_train) # *** see note below
		self.preloop()
		self.loop(self.max_iter)
		self.finalize()

		### Sklearn doesn't want us to store this data
		### But we want to for checkpointing and continuation
		### This may require a finalization function
		###   as we are finalizing at the end of loop right now
		###   either way, we want sklean interface, with curr finalization
		###   while still checkpointing, just need more storage and temps


	def check_config(self):
		if self.system_type == None \
		or self.search_vars == None \
		or self.usable_vars == None:
			return False
		return True

	def set_data(self, X_train, Y_train):
		# set training data 
		self.X_train = X_train
		self.Y_train = Y_train
		self.eval_npts = len(self.Y_train)

		# set peeking data
		pos = numpy.random.randint(0,self.eval_npts, self.peek_npts)
		self.X_peek = self.X_train[:,pos]
		self.Y_peek = self.Y_train[pos]

		print "train.shape:", self.X_train.shape, self.Y_train.shape
		print "peekn.shape:", self.X_peek.shape, self.Y_peek.shape
		print "\n\n"

	def preloop(self):
		# preloop setup (generates,evals,queues first models)
		print "Preloop setup"

		for proc in self.peek_procs:
			proc.start()
		for proc in self.eval_procs:
			proc.start()


		self.first_exprs = self.grower.first_exprs()
		self.iter_expands.append(self.first_exprs)

		to_peek = self.memoize_models(self.first_exprs)

		if self.workers > 1:
			self.peek_models_multiprocess(to_peek, self.workers)
		else:
			self.peek_models(to_peek)

		self.peek_push_models(to_peek)
		to_eval = self.peek_pop() + self.peek_pop() # twice the first time

		if self.workers > 1:
			self.eval_models_multiprocess(to_eval, self.workers)
		else:
			self.eval_models(to_eval)

		self.eval_push_models(to_eval)


	def loop(self, iterations):
		# main loop for # iterations
		for I in range(iterations):
			print "\n\nITER: ", I

			popd = self.eval_pop()

			expanded = self.expand_models(popd)
			self.iter_expands.append(expanded)

			to_peek = self.memoize_models(expanded)

			if self.workers > 1:
				self.peek_models_multiprocess(to_peek, self.workers)
			else:
				self.peek_models(to_peek)

			self.peek_push_models(to_peek)
			to_eval = self.peek_pop()
				
			if self.workers > 1:
				self.eval_models_multiprocess(to_eval, self.workers)
			else:
				self.eval_models(to_eval)

			self.eval_push_models(to_eval)
			self.print_best(24)


	def print_best(self, count):
		best = emo.sortLogNondominated(self.final, count)
		print "Best so far"
		print "      id:  sz           error         r2    expld_vari    theModel"
		print "-----------------------------------------------------------------------------------"
		cnt = 0
		for front in best:
			for m in front:
				if cnt >= count:
					return
				cnt += 1
				print "  ", m
			print ""



	def finalize(self, nfronts=4):
		# finalization
		print "\n\nFinalizing\n\n"

		# pull all non-expanded models in queue out and push into final
		# could also use spea2_list here, they should have same contents
		final = self.final + self.nsga2_list 

		# generate final pareto fronts
		final_list = emo.sortLogNondominated(final, len(final))

		# print first 4 pareto fronts
		print "Final Results"
		print "      id:  sz           error         r2    expld_vari    theModel"
		print "-----------------------------------------------------------------------------------"
		for front in final_list[:nfronts]:
			for m in front:
				print "  ", m
			print ""

		print "\n"
		print "num peek evals:  ", self.peek_nfev, self.peek_nfev * self.peek_npts
		print "num eval evals:  ", self.eval_nfev, self.eval_nfev * self.eval_npts
		print "num total evals: ", self.peek_nfev * self.peek_npts + self.eval_nfev * self.eval_npts
		
		print "\n\n", nx.info(self.graph), "\n\n"

		# handle issue with extra stray node with parent_id == -2 (at end of nodes list)
		del_n = []
		for n in nx.nodes_iter(self.graph):
			if n.score is None:
				del_n.append(n)
		for n in del_n:
			self.graph.remove_node(n)

		print "\n\nstopping workers"

		for proc in self.peek_procs:
			self.peek_in_queue.put(None)
		for proc in self.eval_procs:
			self.eval_in_queue.put(None)

		for proc in self.peek_procs:
			proc.join()
		for proc in self.eval_procs:
			proc.join()

		print "\n\ndone\n\n"
					


	def memoize_models(self, models):
		print "  memoizing:", len(models)
		unique = []
		for m in models:
			found, f_modl = self.memoizer.lookup(m)
			if found:
				p = self.memoizer.get_by_id(m.parent_id)
				self.graph.add_edge(p, m, relation="ex_dupd")
				continue

			if self.memoizer.insert(m):
				m.memoized = True
				m.rewrite_coeff()
				unique.append(m)
				# add node and edge
				p = self.memoizer.get_by_id(m.parent_id)
				self.graph.add_node(m, modl=m)
				self.graph.add_edge(p, m, relation="expanded")

		print "  unique:", len(unique)
		return unique

	def expand_models(self, models):
		print "  expanding'n:", len(models)
		expanded = []
		for p in models:
			p.popped = True

			modls = self.grower.grow(p)
			p.expanded = True

			# any filters here?
			expanded.extend(modls)
			# any filters here?
			
			self.final.append(p)
			p.finalized = True

		print "  expanded to:", len(expanded) 
		return expanded

	def peek_push_models(self, models):
		print "  peek_queue'n:", len(models)
		for m in models:
			self.peek_push(m)

	def peek_push(self, modl):
		self.nsga2_peek.append(modl)
		self.spea2_peek.append(modl)
		modl.peek_queued = True

	def eval_push_models(self, models):
		print "  eval_queue'n:", len(models)
		for m in models:
			self.eval_push(m)

	def eval_push(self, modl):
		self.nsga2_list.append(modl)
		self.spea2_list.append(modl)
		modl.queued = True

	def peek_pop(self):
		nsga2_tmp = emo.selNSGA2(self.nsga2_peek, len(self.nsga2_peek))
		spea2_tmp = emo.selSPEA2(self.spea2_peek, len(self.spea2_peek))

		nsga2_popd, self.nsga2_peek = nsga2_tmp[:self.peek_count], nsga2_tmp[self.peek_count:]
		spea2_popd, self.spea2_peek = spea2_tmp[:self.peek_count], spea2_tmp[self.peek_count:]

		popd_set = set()
		for p in nsga2_popd:
			popd_set.add(p)
		for p in spea2_popd:
			popd_set.add(p)

		popd_list = list(popd_set)
		# print "  uniqued peek'd pop'd:"
		for p in popd_list:
			p.peek_popped = True
			# print "    ", p

		self.nsga2_peek = [m for m in self.nsga2_peek if not m.peek_popped]
		self.spea2_peek = [m for m in self.spea2_peek if not m.peek_popped]

		print "  peek_pop'd", len(popd_list)
		return popd_list

	def eval_pop(self):
		nsga2_tmp = emo.selNSGA2(self.nsga2_list, len(self.nsga2_list))
		spea2_tmp = emo.selSPEA2(self.spea2_list, len(self.spea2_list))

		nsga2_popd, self.nsga2_list = nsga2_tmp[:self.pop_count], nsga2_tmp[self.pop_count:]
		spea2_popd, self.spea2_list = spea2_tmp[:self.pop_count], spea2_tmp[self.pop_count:]

		popd_set = set()
		for p in nsga2_popd:
			popd_set.add(p)
		for p in spea2_popd:
			popd_set.add(p)

		popd_list = list(popd_set)
		# print "  uniqued eval'd pop'd:"
		for p in popd_list:
			p.popped = True
			# print "    ", p

		self.nsga2_list = [m for m in self.nsga2_list if not m.popped]
		self.spea2_list = [m for m in self.spea2_list if not m.popped]

		print "  eval_pop'd", len(popd_list)
		return popd_list


	def peek_models(self, models):
		print "  peek'n:", len(models)
		for m in models:
			passed = self.peek_model(m)
			if not passed or m.error is not None:
				print m.error, m.exception
				continue
			m.peek_nfev = m.fit_result.nfev
			self.peek_nfev += m.peek_nfev

	def peek_models_multiprocess(self, models, processes):
		print "  multi-peek'n:", len(models)

		for i,m in enumerate(models):
			self.peek_in_queue.put( (i,m) )
		
		for i in range(len(models)):
			ret = self.peek_out_queue.get()
			pos = ret[0]
			err = ret[1]
			dat = ret[2]
			modl = models[ret[0]]

			if err is not None:
				modl.error = err
				modl.exception = dat
				modl.errored = True
			else:
				modl.score = dat['score']
				modl.r2 = dat['r2']
				modl.evar = dat['evar']
				modl.peek_nfev = dat['nfev']
				self.peek_nfev += m.peek_nfev

				for v in dat['params']:
					modl.params[v[0]].value = v[1]

				modl.peek_score = dat['score']
				modl.peek_r2 = dat['r2']
				modl.peek_evar = dat['evar']
				
				# build the fitness for selection
				vals = (modl.size(), modl.score)
				modl.fitness = creator.FitnessMin()
				modl.fitness.setValues( vals )
				modl.evaluated = True


	def peek_model(self, modl):
		# fit the modl
		evaluate.Fit(modl, self.vars, self.X_peek, self.Y_peek)
		if modl.error or not modl.fit_result.success:
			modl.error = "errored while fitting"
			modl.errored = True
			return False
		
		# score the modl
		y_pred = evaluate.Eval(modl, self.vars, self.X_peek)

		modl.score, err = evaluate.Score(self.Y_peek, y_pred, self.err_method)
		if err is not None:
			modl.error = "errored while scoring"
			modl.errored = True
			return False
		
		modl.r2, err = evaluate.Score(self.Y_peek, y_pred, "r2")
		if err is not None:
			modl.error = "errored while r2'n"
			modl.errored = True
			return False
		
		modl.evar, err = evaluate.Score(self.Y_peek, y_pred, "evar")
		if err is not None:
			modl.error = "errored while evar'n"
			modl.errored = True
			return False
		
		# copy values over for now, want to keep printing without changing code, but not forget these values either
		modl.peek_score = modl.score
		modl.peek_r2 = modl.r2
		modl.peek_evar = modl.evar
		
		# build the fitness for selection
		vals = (modl.size(), modl.score)
		modl.fitness = creator.FitnessMin()
		modl.fitness.setValues( vals )
		modl.peeked = True

		return True # passed

	def eval_models(self, models):
		print "  eval'n:", len(models)

		for m in models:
			passed = self.eval_model(m)
			if not passed or m.error is not None:
				print m.error, m.exception
				continue
			m.eval_nfev = m.fit_result.nfev
			self.eval_nfev += m.eval_nfev

	def eval_models_multiprocess(self, models, processes):
		print "  multi-eval'n:", len(models)

		for i,m in enumerate(models):
			self.eval_in_queue.put( (i,m) )
		
		for i in range(len(models)):
			ret = self.eval_out_queue.get()
			pos = ret[0]
			err = ret[1]
			dat = ret[2]
			modl = models[ret[0]]

			if err is not None:
				modl.error = err
				modl.exception = dat
				modl.errored = True
			else:
				modl.score = dat['score']
				modl.r2 = dat['r2']
				modl.evar = dat['evar']
				modl.eval_nfev = dat['nfev']
				self.eval_nfev += m.eval_nfev
				
				for v in dat['params']:
					modl.params[v[0]].value = v[1]

				# build the fitness for selection
				vals = (modl.size(), modl.score)
				modl.fitness = creator.FitnessMin()
				modl.fitness.setValues( vals )
				modl.evaluated = True


	def eval_model(self, modl):
		# fit the modl
		evaluate.Fit(modl, self.vars, self.X_train, self.Y_train)
		if modl.error or not modl.fit_result.success:
			modl.error = "errored while fitting"
			modl.errored = True
			return False
		
		# score the modl
		y_pred = evaluate.Eval(modl, self.vars, self.X_train)

		modl.score, err = evaluate.Score(self.Y_train, y_pred, self.err_method)
		if err is not None:
			modl.error = "errored while scoring"
			modl.errored = True
			return False
		
		modl.r2, err = evaluate.Score(self.Y_train, y_pred, "r2")
		if err is not None:
			modl.error = "errored while r2'n"
			modl.errored = True
			return False
		
		modl.evar, err = evaluate.Score(self.Y_train, y_pred, "evar")
		if err is not None:
			modl.error = "errored while evar'n"
			modl.errored = True
			return False
				
		# build the fitness for selection
		vals = (modl.size(), modl.score)
		modl.fitness = creator.FitnessMin()
		modl.fitness.setValues( vals )
		modl.evaluated = True

		return True # passed




