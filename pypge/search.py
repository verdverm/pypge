import sympy

import tests

import model
import expand
import memoize
import evaluate
import select

import lmfit

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
		if self.system_type == None or self.search_vars == None or self.usable_vars == None:
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

		# self.bases = expand.GenerateInitialModels(self.vars, 2, self.usable_funcs)

		for i,e in enumerate(self.grower.first_exprs()):
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
				m.state = "scored"	

				self.queue.push(m)
				m.state = "queued"


		self.prepared = True


	def loop(self):
		if not self.prepared:
			print "PGE not prepared"
			return 

		for I in range(self.max_iter):
			print "ITER: ", I

			# print "  pop'n..."
			popd = self.queue.pop(self.pop_count)
			print "\npopped:"
			for p in popd:
				print p

			# print "  expand..."
			expanded = []
			for p in popd:
				p.state = "popped"
				ex = self.grower.grow(p)
				expanded.extend(ex)
				p.state = "expanded"
				self.final.push(p)
				p.state = "finalized"

			# print "\nexpanded:"
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
						m.state = "scored"
						# print "      queue..."
						self.queue.push(m)
						m.state = "queued"




	# sklearn estimator interface functions
	def fit(self, X_train,Y_train):
		self.X_train = X_train
		self.Y_train = Y_train

		print X_train.shape, Y_train.shape
		
		self.loop()

	def predict(self, X_data):
		pass
		








