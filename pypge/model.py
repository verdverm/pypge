import sympy
C = sympy.Symbol('C')
CS = [sympy.Symbol("C_"+str(i)) for i in range(8)]

from lmfit import Parameters


class Model:

	def __init__(self, expr, xs=None, cs=None):
		self.id = -1
		self.parent_id = -1
		self.iter_id = -1

		self.state = "new"
		self.error = None

		self.orig = expr
		self.expr = None

		self.xs = None
		self.cs = None
		self.params = None

		self.sz = 0

		self.rewrite_coeff()

		params = Parameters()
		for i,c in enumerate(self.cs):
			params.add('C_'+str(i), value=1.0)

		self.params = params

	def __str__(self):
		return str(self.size()) + "  " + str(self.score) + "  " + str(self.expr)


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
		expr, ii = self._rewrite_coeff_helper(self.orig, 0)
		self.expr = expr
		self.cs = CS[:ii]


	def _rewrite_coeff_helper(self, expr, ii):
		ret = expr
		if not expr.is_Atom:
			args = []
			for i,e in enumerate(expr.args):
				if not e.is_Atom:
					ee, ii = self._rewrite_coeff_helper(e,ii)
					args.append(ee)
					# args = args + ee
				elif e == C:
					args.append(CS[ii])
					# args = args + cs[ii]
					ii += 1
				else:
					args.append(e)
			args = tuple(args)
			ret = expr.func(*args)
		return ret,ii



# x,y,z = sympy.symbols("x y z")

# print cs

# f = C*x+C*y+C*z
# F, ii = rewrite_coeff_helper(f,0)
# G, ii = rewrite_coeff_helper(f,3)
# args = (x,y,z)
# F = f.func(*args)
# print F

# g = f.subs(cs)
# print f
# print F
# print G
# print g
