import sympy

class Model:

	def __init__(self, expr, xs=None, cs=None):
		self.expr = expr

		self.xs = None
		self.cs = None

		self.sz = 0


	def get_coeff(self):
		if self.coeff is not None:
			return self.coeff
		else:
			self.coeff = self.rewrite_coeff()

	def size(self):
		if self.sz == 0:
			self.sz = self.calc_tree_size()
		return self.sz

	def calc_tree_size(self):
		i = 0
		for e in sympy.preorder_traversal(self.expr):
			i+=1
		return i


	def rewrite_coeff(self):
		pass



