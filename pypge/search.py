import model
import expand
import memoize
import evaluate

import numpy
import sympy
import lmfit
from deap.tools import emo

import networkx as nx

class PGE:
	
	def __init__(self,**kwargs):
		# default values
		self.max_iter = 100
		self.pop_count = 3

		self.min_size = 1
		self.max_size = 64
		self.min_depth = 1
		self.max_depth = 6

		self.max_power = 5

		self.zero_epsilon = 1e-6
		self.err_method = "mse"

		self.system_type = None
		self.search_vars = None
		self.usable_vars = None
		self.usable_funcs = None

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

		self.memoizer = memoize.Memoizer(self.vars)
		self.grower = expand.Grower(self.vars, self.usable_funcs)
		self.iter_expands = []

		# Pareto Front stuff
		self.nsga2_list = []
		self.spea2_list = []
		self.nondom_list = []
		self.lognondom_list = []
		self.final = []

		# Relationship Graph
		r = sympy.Symbol("root")
		self.root_model = model.Model(r)
		R = self.root_model
		R.id = -1
		R.score = 9999999999999.
		R.r2 = -100.
		R.evar = -100.

		self.iter_expands.append([R])

		self.graph = nx.MultiDiGraph()
		self.graph.add_node(R, modl=R)


	# sklearn estimator interface functions
	def fit(self, X_train,Y_train):
		self.X_train = X_train
		self.Y_train = Y_train
		
		self.loop()


	def check_config(self):
		if self.system_type == None \
		or self.search_vars == None \
		or self.usable_vars == None:
			return False
		return True


	def loop(self):

		# preloop setup (generates,evals,queues first models)
		self.first_exprs = self.grower.first_exprs()
		self.iter_expands.append(self.first_exprs)

		to_eval = []
		for i,m in enumerate(self.first_exprs):
			found, f_modl = self.memoizer.lookup(m)
			if found:
				p = self.memoizer.get_by_id(m.parent_id)
				self.graph.add_edge(p, m, relation="ex_dupd")
				continue

			did_ins = self.memoizer.insert(m)
			size = m.size()
			m.rewrite_coeff()

			if did_ins:
				to_eval.append(m)
				# add node and edge
				self.graph.add_node(m, modl=m)
				p = self.memoizer.get_by_id(m.parent_id)
				self.graph.add_edge(p, m, relation="expanded")

		for m in to_eval:
			passed = self.eval(m)
			if not passed or m.error is not None:
				print m.error, m.exception
				continue
			self.push(m)



		# main loop for # iterations
		for I in range(self.max_iter):
			print "\nITER: ", I

			popd = self.pop()

			expanded = []
			for i,p in enumerate(popd):
				p.state = "popped"
				modls = self.grower.grow(p)

				expanded.extend(modls)
				p.state = "expanded"
				self.final.append(p)
				p.state = "finalized"

			print "  expanded: ", len(expanded) 

			self.iter_expands.append(expanded)


			to_eval = []
			for i,m in enumerate(expanded):
				found, f_modl = self.memoizer.lookup(m)
				if found:
					p = self.memoizer.get_by_id(m.parent_id)
					self.graph.add_edge(p, m, relation="ex_dupd")
					continue

				did_ins = self.memoizer.insert(m)
				size = m.size()
				m.rewrite_coeff()

				if did_ins:
					to_eval.append(m)
					# add node and edge
					self.graph.add_node(m, modl=m)
					p = self.memoizer.get_by_id(m.parent_id)
					self.graph.add_edge(p, m, relation="expanded")
				

			for m in to_eval:
				passed = self.eval(m)
				if not passed or m.error is not None:
					print m.error, m.exception
					continue
				self.push(m)


		# finalization
		print "\n\nFinalizing\n\n"

		# pull all non-expanded models in queue out and push into final
		# could also use spea2_list here, they should have same contents
		self.final = self.final + self.nsga2_list 

		# generate final pareto fronts
		final_list = emo.selNSGA2(self.final, len(self.final))

		# print first 4 pareto fronts
		print "Final Results"
		print "      id:  sz           error         r2    expld_vari    theModel"
		print "-----------------------------------------------------------------------------------"
		for m in final_list[:32]:
			print "  ", m
		
		print "\n\n", nx.info(self.graph), "\n\n"

		# handle issue with extra stray node with parent_id == -2 (at end of nodes list)
		del_n = []
		for n in nx.nodes_iter(self.graph):
			if n.score is None:
				del_n.append(n)
		for n in del_n:
			self.graph.remove_node(n)

		print "\n\ndone\n\n"
					

	def push(self, model):
		self.nsga2_list.append(model)
		self.spea2_list.append(model)
		model.state = "queued"

	def pop(self):
		nsga2_tmp = emo.selNSGA2(self.nsga2_list, len(self.nsga2_list))
		spea2_tmp = emo.selSPEA2(self.spea2_list, len(self.spea2_list))

		self.nsga2_popd, self.nsga2_list = nsga2_tmp[:self.pop_count], nsga2_tmp[self.pop_count:]
		self.spea2_popd, self.spea2_list = spea2_tmp[:self.pop_count], spea2_tmp[self.pop_count:]

		popd_set = set()
		# print "  nsga2:"
		for p in self.nsga2_popd:
			popd_set.add(p)
			# print "    ", p

		# print "  spea2:"
		for p in self.spea2_popd:
			popd_set.add(p)
			# print "    ", p


		popd_list = list(popd_set)
		print "  uniqued pop'd:"
		for p in popd_list:
			p.popped = True
			print "    ", p

		self.nsga2_list = [m for m in self.nsga2_list if not m.popped]
		self.spea2_list = [m for m in self.spea2_list if not m.popped]

		return popd_list


	def eval(self, model):
		# fit the model
		evaluate.Fit(model, self.vars, self.X_train, self.Y_train)
		if model.error or not model.fit_result.success:
			model.state = "errored"
			return False
		model.state = "fitted"
		
		# score the model
		y_pred = evaluate.Eval(model, self.vars, self.X_train)

		model.score, err = evaluate.Score(self.Y_train, y_pred, self.err_method)
		if err is not None:
			print err
			model.error = "errored while scoring"
			model.state = "errored"
			return False
		
		model.r2, err = evaluate.Score(self.Y_train, y_pred, "r2")
		if err is not None:
			model.error = "errored while r2'n"
			model.state = "errored"
			return False
		
		model.evar, err = evaluate.Score(self.Y_train, y_pred, "evar")
		if err is not None:
			model.error = "errored while evar'n"
			model.state = "errored"
			return False
		
		
		# build the fitness for selection
		vals = (model.size(), model.score)
		model.fitness.setValues( vals )
		model.state = "scored"

		return True # passed









