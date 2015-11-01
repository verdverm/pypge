from __future__ import print_function

from pypge import model
from pypge import expand
from pypge import filters
from pypge import algebra
from pypge import memoize
from pypge import evaluate
from pypge import fitness_funcs
from pypge import selection
from pypge import parallel

from pypge.timer import timewith

import numpy
import sympy

import networkx as nx

import multiprocessing as mp
import os, sys, time

numpy.random.seed(23)



class PGE:
	
	def __init__(self,**kwargs):
		# default values
		self.workers = 1
		self.queue_size = 4096

		self.max_iter = 100
		self.pop_count = 3
		self.peek_count = 2*self.pop_count
		self.peek_npts = 16

		self.min_size = 1
		self.max_size = 64
		self.min_depth = 1
		self.max_depth = 6

		self.max_power = 5

		self.algebra_methods = ["expand", "factor"]

		self.zero_epsilon = 1e-6  ## still need to use
		self.err_method = "mse"
		self.fitness_func = "normalized_size_score"

		self.system_type = None
		self.search_vars = None
		self.usable_vars = None
		self.usable_funcs = []

		self.func_level = "linear"
		self.init_level = "low"
		self.grow_level = "low"

		self.grow_params = {
			"func_level": "linear",
			"init_level": "low",
			"grow_level": "low",
			"subs_level": "med",
			"add_extend_level": "low",
			"mul_extend_level": "low",
		}

		self.print_timing = False
		self.log_details = False
		self.log_dir = "./logs/"


		# --------------------
		# --------------------
		# override with kwargs
		# --------------------
		# --------------------
		for key, value in kwargs.items():
			# print (key, value)
			setattr(self, key, value)
		# --------------------
		# --------------------
		# --------------------
		# --------------------


		# do some conversions for string params to python objects
		self.usable_funcs = expand.map_names_to_funcs(self.usable_funcs)
		# self.fitness_calc = fitness_funcs.get_fitness_calc(self.fitness_func)
		print(self.fitness_func)

		print("fitness: ", self.fitness_func_params)
		self.fitness_calc = fitness_funcs.build_fitness_calc(self.fitness_func_params)


		self.vars = sympy.symbols(self.usable_vars)
		if type(self.vars) is sympy.Symbol:
			self.vars = [self.vars]

		# check the configuration for correctness
		if not self.check_config():
			print ("ERROR: config missing values")
			return

		# initialize internal objects
		self.curr_iter = -1

		# number of function evaluations 
		self.peekd_models = 0
		self.evald_models = 0
		self.peek_nfev = 0 # mul by peek_npts
		self.eval_nfev = 0

		err_columns = [
		    "iteration",
		    "peekd_models",
		    "evald_models",
		    "peek_fit_loops",
		    "peek_point_evals",
		    "eval_fit_loops",
		    "eval_point_evals",
		    "total_point_evals", 
		    "best_size",
		    "best_err",
		    "best_r2",
		    "best_vari",
		    "ave_size",
		    "ave_err",
		    "ave_r2",
		    "ave_evar"
		]

		# log files
		os.makedirs(self.log_dir, exist_ok=True)

		log_files = ["main", "graph", "nodes", "evals", "errs", "final"]

		self.logs = {}
		self.logs["stdout"] = sys.stdout
		for lf in log_files:
			self.logs[lf] = open(self.log_dir + "pge_" + lf + ".log", "w")
		# self.logs["main"]   = open(self.log_dir + "pge_main.log", "w")
		# self.logs["graph"]  = open(self.log_dir + "pge_graph.log", "w")
		# self.logs["nodes"]  = open(self.log_dir + "pge_nodes.log", "w")
		# self.logs["errs"]   = open(self.log_dir + "pge_errs.log", "w")
		# self.logs["final"]   = open(self.log_dir + "pge_final.log", "w")
		print( ' '.join(err_columns), file=self.logs["errs"] )

		# memoizer & grower
		self.memoizer = memoize.Memoizer(self.vars)
		self.grower = expand.Grower(self.vars, self.usable_funcs, **self.grow_params)
		# self.grower = expand.Grower(self.vars, self.usable_funcs, 
		# 	func_level=self.func_level, init_level=self.init_level, grow_level=self.grow_level)

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
		s = "{}: node {} ".format(self.curr_iter, R.id)
		print(s, file=self.logs["graph"])

		self.peek_procs = []
		self.eval_procs = []
		self.alge_procs = []
		
		# multiprocessing stuff
		if self.workers > 1:
			self.peek_in_queue = mp.Queue(self.queue_size)
			self.peek_out_queue = mp.Queue(self.queue_size)
			self.peek_procs = [mp.Process(target=parallel.unwrap_self_peek_model_queue, args=(self,) ) for i in range(self.workers)]

			self.eval_in_queue = mp.Queue(self.queue_size)
			self.eval_out_queue = mp.Queue(self.queue_size)
			self.eval_procs = [mp.Process(target=parallel.unwrap_self_eval_model_queue, args=(self,) ) for i in range(self.workers)]

			self.alge_in_queue = mp.Queue(self.queue_size)
			self.alge_out_queue = mp.Queue(self.queue_size)
			self.alge_procs = [mp.Process(target=parallel.unwrap_self_alge_model_queue, args=(self,) ) for i in range(self.workers)]



	def check_config(self):
		"""
			This function checks the correctness of the PGE configuration.
			It is not quite complete at the time of this writing
		"""
		if self.search_vars == None \
		or self.usable_vars == None:
			return False

		complexities = ["low","med","high"]
		if self.init_level not in complexities \
		or self.grow_level not in complexities:
			return False


		return True

	def assign_iter_id(self, expr_list):
		for e in expr_list:
			e.iter_id = self.curr_iter


	# sklearn estimator interface functions
	def fit(self, X_train,Y_train):

		start = time.time()

		self.set_data(X_train,Y_train) # *** see note below
		self.preloop()
		self.loop(self.max_iter)
		self.finalize()

		end = time.time()

		runtime = '     {:14.4f} seconds'.format(end - start)
		print("TOTAL RUN TIME:", runtime)


		### Sklearn doesn't want us to store this data
		### But we want to for checkpointing and continuation
		### This may require a finalization function
		###   as we are finalizing at the end of loop right now
		###   either way, we want sklean interface, with curr finalization
		###   while still checkpointing, just need more storage and temps


	def set_data(self, X_train, Y_train):
		# set training data 
		self.X_train = X_train
		self.Y_train = Y_train
		self.eval_npts = len(self.Y_train)

		# set peeking data
		pos = numpy.random.randint(0,self.eval_npts, self.peek_npts)
		self.X_peek = self.X_train[:,pos]
		self.Y_peek = self.Y_train[pos]

		print ("train.shape:", self.X_train.shape, self.Y_train.shape)
		print ("peekn.shape:", self.X_peek.shape, self.Y_peek.shape)
		print ("\n\n")

	def preloop(self):
		# preloop setup (generates,evals,queues first models)
		print ("Preloop setup")

		if self.workers > 1:
			for proc in self.peek_procs:
				proc.start()
			for proc in self.eval_procs:
				proc.start()
			for proc in self.alge_procs:
				proc.start()

		L = None
		if self.log_details:
			L = self.logs
		T = None
		if self.print_timing:
			T = timewith()

		def pfunc(msg, iarg, numto=0, lognames=["stdout"], final=False):
			if T:
				s = "  {:3d} {:24s}| {:4d} ".format(self.curr_iter, msg, iarg)
				if numto == 0:
					s += "        "
				else:
					s += "-> {:4d} ".format(numto)
				if final:
					s += T.finalize()
				else:
					s += T.checkpoint(iarg)

				if len(lognames) == 0:
					return s
				elif L is not None:
					for logname in lognames:
						print(s, file=L[logname])


		# create first models
		first_exprs = self.grower.first_exprs()
		self.assign_iter_id(first_exprs)
		pfunc("create first exprs", len(first_exprs), lognames=["stdout","main"])

		# filter and memoize first_exprs models
		to_memo = self.filter_models(first_exprs)
		pfunc("first => filtered", len(first_exprs), numto=len(to_memo), lognames=["stdout","main"])

		to_alge = []
		if self.algebra_methods is not None and len(self.algebra_methods) > 0:
			to_alge = self.memoize_models(to_memo)
			pfunc("memoize => algebra", len(to_memo), numto=len(to_alge), lognames=["stdout","main"])

			# algebra the models which made it through
			algebrad = self.algebra_models(to_alge)
			self.assign_iter_id(algebrad)
			pfunc("algebra => result models", len(to_alge), numto=len(algebrad), lognames=["stdout","main"])

			# filter and memoize the algebrad models
			to_memo = self.filter_models(algebrad)
			pfunc("algebrad => filtered", len(algebrad), numto=len(to_memo), lognames=["stdout","main"])

		to_peek = self.memoize_models(to_memo)
		pfunc("memoized => fitting", len(to_memo), numto=len(to_peek), lognames=["stdout","main"])

		# pass along the unique expressions, plus the algebrad offspring unique
		to_peek = to_alge + to_peek
		pfunc("total for fitting", len(to_peek), lognames=["stdout","main"])


		to_eval = []
		if self.peek_npts == 0:
			to_eval = to_peek
		else:
			self.peek_models(to_peek)
			pfunc("peeking", len(to_peek), lognames=["stdout","main"])

			self.peek_push_models(to_peek)
			pfunc("peek pushing", len(to_peek), lognames=["stdout","main"])

			fromlen = len(self.nsga2_peek)
			to_eval = self.peek_pop() + self.peek_pop() # twice the first time
			pfunc("peek popping", fromlen, numto=len(to_eval), lognames=["stdout","main"])


		self.eval_models(to_eval)
		pfunc("evaling", len(to_eval), lognames=["stdout","main"])

		self.eval_push_models(to_eval)
		pfunc("eval pushing", len(to_eval), lognames=["stdout","main"])

		pfunc("total preloop time", -1, final=True, lognames=["stdout","main"])

		if self.log_details:
			for name, file_obj in self.logs.items():
				file_obj.flush()



	def loop(self, iterations):
		# main loop for # iterations
		for I in range(iterations):
			print ("\n\nITER: ", I)
			self.curr_iter = I
		
			L = None
			if self.log_details:
				L = self.logs
			T = None
			if self.print_timing:
				T = timewith()

			def pfunc(msg, iarg, numto=0, lognames=["stdout"], final=False):
				if T:
					s = "  {:3d} {:24s}| {:4d} ".format(self.curr_iter, msg, iarg)
					if numto == 0:
						s += "        "
					else:
						s += "-> {:4d} ".format(numto)
					if final:
						s += T.finalize()
					else:
						s += T.checkpoint(iarg)

					if len(lognames) == 0:
						return s
					else:
						for logname in lognames:
							print(s, file=L[logname])

			# pop some models, these will be finalized next
			fromlen = len(self.nsga2_list)
			popd = self.eval_pop()
			pfunc("eval popping", fromlen, numto=len(popd), lognames=["stdout","main"])

			# expand these models, popd are finalized
			expanded = self.expand_models(popd)
			self.assign_iter_id(expanded)
			pfunc("popped => expanded", len(popd), numto=len(expanded), lognames=["stdout","main"])

			# filter and memoize expanded models
			to_memo = self.filter_models(expanded)			
			pfunc("expanded => filtered", len(expanded), numto=len(to_memo), lognames=["stdout","main"])

			to_alge = []
			if self.algebra_methods is not None and len(self.algebra_methods) > 0:
				to_alge = self.memoize_models(to_memo)
				pfunc("memoize => algebra", len(to_memo), numto=len(to_alge), lognames=["stdout","main"])

				# algebra the models which made it through
				algebrad = self.algebra_models(to_alge)
				self.assign_iter_id(algebrad)
				pfunc("algebra => result models", len(to_alge), numto=len(algebrad), lognames=["stdout","main"])

				# filter and memoize the algebrad models
				to_memo = self.filter_models(algebrad)
				pfunc("algebrad => filtered", len(algebrad), numto=len(to_memo), lognames=["stdout","main"])

			to_peek = self.memoize_models(to_memo)
			pfunc("memoized => fitting", len(to_memo), numto=len(to_peek), lognames=["stdout","main"])

			# pass along the unique expressions, plus the algebrad offspring unique
			to_peek = to_alge + to_peek
			pfunc("total for fitting", len(to_peek), lognames=["stdout","main"])


			to_eval = []
			if self.peek_npts == 0:
				to_eval = to_peek
			else:
				# peek evaluate the unique models
				self.peek_models(to_peek)
				pfunc("peeking", len(to_peek), lognames=["stdout","main"])

				# push the peek'd models
				self.peek_push_models(to_peek)
				pfunc("peek pushing", len(to_peek), lognames=["stdout","main"])

				# pop some models for full evaluation
				fromlen = len(self.nsga2_peek)
				to_eval = self.peek_pop()
				pfunc("peek popping", fromlen, numto=len(to_eval), lognames=["stdout","main"])

			# fully fit and evaluate these models
			self.eval_models(to_eval)
			pfunc("evaling", len(to_eval), lognames=["stdout","main"])

			# push fully fit models into the queue for expansion candidacy
			self.eval_push_models(to_eval)
			pfunc("eval pushing", len(to_eval), lognames=["stdout","main"])

			pfunc("total loop time", I, final=True, lognames=["stdout","main"])
			self.print_best(24)

			s = "{:3d} {} {}   {} {} {} {} {}   {} {} {} {}   {} {} {} {}".format(
					self.curr_iter, 
					self.peekd_models, 
					self.evald_models,

					self.peek_nfev, 
					self.peek_nfev * self.peek_npts,
					self.eval_nfev, 
					self.eval_nfev * self.eval_npts,
					self.peek_nfev * self.peek_npts + self.eval_nfev * self.eval_npts,

					self.best_size,
					self.best_err,
					self.best_r2,
					self.best_vari,

					self.ave_size,
					self.ave_err,
					self.ave_r2,
					self.ave_vari

				)
			print(s, file=self.logs["errs"])

			if self.log_details:
				for name, file_obj in self.logs.items():
					file_obj.flush()



	def print_best(self, count, file=sys.stdout):
		self.fitness_calc(self.final)
		best = selection.sortLogNondominated(self.final, count)
		print ("Best so far", file=file)
		print (best[0][0].print_long_columns(), file=file)
		print ("-----------------------------------------------------------------------------------", file=file)
		cnt = 0
		self.best_size = 0
		self.best_err = 10000000000
		self.best_r2 = 0
		self.best_vari = 0
		self.ave_size = 0
		self.ave_err = 0
		self.ave_r2 = 0
		self.ave_vari = 0

		for front in best:
			for m in front:
				if cnt >= count:
					return
				cnt += 1
				print ("  ", m.print_long(), file=file)

				if m.score < self.best_err:
					self.best_size = m.size()
					self.best_err = m.score
					self.best_r2 = m.r2
					self.best_vari = m.evar
				self.ave_size += m.size()
				self.ave_err += m.score
				self.ave_r2 += m.r2
				self.ave_vari += m.evar

			print ("", file=file)

		self.ave_size /= float(count)
		self.ave_err /= float(count)
		self.ave_r2 /= float(count)
		self.ave_vari /= float(count)


	def print_final_models(self, model_list, count, file=sys.stdout):
		print (model_list[0][0].print_csv_columns(), file=file)

		cnt = 0
		for front in model_list:
			for m in front:
				if cnt >= count:
					return
				cnt += 1
				print (m.print_csv(), file=file)


	def finalize(self, nfronts=4):
		# finalization
		print ("\n\nFinalizing\n\n")

		# pull all non-expanded models in queue out and push into final
		# could also use spea2_list here, they should have same contents
		final = self.final + self.nsga2_list 

		# generate final pareto fronts
		self.fitness_calc(final)
		final_list = selection.sortLogNondominated(final, len(final))

		self.print_final_models(final_list, 128, self.logs["final"])

		# print first 4 pareto fronts
		print ("Final Results")
		print (final_list[0][0].print_columns())
		print ("-----------------------------------------------------------------------------------")
		for front in final_list[:nfronts]:
			for m in front:
				print ("  ", m)
			print ("")

		print ("\n")
		print ("num peekd models:  ", self.peekd_models)
		print ("num evald models:  ", self.evald_models)
		print ("num peek evals:  ", self.peek_nfev, self.peek_nfev * self.peek_npts)
		print ("num eval evals:  ", self.eval_nfev, self.eval_nfev * self.eval_npts)
		print ("num total evals: ", self.peek_nfev * self.peek_npts + self.eval_nfev * self.eval_npts)
		
		print ("\n\n", nx.info(self.GRAPH), "\n\n")

		# handle issue with extra stray node with parent_id == -2 (at end of nodes list)
		del_n = []
		for n in nx.nodes_iter(self.GRAPH):
			modl = self.memoizer.get_by_id(n)
			if modl.score is None:
				del_n.append(n)
		for n in del_n:
			self.GRAPH.remove_node(n)


		if self.workers > 1:
			print ("\n\nstopping workers")
			for proc in self.peek_procs:
				self.peek_in_queue.put(None)
			for proc in self.eval_procs:
				self.eval_in_queue.put(None)
			for proc in self.alge_procs:
				self.alge_in_queue.put(None)

			for proc in self.peek_procs:
				proc.join()
			for proc in self.eval_procs:
				proc.join()
			for proc in self.alge_procs:
				proc.join()

		print ("\n\ndone\n\n")

		if self.log_details:
			for name, file_obj in self.logs.items():
				if file_obj is not sys.stdout:
					file_obj.close()
					
	def get_final_paretos(self):
		# pull all non-expanded models in queue out and push into final
		# could also use spea2_list here, they should have same contents
		final = self.final + self.nsga2_list 

		# generate final pareto fronts
		self.fitness_calc(final)
		final_list = selection.sortLogNondominated(final, len(final))
		return final_list


	def expand_models(self, models):
		expanded = []
		for p in models:
			modls = self.grower.grow(p)
			p.expanded = True

			expanded.extend(modls)
			
			self.final.append(p)
			p.finalized = True

		return expanded

	def filter_models(self, models):
		passed = filters.filter_models(models, filters.default_filters)
		return passed

	def memoize_models(self, models):
		# print ("  MEMOIZING:", len(models))
		unique = []
		for i,m in enumerate(models):
			found, f_modl = self.memoizer.lookup(m)
			# print(i, found, m.id, m.orig)
			if found:
				self.GRAPH.add_edge(m.parent_id, f_modl.id, relation=m.gen_relation)
				s = "{}: EDGE {} -> {} r {}".format(self.curr_iter, m.parent_id, f_modl.id, m.gen_relation)
				print(s, file=self.logs["graph"])

			did_ins = self.memoizer.insert(m)
			if did_ins:
				m.memoized = True
				m.rewrite_coeff()
				unique.append(m)
				# add node and edge
				self.GRAPH.add_node(m.id, modl=m)				
				s = "{}: node {} ".format(self.curr_iter, m.id)
				print(s, file=self.logs["graph"])
				print(s, m.orig, file=self.logs["nodes"])

				self.GRAPH.add_edge(m.parent_id, m.id, relation=m.gen_relation)
				s = "{}: edge {} -> {} r {}".format(self.curr_iter, m.parent_id, m.id, m.gen_relation)
				print(s, file=self.logs["graph"])

		# print ("  UNIQUE:", len(unique),"/",len(models))
		return unique

	def algebra_models(self, models):
		if self.workers > 1:
			return self.algebra_models_multiprocess(models)
		else:
			# print ("  algebra:", len(models))
			alges = []
			for modl in models:
				for meth in self.algebra_methods:
					manipd, err = algebra.manip_model(modl,meth)
					if err is not None:
						if err == "same":
							continue
						else:
							print ("Error:", err)
					else:
						# print (modl.expr, "==", meth, "==>", manipd.expr, manipd.xs, manipd.cs)
						manipd.parent_id = modl.id
						manipd.gen_relation = meth
						alges.append(manipd)
				modl.algebrad = True
			return alges

	def algebra_models_multiprocess(self, models):
		# print ("  multi-algebra:", len(models))
		alges = []
		
		for i,m in enumerate(models):
			for meth in self.algebra_methods:
				try:
					self.alge_in_queue.put( (i,m, meth) )
				except Exception as e:
					print ("alge send error!", e, "\n  ", i, m.expr)
					break
			m.algebrad = True

		
		for i in range(len(models) * 2):
			try:
				ret = self.alge_out_queue.get()
			except Exception as e:
				print ("alge recv error!", e, "\n  ", i)
				break

			pos = ret[0]
			err = ret[1]
			meth = ret[2]
			manipd = ret[3]
			modl = models[ret[0]]

			if err is not None:
				if err == "same":
					continue
				else:
					print ("Error:", err)
			else:
				# print (modl.expr, "==", meth, "==>", manipd.expr, manipd.xs, manipd.cs)
				manipd.parent_id = modl.id
				manipd.gen_relation = meth
				alges.append(manipd)

		return alges


	def add_rm_const(self, models):
		# print ("  add_rm_c:", len(models))
		reverse = []
		for modl in models:
			rev = algebra.add_rm_c_term()
			reverse.append(rev)
		return reverse

	def peek_push_models(self, models):
		# print ("  peek_queue'n:", len(models))
		ms = [m for m in models if m is not None and m.errored is False and m.score is not None]
		self.nsga2_peek.extend(ms)
		# self.spea2_peek.extend(ms)
		for m in ms:
			m.peek_queued = True
		return ms

	def eval_push_models(self, models):
		# print ("  eval_queue'n:", len(models))
		ms = [m for m in models if m is not None and m.errored is False and m.score is not None]
		self.nsga2_list.extend(ms)
		# self.spea2_list.extend(ms)
		for m in models:
			m.queued = True
		return ms


	def peek_pop(self):
		
		# print ("Applying fitness function in peek_pop")
		self.fitness_calc(self.nsga2_peek)

		nsga2_popd = selection.selNSGA2(self.nsga2_peek, self.peek_count, nd='log')
		# spea2_popd = selection.selSPEA2(self.spea2_peek, self.peek_count)

		# nsga2_tmp = selection.selNSGA2(self.nsga2_peek, len(self.nsga2_peek))
		# spea2_tmp = selection.selSPEA2(self.spea2_peek, len(self.spea2_peek))
		# nsga2_popd, self.nsga2_peek = nsga2_tmp[:self.peek_count], nsga2_tmp[self.peek_count:]
		# spea2_popd, self.spea2_peek = spea2_tmp[:self.peek_count], spea2_tmp[self.peek_count:]

		popd_set = set()
		for p in nsga2_popd:
			popd_set.add(p)
		# for p in spea2_popd:
		# 	popd_set.add(p)

		popd_list = list(popd_set)
		# print ("  uniqued peek'd pop'd:")
		for p in popd_list:
			p.peek_popped = True
			# print ("    ", p)

		self.nsga2_peek = [m for m in self.nsga2_peek if not m.peek_popped]
		# self.spea2_peek = [m for m in self.spea2_peek if not m.peek_popped]

		# print ("  peek_pop'd", len(popd_list), "of", len(self.nsga2_peek) + len(popd_list))
		return popd_list

	def eval_pop(self):
		# print ("Applying fitness function in eval_pop")
		self.fitness_calc(self.nsga2_list)

		nsga2_popd = selection.selNSGA2(self.nsga2_list, self.pop_count, nd='log')
		# spea2_popd = selection.selSPEA2(self.spea2_list, self.pop_count)

		# nsga2_tmp = selection.selNSGA2(self.nsga2_list, len(self.nsga2_list))
		# spea2_tmp = selection.selSPEA2(self.spea2_list, len(self.spea2_list))
		# nsga2_popd, self.nsga2_list = nsga2_tmp[:self.pop_count], nsga2_tmp[self.pop_count:]
		# spea2_popd, self.spea2_list = spea2_tmp[:self.pop_count], spea2_tmp[self.pop_count:]

		popd_set = set()
		for p in nsga2_popd:
			popd_set.add(p)
		# for p in spea2_popd:
		# 	popd_set.add(p)

		popd_list = list(popd_set)
		# print ("  uniqued eval'd pop'd:")
		for p in popd_list:
			p.popped = True
			# print ("    ", p)

		self.nsga2_list = [m for m in self.nsga2_list if not m.popped]
		# self.spea2_list = [m for m in self.spea2_list if not m.popped]

		# print ("  eval_pop'd", len(popd_list), "of", len(self.nsga2_list) + len(popd_list))
		return popd_list


	def peek_models(self, models):
		if self.workers > 1:
			self.peek_models_multiprocess(models)
		else:
			# print ("  peek'n:", len(models))
			for modl in models:
				passed = evaluate.peex_model(modl, self.vars, self.X_peek, self.Y_peek, self.err_method)
				if not passed or modl.error is not None:
					print (modl.error, modl.exception, "\n   ", modl.expr)
					continue
				modl.peek_nfev = modl.fit_result.nfev
				self.peek_nfev += modl.peek_nfev
				self.peekd_models += 1

				if modl.parent_id >= 0:
					parent = self.memoizer.get_by_id(modl.parent_id)
					modl.improve_score = parent.score - modl.score
					modl.improve_r2 = modl.r2 - parent.r2
					modl.improve_evar = modl.evar - parent.evar
					modl.improve_aic = parent.aic - modl.aic
					modl.improve_bic = parent.bic - modl.bic
					modl.improve_redchi = parent.redchi - modl.redchi
				else:
					# should probaly normalized this across the initial population and permenately set
					modl.improve_score  = -0.000001 * modl.score
					modl.improve_r2     = -0.000001 * modl.r2
					modl.improve_evar   = -0.000001 * modl.evar
					modl.improve_aic    = -0.000001 * modl.aic
					modl.improve_bic    = -0.000001 * modl.bic
					modl.improve_redchi = -0.000001 * modl.redchi

	def peek_models_multiprocess(self, models):
		# print ("  multi-peek'n:", len(models))

		for i,m in enumerate(models):
			try:
				self.peek_in_queue.put( (i,m) )
			except Exception as e:
				print ("send error!", e, "\n  ", i, modl.expr)
				break

		
		for i in range(len(models)):
			try:
				ret = self.peek_out_queue.get()
			except Exception as e:
				print ("recv error!", e, "\n  ", i, modl.expr)
				break

			pos = ret[0]
			err = ret[1]
			dat = ret[2]
			modl = models[ret[0]]

			if err is not None:
				modl.error = err
				modl.exception = dat
				modl.errored = True
				# print ("GOT HERE ERROR", err, dat)
			else:
				modl.score  = dat['score']
				modl.r2     = dat['r2']
				modl.evar   = dat['evar']
				modl.aic    = dat['aic']
				modl.bic    = dat['bic']
				modl.chisqr = dat['chisqr']
				modl.redchi = dat['redchi']
				
				modl.peek_score  = modl.score
				modl.peek_r2     = modl.r2
				modl.peek_evar   = modl.evar
				modl.peek_aic    = modl.aic
				modl.peek_bic    = modl.bic
				modl.peek_chisqr = modl.chisqr
				modl.peek_redchi = modl.redchi

				modl.peek_nfev = dat['nfev']
				self.peek_nfev += modl.peek_nfev
				self.peekd_models += 1
				for v in dat['params']:
					modl.params[v[0]].value = v[1]

				modl.peek_score = dat['score']
				modl.peek_r2 = dat['r2']
				modl.peek_evar = dat['evar']
				modl.peeked = True



	def eval_models(self, models):
		if self.workers > 1:
			self.eval_models_multiprocess(models, self.workers)
		else:
			# print ("  eval'n:", len(models))
			for modl in models:
				passed = evaluate.eval_model(modl, self.vars, self.X_train, self.Y_train, self.err_method)
				if not passed or modl.error is not None:
					info = "{:5d}  ERROR     ".format(modl.id)
					print(info, modl.expr, modl.jac, file=self.logs["evals"])

				else:
					self.eval_nfev += modl.eval_nfev
					self.evald_models += 1
					modl.eval_nfev = modl.fit_result.nfev

					info = "{:5d}  {:5d}     ".format(modl.id, modl.eval_nfev)
					print(info, modl.expr, modl.jac, file=self.logs["evals"])
			
					if modl.parent_id >= 0:
						parent = self.memoizer.get_by_id(modl.parent_id)
						modl.improve_score = parent.score - modl.score
						modl.improve_r2 = modl.r2 - parent.r2
						modl.improve_evar = modl.evar - parent.evar
						modl.improve_aic = parent.aic - modl.aic
						modl.improve_bic = parent.bic - modl.bic
						modl.improve_redchi = parent.redchi - modl.redchi
					else:
						# should probaly normalized this across the initial population and permenately set
						modl.improve_score  = -0.000001 * modl.score
						modl.improve_r2     = -0.000001 * modl.r2
						modl.improve_evar   = -0.000001 * modl.evar
						modl.improve_aic    = -0.000001 * modl.aic
						modl.improve_bic    = -0.000001 * modl.bic
						modl.improve_redchi = -0.000001 * modl.redchi

	def eval_models_multiprocess(self, models, processes):
		# print ("  multi-eval'n:", len(models))

		LenModels = len(models)
		cnt1 = 0
		for i,m in enumerate(models):
			pkg = (cnt1,m)
			self.eval_in_queue.put( pkg )
			cnt1 += 1

		# print("  LENGTHS: ", LenModels, cnt1)

		cnt2 = 0		
		for i in range(cnt1):
			ret = self.eval_out_queue.get()
			pos = ret[0]
			err = ret[1]
			dat = ret[2]

			cnt2 += 1

			try:
				modl = models[pos]
			except Exception as e:
				print ("POS ERROR: ", pos, len(models), e, ret)
				continue

			if err is not None:
				# print("ERROR IS NOT NONE", err)
				modl.error = err
				modl.exception = dat
				modl.errored = True
			else:
				modl.score = dat['score']
				modl.r2 = dat['r2']
				modl.evar = dat['evar']
				modl.aic = dat['aic']
				modl.bic = dat['bic']
				modl.chisqr = dat['chisqr']
				modl.redchi = dat['redchi']

				modl.eval_nfev = dat['nfev']
				self.eval_nfev += modl.eval_nfev
				self.evald_models += 1
				
				info = "{:5d}  {:5d}     ".format(modl.id, modl.eval_nfev)
				print(info, modl.expr, modl.jac, file=self.logs["evals"])

				for v in dat['params']:
					if len(v[0]) == 1 and v[0] == 'C':
						print("GOT THE SINGULAR: ", v[0], dat['params'])
						continue
					# if v[0] in modl.params:
					modl.params[v[0]].value = v[1]

				if modl.parent_id >= 0:
					parent = self.memoizer.models[modl.parent_id]
					# print("  ", parent.id, parent.expr )
					modl.improve_score = parent.score - modl.score
					modl.improve_r2 = modl.r2 - parent.r2
					modl.improve_evar = modl.evar - parent.evar
					modl.improve_aic = parent.aic - modl.aic
					modl.improve_bic = parent.bic - modl.bic
					modl.improve_redchi = parent.redchi - modl.redchi
				else:
					# should probaly normalized this across the initial population and permenately set
					modl.improve_score  = -0.000001 * modl.score
					modl.improve_r2     = -0.000001 * modl.r2
					modl.improve_evar   = -0.000001 * modl.evar
					modl.improve_aic    = -0.000001 * modl.aic
					modl.improve_bic    = -0.000001 * modl.bic
					modl.improve_redchi = -0.000001 * modl.redchi

				modl.evaluated = True

		# print("  CNTS: ", cnt1, cnt2)





