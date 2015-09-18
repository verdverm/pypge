import sympy

import tests

import model
import expand
import memoize
import evaluate
import select

import lmfit

from deap.tools import emo

class PGE:
	
	def __init__(self,**kwargs):
		# default values
		self.max_iter = 100
		self.pop_count = 3

		self.min_size = 1
		self.max_size = 64
		self.min_depth = 1
		self.max_depth = 6

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


		self.prepared = False
		self.prepare()


	def check_config(self):
		if self.system_type == None \
		or self.search_vars == None \
		or self.usable_vars == None:
			return False
		return True


	def prepare(self):

		if not self.check_config():
			print "ERROR: config missing values"
			return

		self.memoizer = memoize.Memoizer(self.vars)
		self.queue = select.ModelQueue(self.max_size)
		self.grower = expand.Grower(self.vars, self.usable_funcs)
		self.final = select.ModelQueue(self.max_size)

		self.nsga2_list = []
		self.spea2_list = []

		first_exprs = self.grower.first_exprs()
		for i,e in enumerate(first_exprs):
			m = model.Model(e)
			did_ins = self.memoizer.insert(m)
			size = m.size()
			m.rewrite_coeff()
			# print i,m.expr, size, m.id

			if did_ins:
				evaluate.Fit(m, self.vars, tests.F_1_X, tests.F_1_Y)
				if m.error or not m.fit_result.success:
					m.state = "errored"
					continue
				m.state = "fitted"
				y_pred = evaluate.Eval(m, self.vars, tests.F_1_X)
				m.score, err = evaluate.Score(tests.F_1_Y, y_pred)
				if err is not None:
					m.error = "errored while scoring"
					m.state = "errored"
					continue
				m.fitness.setValues( (m.size(), m.score) )
				m.state = "scored"	

				self.queue.push(m)
				self.nsga2_list.append(m)
				self.spea2_list.append(m)
				m.state = "queued"


		self.prepared = True


	def loop(self):
		if not self.prepared:
			print "PGE not prepared"
			return 

		for I in range(self.max_iter):
			print "\nITER: ", I

			# print "  pop'n..."
			nsga2_tmp = emo.selNSGA2(self.nsga2_list, len(self.nsga2_list))
			spea2_tmp = emo.selSPEA2(self.spea2_list, len(self.spea2_list))

			nsga2, self.nsga2_list = nsga2_tmp[:self.pop_count], nsga2_tmp[self.pop_count:]
			spea2, self.spea2_list = spea2_tmp[:self.pop_count], nsga2_tmp[self.pop_count:]

			popd = self.queue.pop(self.pop_count)
			print "  popped:"
			for p in popd:
				print "    ", p

			print "  nsga2:"
			for p in nsga2:
				print "    ", p

			print "  spea2:"
			for p in spea2:
				print "    ", p

			# print "  expand..."
			expanded = []
			for i,p in enumerate(popd):
				p.state = "popped"
				ex = self.grower.grow(p)
				# print "    ", p, " -> ", len(ex)
				# print "    ", p, "  ~~  ", picked[i]
				expanded.extend(ex)
				p.state = "expanded"
				self.final.push(p)
				p.state = "finalized"

			print "  expanded: ", len(expanded) 
			# for e in expanded:
			# 	print e

			for i,e in enumerate(expanded):

					# print "  memoize..."
					m = model.Model(e)
					did_ins = self.memoizer.insert(m)
					size = m.size()
					m.rewrite_coeff()

					# print "    if new:"
					if did_ins:
						# print "      train..."
						evaluate.Fit(m, self.vars, tests.F_1_X, tests.F_1_Y)
						if m.error or not m.fit_result.success:
							m.state = "errored"
							continue
						m.state = "fitted"
						# print "      score..."
						y_pred = evaluate.Eval(m, self.vars, tests.F_1_X)
						m.score, err = evaluate.Score(tests.F_1_Y, y_pred)
						if err is not None:
							m.error = "errored while scoring"
							m.state = "errored"
							continue
						m.fitness.setValues( (m.size(), m.score) )
						m.state = "scored"
						# print "      queue..."
						self.queue.push(m)
						self.nsga2_list.append(m)
						self.spea2_list.append(m)
						m.state = "queued"




	# sklearn estimator interface functions
	def fit(self, X_train,Y_train):
		self.X_train = X_train
		self.Y_train = Y_train

		print X_train.shape, Y_train.shape
		
		self.loop()

	def predict(self, X_data):
		pass
		








