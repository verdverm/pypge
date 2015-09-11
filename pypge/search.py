import expand
import memoize



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

		self.prepare()

	def fit(self, X_train,Y_train):
		self.X_train = X_train
		self.Y_train = Y_train

		print X_train.shape, Y_train.shape
		
		self.prepare()
		self.loop()

	def predict(self, X_data):
		pass
		

	def prepare(self):
		self.bases = expand.GenBases(self.usable_vars,2,self.usable_funcs)
		for i,e in enumerate(self.bases):
			print i,e


	def loop(self):
		for I in range(self.max_iter):
			print "iter: ", I
