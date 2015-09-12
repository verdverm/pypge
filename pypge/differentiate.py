from __future__ import division
from sympy import *


# print task

eSubs = []
dSubs = []

def buildDeps(deps):

	del eSubs[:]
	del dSubs[:]

	# print deps

	tuples = deps.split('),')
	for t in tuples:
		t = str(t)
		# print "  ", t
		a,b = t.strip().strip('(').strip(')').split(',')
		a,b = a.strip(),b.strip()
		# a, b = str(t[0]), str(t[1])

		sa, sb = symbols(a), symbols(b)
		f = Function(a)(sb)
		df = diff(f,sb,1)

		eSubs.append( [a,b,a+'('+b+')'] )
		dSubs.append( (df,'d'+a+'d'+b) )
		dSubs.append( (f,sa) )

	# print eSubs
	# print dSubs



def do_diff(task):
	eqnStr = task['Eqn'].strip()

	depStr= task['Deps']
	buildDeps(depStr)

	wrts = task['Wrt'].split()

	task["results"]=[]

	for wrt in wrts:
		# replace vars for dependent function version
		tmp = eqnStr
		# print wrt, tmp
		for sub in eSubs:
			if sub[1] == wrt:
				# print sub[0]
				tmp = tmp.replace(sub[0],sub[2])
		# print tmp

		eq = sympify(tmp)


		d_eq = diff(eq, symbols(wrt), 1)
		# print d_eq

		# substitute to look better
		tmp_eq = d_eq
		for sub in dSubs:
			tmp_eq = tmp_eq.subs(sub[0],sub[1])

		task["results"].append(str(tmp_eq))



def do_coeff(task):
	eqnStr = task['Eqn'].strip()
	eq = sympify(eqnStr)

	task["results"]=[]

	coeffs = task['Coeff'].split()

	for c in coeffs:
		d_eq = diff(eq, symbols(c), 1)
		task['result'].append(str(d_eq))
