import model
import expand
import filters
import algebra
import memoize
import evaluate
import selection

import numpy
import sympy
import lmfit
from deap import base, creator
import networkx as nx

import multiprocessing as mp
import parallel

numpy.random.seed(23)
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))

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

		# memoizer & grower
		self.memoizer = memoize.Memoizer(self.vars)
		self.grower = expand.Grower(self.vars, self.usable_funcs)
		self.algebra_methods = ["expand", "factor"]

		# Pareto Front stuff
		self.nsga2_peek = []
		self.spea2_peek = []
		self.nsga2_list = []
		self.spea2_list = []

		# list of all finalized models
		self.final = []
		self.final_paretos = None

		# Root node for the GRAPH
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
		self.GRAPH = nx.MultiDiGraph()
		self.GRAPH.add_node(R.id, modl=R)

		# multiprocessing stuff
		if self.workers > 1:
			self.peek_in_queue = mp.Queue(1024)
			self.peek_out_queue = mp.Queue(1024)
			self.peek_procs = [mp.Process(target=parallel.unwrap_self_peek_model_queue, args=(self,) ) for i in range(self.workers)]

			self.eval_in_queue = mp.Queue(1024)
			self.eval_out_queue = mp.Queue(1024)
			self.eval_procs = [mp.Process(target=parallel.unwrap_self_eval_model_queue, args=(self,) ) for i in range(self.workers)]



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

		if self.workers > 1:
			for proc in self.peek_procs:
				proc.start()
			for proc in self.eval_procs:
				proc.start()


		# create first models
		first_exprs = self.grower.first_exprs()

		# filter and memoize first_exprs models
		to_memo = self.filter_models(first_exprs)
		to_alge = self.memoize_models(to_memo)

		# algebra the models which made it through
		algebrad = self.algebra_models(to_alge)

		# filter and memoize the algebrad models
		to_memo = self.filter_models(algebrad)
		to_peek = self.memoize_models(to_memo)

		# pass along the unique expressions, plus the algebrad offspring unique
		to_peek = to_alge + to_peek

		to_eval = []
		if self.peek_npts == 0:
			to_eval = to_peek
		else:
			self.peek_models(to_peek)
			self.peek_push_models(to_peek)
			to_eval = self.peek_pop() + self.peek_pop() # twice the first time

		self.eval_models(to_eval)
		self.eval_push_models(to_eval)


	def loop(self, iterations):
		# main loop for # iterations
		for I in range(iterations):
			print "\n\nITER: ", I

			# pop some models, these will be finalized next
			popd = self.eval_pop()

			# expand these models, popd are finalized
			expanded = self.expand_models(popd)

			# filter and memoize expanded models
			to_memo = self.filter_models(expanded)
			to_alge = self.memoize_models(to_memo)

			# algebra the models which made it through
			algebrad = self.algebra_models(to_alge)

			# filter and memoize the algebrad models
			to_memo = self.filter_models(algebrad)
			to_peek = self.memoize_models(to_memo)

			# pass along the unique expressions, plus the algebrad offspring unique
			to_peek = to_alge + to_peek

			to_eval = []
			if self.peek_npts == 0:
				to_eval = to_peek
			else:
				# peek evaluate the unique models
				self.peek_models(to_peek)

				# push the peek'd models
				self.peek_push_models(to_peek)

				# pop some models for full evaluation
				to_eval = self.peek_pop()			

			# fully fit and evaluate these models
			self.eval_models(to_eval)

			# push fully fit models into the queue for expansion candidacy
			self.eval_push_models(to_eval)
			self.print_best(24)


	def print_best(self, count):
		best = selection.sortLogNondominated(self.final, count)
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
		final_list = selection.sortLogNondominated(final, len(final))

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
		
		print "\n\n", nx.info(self.GRAPH), "\n\n"

		# handle issue with extra stray node with parent_id == -2 (at end of nodes list)
		del_n = []
		for n in nx.nodes_iter(self.GRAPH):
			modl = self.memoizer.get_by_id(n)
			if modl.score is None:
				del_n.append(n)
		for n in del_n:
			self.GRAPH.remove_node(n)


		if self.workers > 1:
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
					
	def get_final_paretos(self):
		# pull all non-expanded models in queue out and push into final
		# could also use spea2_list here, they should have same contents
		final = self.final + self.nsga2_list 

		# generate final pareto fronts
		final_list = selection.sortLogNondominated(final, len(final))
		return final_list


	def expand_models(self, models):
		print "  expanding'n:", len(models)
		expanded = []
		for p in models:
			modls = self.grower.grow(p)
			p.expanded = True

			# any filters here?
			expanded.extend(modls)
			# any filters here?
			
			self.final.append(p)
			p.finalized = True

		print "  expanded to:", len(expanded) 
		return expanded

	def filter_models(self, models):
		print "  filtering:", len(models)
		passed = filters.filter_models(models, filters.default_filters)
		return passed

	def memoize_models(self, models):
		print "  memoizing:", len(models)
		unique = []
		for m in models:
			found, f_modl = self.memoizer.lookup(m)
			if found:
				self.GRAPH.add_edge(m.parent_id, f_modl.id, relation=m.gen_relation)

			did_ins = self.memoizer.insert(m)
			if did_ins:
				m.memoized = True
				m.rewrite_coeff()
				unique.append(m)
				# add node and edge
				self.GRAPH.add_node(m.id, modl=m)
				self.GRAPH.add_edge(m.parent_id, m.id, relation=m.gen_relation)

		print "  unique:", len(unique),"/",len(models)
		return unique

	def algebra_models(self, models):
		print "  algebra:", len(models)
		alges = []
		for modl in models:
			for meth in self.algebra_methods:
				manipd, err = algebra.manip_model(modl,meth)
				if err is not None:
					if err == "same":
						continue
					else:
						print "Error:", err
				else:
					# print modl.expr, "==", meth, "==>", manipd.expr, manipd.xs, manipd.cs
					manipd.parent_id = modl.id
					manipd.gen_relation = meth
					alges.append(manipd)
			modl.algebrad = True
		return alges

	def add_rm_const(self, models):
		print "  add_rm_c:", len(models)
		reverse = []
		for modl in models:
			rev = algebra.add_rm_c_term()
			reverse.append(rev)
		return reverse

	def peek_push_models(self, models):
		print "  peek_queue'n:", len(models)
		self.nsga2_peek.extend([m for m in models if m is not None and m.errored is False])
		self.spea2_peek.extend([m for m in models if m is not None and m.errored is False])
		for m in models:
			m.peek_queued = True
			# self.peek_push(m)

	def peek_push(self, modl):
		if modl is None or modl.errored is True:
			return
		self.nsga2_peek.append(modl)
		self.spea2_peek.append(modl)
		modl.peek_queued = True

	def eval_push_models(self, models):
		print "  eval_queue'n:", len(models)
		self.nsga2_list.extend([m for m in models if m is not None and m.errored is False])
		self.spea2_list.extend([m for m in models if m is not None and m.errored is False])
		for m in models:
			m.queued = True
			# self.eval_push(m)

	def eval_push(self, modl):
		if modl is None or modl.errored is True:
			return
		self.nsga2_list.append(modl)
		self.spea2_list.append(modl)
		modl.queued = True

	def peek_pop(self):
		nsga2_tmp = selection.selNSGA2(self.nsga2_peek, len(self.nsga2_peek))
		spea2_tmp = selection.selSPEA2(self.spea2_peek, len(self.spea2_peek))

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
		nsga2_tmp = selection.selNSGA2(self.nsga2_list, len(self.nsga2_list))
		spea2_tmp = selection.selSPEA2(self.spea2_list, len(self.spea2_list))

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
		if self.workers > 1:
			self.peek_models_multiprocess(models)
		else:
			print "  peek'n:", len(models)
			for m in models:
				passed = self.peek_model(m)
				if not passed or m.error is not None:
					print m.error, m.exception, "\n   ", m.expr
					continue
				m.peek_nfev = m.fit_result.nfev
				self.peek_nfev += m.peek_nfev

	def peek_models_multiprocess(self, models):
		print "  multi-peek'n:", len(models)

		for i,m in enumerate(models):
			try:
				self.peek_in_queue.put( (i,m) )
			except Exception, e:
				print "send error!", e, "\n  ", i, modl.expr
				break

		
		for i in range(len(models)):
			try:
				ret = self.peek_out_queue.get()
			except Exception, e:
				print "recv error!", e, "\n  ", i, modl.expr
				break

			pos = ret[0]
			err = ret[1]
			dat = ret[2]
			modl = models[ret[0]]

			if err is not None:
				modl.error = err
				modl.exception = dat
				modl.errored = True
				print "GOT HERE ERROR"
			else:
				modl.score = dat['score']
				modl.r2 = dat['r2']
				modl.evar = dat['evar']
				modl.peek_nfev = dat['nfev']
				self.peek_nfev += modl.peek_nfev

				for v in dat['params']:
					modl.params[v[0]].value = v[1]

				modl.peek_score = dat['score']
				modl.peek_r2 = dat['r2']
				modl.peek_evar = dat['evar']
				
				# build the fitness for selection
				vals = (modl.size(), modl.score)
				modl.fitness = creator.FitnessMin()
				modl.fitness.setValues( vals )
				modl.peeked = True


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
		if self.workers > 1:
			self.eval_models_multiprocess(models, self.workers)
		else:
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
				self.eval_nfev += modl.eval_nfev
				
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




