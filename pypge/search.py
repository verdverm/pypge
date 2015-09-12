import sympy

import expand
import memoize
import model


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
			print key, value
			setattr(self, key, value)

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

		self.vars = sympy.symbols(self.usable_vars)
		if type(self.vars) is sympy.Symbol:
			self.vars = [self.vars]


		self.memoizer = memoize.Memoizer(self.vars)

		self.bases = expand.GenBases(self.vars, 2, self.usable_funcs)


		for i,e in enumerate(self.bases):
			did_ins = self.memoizer.insert(e)
			m = model.Model(e)
			size = m.size()
			m.rewrite_coeff()
			print i,m.expr, size, m.cs

			# if did_ins:
			# 	print "  train..."
			# 	print "  score..."
			# 	print "  queue..."

		self.prepared = True


	def loop(self):
		if not self.prepared:
			print "PGE not prepared"
			return 

		for I in range(self.max_iter):
			print "iter: ", I
			# print "  pop'n..."
			# print "  expand..."
			# print "  memoize..."
			# print "    if new:"
			# print "      train..."
			# print "      score..."
			# print "      queue..."




	# sklearn estimator interface functions
	def fit(self, X_train,Y_train):
		self.X_train = X_train
		self.Y_train = Y_train

		print X_train.shape, Y_train.shape
		
		self.loop()

	def predict(self, X_data):
		pass
		








