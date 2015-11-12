import sympy
C = sympy.Symbol('C')
CS = [sympy.Symbol("C_"+str(i)) for i in range(128)]

from lmfit import Parameters

from pypge import evaluate

class Model:

	def __init__(self, expr, xs=None, cs=None, p_id=-2, reln="unknown"):
		# Identification please
		self.id = -2
		self.iter_id = -2

		# Family tree
		self.parent_id = p_id
		self.gen_relation = reln
		
		# Possible states for a model (in order)
		self.inited = False
		self.memoized = False
		self.algebrad = False ### not used yet, but should come here
		self.peeked = False
		self.peek_queued = False
		self.peek_popped = False
		self.evaluated = False
		self.queued = False
		self.popped = False
		self.expanded = False
		self.finalized = False

		# error accounting
		self.errored = False
		self.error = None
		self.exception = None

		# expression variations
		self.orig = expr
		# self.expr = expr
		self.pretty = None

		# vars, coeff, params
		self.xs = xs
		self.cs = cs
		self.params = None

		# initialization processes
		self.expr = sympy.expand(self.orig)
		self.rewrite_coeff()
		self.jac = [ sympy.diff(self.expr, c) for c in self.cs ]
		self.guess = [1.0 for c in self.cs]
		

		# fitness metrics
		self.sz = 0
		self.psz = 0
		self.jsz = 0
		self.jpsz = 0
		self.ncs = len(self.cs)

		self.peek_score = None
		self.peek_r2 = None
		self.peek_evar = None
		self.peek_aic = None
		self.peek_bic = None
		self.peek_redchi = None

		self.score = None
		self.r2 = None
		self.evar = None
		self.aic = None
		self.bic = None
		self.redchi = None

		self.improve_score = None
		self.improve_r2 = None
		self.improve_evar = None
		self.improve_aic = None
		self.improve_bic = None
		self.improve_redchi = None

		self.fitness = None

		self.fit_result = None
		self.peek_nfev = 0
		self.eval_nfev = 0
		self.total_fev = 0

		# all done, so we be inited
		self.inited = True


	def __hash__(self):
		return self.id

	def __cmp__(self, other):
		return cmp(self.id, other.id)

	def __str__(self):
		if self.pretty is None:
			self.pretty_expr()
		fs = "{:5d}  {:5d}  {:5d}    {:2d}   {:2d}   {:2d}   {:2d}  {:15.6f}  {:10.6f}  {:10.6f}  {:15.6f}  {:15.6f}  {:15.6f} |  {:s}"
		return fs.format(self.id, self.iter_id, self.parent_id, self.size(), self.psz, self.jsz, self.jpsz,
			self.score,self.r2,self.evar,self.aic,self.bic,self.redchi,
			self.pretty)

	def print_columns(self):
		cols =  "      id    iid    pid    sz  psz  jsz  jpsz          "
		cols += "error         r2     expld_vari          aic              bic            redchi   |      theModel"
		return cols

	def print_long_columns(self):
		cols =  "      id    iid    pid    sz  psz  jsz  jpsz          "
		cols += "error         r2     expld_vari          aic              bic            redchi   |        "
		cols += "I_error      I_r2    I_expld_vari        I_aic            I_bic          I_redchi        theModel"
		return cols

	def print_long(self):
		if self.pretty is None:
			self.pretty_expr()
		fs = "{:5d}  {:5d}  {:5d}    {:2d}   {:2d}   {:2d}   {:2d}  {:15.6f}  {:10.6f}  {:10.6f}  {:15.6f}  {:15.6f}  {:15.6f} | {:15.6f}  {:10.6f}  {:10.6f}  {:15.6f}  {:15.6f}  {:15.6f}    {:s}"
		return fs.format(self.id, self.iter_id, self.parent_id, self.size(), self.psz, self.jsz, self.jpsz,
			self.score,self.r2,self.evar,self.aic,self.bic,self.redchi,
			self.improve_score,self.improve_r2,self.improve_evar,self.improve_aic,self.improve_bic,self.improve_redchi,
			self.pretty)

	def print_csv(self):
		if self.pretty is None:
			self.pretty_expr()
		fs = "{:5d},  {:5d},  {:5d},  {:2d},  {:2d},  {:2d},  {:2d},  {:15.6f},  {:10.6f},  {:10.6f},  {:15.6f},  {:15.6f},  {:15.6f},  {:s}"
		return fs.format(self.id, self.iter_id, self.parent_id, self.size(), self.psz, self.jsz, self.jpsz,
			self.score,self.r2,self.evar,self.aic,self.bic,self.redchi,
			self.pretty)

	def print_csv_columns(self):
		cols =  "   id,    iid,    pid,  sz, psz, jsz, jpsz,         "
		cols += "error,        r2,       evar,          aic,             bic,          redchi,         theModel"
		return cols

	def pretty_expr(self, float_format="%.4e"):
		c_sub = [ (str(c), float_format % self.params[str(c)].value) for c in self.cs ]
		self.pretty = str( self.expr.subs(c_sub) )
		return self.pretty

	def size(self):
		if self.sz == 0:
			self.sz, self.psz = self.calc_tree_size()
			self.jsz, self.jpsz = self.calc_jac_size()
		return self.sz

	def calc_tree_size(self):
		i = 0
		p = 0
		for e in sympy.preorder_traversal(self.expr):
			if e.is_Integer:
				i += int(abs(e))
				continue
			if e.is_Function:
				p += 2  # add an extra penalty
			i+=1
		return i, i+p

	def calc_jac_size(self):
		i,p = 0,0
		for jac in self.jac:
			for e in sympy.preorder_traversal(jac):
				if e.is_Integer:
					i += int(abs(e))
					continue
				if e.is_Function:
					p += 2  # add an extra penalty
				i+=1
		return i, i+p

	def get_coeff(self):
		if self.coeff is not None:
			return self.coeff
		else:
			self.coeff = self.rewrite_coeff()

	def rewrite_coeff(self):
		if self.cs is not None:
			c_subs = [ (c, C) for c in CS]
			self.orig = self.expr.subs(c_subs)

		expr, ii = self._rewrite_coeff_helper(self.orig, 0)
		self.expr = expr
		self.cs = CS[:ii]

		params = Parameters()
		for i,c in enumerate(self.cs):
			params.add('C_'+str(i), value=1.0)
		self.params = params

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

	def predict(self, model, xs, x_pts):
		return evaluate.Eval(model, xs, x_pts)

