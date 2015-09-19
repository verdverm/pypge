from sympy import *
init_printing(use_unicode=True)


class Memoizer:

	def __init__(self, variables):
		self.models = []
		self.mapper = Mapper(variables)
		self.memory = Node()

	def insert(self,model):
		expr = model.orig
		iis, ffs = self.encode(expr)
		return self.insert_encoded(iis,model)

	def insert_encoded(self,iis, model):
		did_ins = self.memory.insert(iis, model)
		if did_ins:
			model.id = len(self.models)
			self.models.append(model)
		return did_ins

	def lookup(self,model):
		expr = model.orig
		iis, ffs = self.encode(expr)
		return self.memory.lookup(iis)

	def lookup_encoded(self,iis):
		return self.memory.lookup(iis)

	def encode(self,expr):
		# print expr
		iis = []
		ffs = []
		for i,e in enumerate(preorder_traversal(expr)):
			# print i, e.func
			ii, ff = self.mapper.get(e)
			iis = iis + ii
			if ff is not None:
				iis.append(len(ffs))
				ffs = ffs + ff
			# print "   ", ii, ff
		return iis, ffs

	def get_by_id(self, i):
		return self.models[i]


class Mapper:

	def __init__(self, variables):
		self.variables = variables
		self.coeffs = symbols("C C_0:16")
		self.map = {
			## the Leaf types

			# Symbol: self.map_symbol,
			# Constant 'C_#': 1
			# Float '#.#': 2
			# Time 'T': 3
			# System 'S_#': 4
			# Variable 'X_#': 5
			# Derivative 'dX_#': 6

			numbers.NegativeOne: 7,


			## the Node types
			
			# Mul: 8,  ++ num children
			# Add: 9,  ++ num children
			Pow: 10,
			# Div: 11,

			Abs: 12,
			sqrt: 13,
			log: 14,
			exp: 15,

			cos: 16,
			sin: 17,
			tan: 18,
			
		}
		# print self.variables
		# print self.coeffs

	def get(self,expr):
		e = expr.func
		
		if e is Mul:
			return [8,len(expr.args)], None
		if e is Add:
			return [9,len(expr.args)], None
		
		if e is Symbol:
			return self.map_symbol(expr), None

		if e is Integer or e is numbers.Zero or e is numbers.One:
			return [2, int(expr.evalf(0))], None

		if e is Float or e is numbers.Pi:
			return [2], [expr.evalf(8)]
		
		ii = [self.map[e]]
		return ii, None

	def map_symbol(self,expr):
		# print "SYMBOL: ", expr
		if expr in self.variables:
			idx = self.variables.index(expr)
			return [5,idx]
		if expr in self.coeffs:
			idx = self.coeffs.index(expr)
			return [1,idx-1]

		return [-2]



class Node:

	def __init__(self, key=0, value=None):
		self.map = {}
		self.key = key
		self.value = value


	def get_key(self):
		return self.key

	def get_value(self):
		return self.value

	def insert(self,iis, value):
		# print "  processing: ", iis
		# print "    ", self.key, self.map
		if len(iis) > 1:
			ii = iis[0]
			if ii not in self.map:
				# print "  new node for key: ", ii
				self.map[ii] = Node(key=ii)
			return self.map[ii].insert(iis[1:], value)
		if len(iis) == 1:
			ii = iis[0]
			if ii not in self.map:
				# print "  new node for key: ", ii
				self.map[ii] = Node(key=ii, value=value)
				return True
			else:
				return False
		return False

	def lookup(self,iis):
		if len(iis) > 1:
			ii = iis[0]
			if ii in self.map:
				return self.map[ii].lookup(iis[1:])
			else:
				return False, None
		if len(iis) == 1:
			ii = iis[0]
			if ii in self.map:
				return True, self.map[ii].get_value()
			else:
				return False, None
		return False, None

