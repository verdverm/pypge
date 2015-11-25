import sympy

from scipy.integrate import odeint

import numpy as np
np.random.seed(23)

import pandas as pd

T = sympy.Symbol("T")

import pprint
pp = pprint.PrettyPrinter(indent=4)



def gen(prob_params, **kwargs):
	prob_params = prep_params(prob_params, **kwargs)

	pp.pprint(prob_params)

	eqns = []
	for estr in prob_params['eqn_strs']:
		e = sympy.sympify(estr)
		print e
		# if we have extra substitutions, do that now
		# (generally used for shared sub-expressions, for readability)
		if 'eqn_subs' in prob_params:
			esubs = prob_params['eqn_subs']
			for old,new in esubs.items():
				e = e.subs(old,new)
		# print e, "\n"
		eqns.append(e)

	time_pts = np.arange(0., prob_params['time_end'], prob_params['time_step'])
	win_sz = len(time_pts)/10
	if win_sz % 2 == 0:
		win_sz += 1

	xs_pure = gen_pts(eqns, prob_params['xs'], prob_params['params'], prob_params['init_conds'], time_pts)
	xs_pure = xs_pure.T
	xs_pts = []
	for data in xs_pure:
		dpts = data
		if prob_params['noise_type'] == "var":
			var = np.var(data) * prob_params['noise']**2
			dpts = data + np.random.normal(0, var, len(data))
		elif prob_params['noise_type'] == "percent":
			dpts = data * np.random.normal(1, prob_params['noise'], len(data))
		
		xs_pts.append(dpts)
	xs_pts = np.array(xs_pts)

	prob_params['eqns'] = eqns
	prob_params['time_pts'] = time_pts
	prob_params['xs_pure'] = xs_pure
	prob_params['xs_pts'] = xs_pts

	return prob_params

def prep_params(prob_params, **kwargs):
	prob_params['xs'] = sympy.symbols(prob_params['xs_str'])
	prob_params['dxs_str'] = ["D_"+x for x in prob_params['xs_str']]
	prob_params['dxs'] = sympy.symbols(prob_params['dxs_str'])
	prob_params['noise_type'] = "percent"

	# override locals with kwargs
	for key, value in kwargs.items():
		if key == "params":
			for param,val in value.items():
				prob_params['params'][param] = val
		else:
			prob_params[key] = value

	# pp.pprint(prob_params)
	return prob_params

def gen_pts(eqns, xs, params, init_conds, time_pts):
	es = [ eqn.subs(params) for eqn in eqns ]
	fs = [ sympy.lambdify([T] + xs, eqn, "numpy") for eqn in es ]

	def evalr(curr_xs_vals, t):
		derivs = [ f(t, *curr_xs_vals) for f in fs ]
		# print "\nderivs:\n", derivs
		return derivs

	iconds = [val for k,val in init_conds.items()]

	# print "\niconds:\n", iconds

	pts = odeint(evalr, iconds, time_pts)
	return pts









def BacResp(**kwargs):
	this = {
		'name': "BacResp",
		'xs_str': ["x", "y"],
		'params': {
			'A': 20.0,
			'B': 10.0,
			'k': 2.1,
		},
		'eqn_strs': [
			"A + B - x - (k**2*x*y)/(k**2+x**2)",  # dx
			"A - (k**2*x*y)/(k**2+x**2)"  		# dy
		],
		'init_conds': {
			"x": 10.0,
			"y": 3.0
		},
		'time_end': 100.0,
		'time_step': 1.0,
		'noise': 0.1
	}
	return gen(this,**kwargs)


def BarMags(**kwargs):
	this = {
		'name': "BarMags",
		'xs_str': ["X", "Y"],
		'params': {
			'A': 0.5,
			'B': 1.0,
			'C': 0.5,
			'D': 1.0,
		},
		'eqn_strs': [
			"A*sin(X-Y)-B*sin(X)",               # dX
			"C*sin(Y-X)-D*sin(Y)"  # dY
		],
		'init_conds': {
			"X": 1.5,
			"Y": 3.0
		},
		'time_end': 20.0,
		'time_step': 0.01,
		'noise': 0.1
	}
	return gen(this,**kwargs)


def Glider(**kwargs):
	this = {
		'name': "Glider",
		'xs_str': ["v", "A"],
		'params': {},
		'eqn_strs': [
			"-0.05*v**2 - sin(A)",  # dv
			"v - cos(A)/v"  		# dA
		],
		'init_conds': {
			"v": 5.0,
			"A": 0.5
		},
		'time_end': 50.0,
		'time_step': 0.01,
		'noise': 0.1
	}
	return gen(this,**kwargs)


def Ecoli(**kwargs):
	this = {
		'name': "Ecoli",
		'xs_str': ["G", "A", "L"],
		'params': {},
		'eqn_strs': [
			"L**2 / (1 + L**2) - 0.01*G + 0.001",               # dA
			"G * ( L/(1+L) - A/(1+A) )",               # dA
			"-G*L / (1+L)"  # dL
		],
		'init_conds': {
			"G": 1.0,
			"A": 0.0,
			"L": 0.0
		},
		'time_end': 10.0,
		'time_step': 0.1,
		'noise': 0.2
	}
	return gen(this,**kwargs)




def Lorenz(**kwargs):
	this = {
		'name': "Lorenz",
		'xs_str': ["x", "y", "z"],
		'params': {
			"A": 10.0,  
			"B": 28.0,  
			"C": 8.0/3.0,  
		},
		'eqn_strs': [
			"A*(y-x)",       # dx
			"x*(B-z) - y",    # dy
			"x*y - C*z"   # dz
		],
		'init_conds': {
			"x": 1.0,
			"y": 1.0,
			"z": 1.0,
		},
		'time_end': 50.0,
		'time_step': 0.01,
		'noise': 0.1
	}
	return gen(this,**kwargs)




def ShearFlow(**kwargs):
	this = {
		'name': "ShearFlow",
		'xs_str': ["A", "B"],
		'params': {},
		'eqn_strs': [
			"cos(B)/sin(B)*cos(A)",               # dA
			"(cos(B)**2 - 0.1*sin(B)**2) * sin(A)"  # dB
		],
		'init_conds': {
			"A": 1.0,
			"B": 1.57
		},
		'time_end': 10.0,
		'time_step': 0.01,
		'noise': 0.33
	}
	return gen(this,**kwargs)




def vanDerPol(**kwargs):
	this = {
		'name': "vanDerPol",
		'xs_str': ["x", "y"],
		'params': {
			'U': 3.0,
		},
		'eqn_strs': [
			"U * (x - (1.0/3.0)*x**3 - y)",               # dx
			"(1.0/U)*x"  # dy
		],
		'init_conds': {
			"x": 1.0,
			"y": 2.0
		},
		'time_end': 50.0,
		'time_step': 0.1,
		'noise': 0.1
	}
	return gen(this,**kwargs)


def PredPreyInt(**kwargs):
	this = {
		'name': "PredPreyInt",
		'xs_str': ["x", "y"],
		'params': {},
		'eqn_strs': [
			"x * (4 - x - y/(1+x))",               # dx
			"y* ( x/(1+x) - 0.075*y)"  # dy
		],
		'init_conds': {
			"x": 20.0,
			"y": 4.0
		},
		'time_end': 10.0,
		'time_step': 0.01,
		'noise': 0.1
	}
	return gen(this,**kwargs)


def PredPreyFrac(**kwargs):
	this = {
		'name': "PredPreyFrac",
		'xs_str': ["x", "y"],
		'params': {},
		'eqn_strs': [
			"-0.2*x + 0.001*x*y",               # dx
			"0.1*y - 0.001*x*y"  # dy
		],
		'init_conds': {
			"x": 20.0,
			"y": 200.0
		},
		'time_end': 500.0,
		'time_step': 0.1,
		'noise': 0.1
	}
	return gen(this,**kwargs)




def LotkaVolterra(**kwargs):
	this = {
		'name': "LotkaVolterra",
		'xs_str': ["x", "y"],
		'params': {
			'A': 1.5,
			'B': 1.0,
			'C': 3.0,
			'D': 1.0,
		},
		'eqn_strs': [
			"A*x - B*x*y",               # dx
			"-C*y + D*x*y"  # dy
		],
		'init_conds': {
			"x": 10.0,
			"y": 5.0
		},
		'time_end': 20.0,
		'time_step': 0.01,
		'noise': 0.1
	}
	return gen(this,**kwargs)





def SimplePendulum(**kwargs):
	this = {
		'name': "SimplePendulum",
		'xs_str': ["A", "V"],
		'params': {
			"M": 1.0,  # Mass of pendulum
			"R": 1.0   # Length of rod
		},
		'eqn_strs': [
			"V",               # dA
			"(-9.8/R)*sin(A)"  # dV
		],
		'init_conds': {
			"A": 2.0,
			"V": 2.0
		},
		'time_end': 10.0,
		'time_step': 0.01,
		'noise': 0.01
	}
	return gen(this,**kwargs)

def ChaoticPendulum(**kwargs):
	this = {
		'name': "ChaoticPendulum",
		'xs_str': ["A", "V"],
		'params': {
			"M": 1.0,   # Mass of pendulum
			"R": 1.0,   # Length of rod
			"a": 5.0,   # Amplitude of driving force
			"b": 0.05,   # Damping (friction) constant
			"k": 0.65,  # constant related to frequency of driving force
			"g": 9.81   # Gravity constant (let's got to the moon! [1.62])
		},
		'eqn_strs': [
			"V",                 # dO
			# "sin(A) + (-b*V + a*cos(k*T) )"  # dV
			"(-g/R)*sin(A) + (-b*V + a*cos(k*T) ) / (M*R**2)"  # dV
		],
		'init_conds': {
			"A": 0.0,
			"V": 0.0
		},
		'time_end': 100.0,
		'time_step': 0.025,
		'noise': 0.01
	}
	return gen(this, **kwargs)







def YeastMetabolism(**kwargs):
	this = {
		'name': 'YeastMetabolism',
		'xs_str': ["s1", "s2", "s3", "s4", "n2", "a3", "s5", "a2", "n1"],
		'params': {
			"J0": 3,           # mM/min
			"k1": 100.0,       # /mM*min
			"k2": 6.0,         # /mM*min
			"k3": 16.0,        # /mM*min
			"k4": 100.0,       # /mM*min
			"k5": 1.28,        # /min
			"k6": 12.0,        # /mM*min
			"k" : 1.3,         # /min
			"K" : 13.0,        # /min
			"q" : 4.0,
			"K1": 0.52,        # mM
			"N" : 1.0,         # mM
			"A" : 4.0,         # mM
			"P" : 0.1,
		},
		'eqn_subs': {
			'Ja' :  "K*(s4-s5)",
			"v1" :  "k1*s1*a3/fA3",  
			"fA3":  "1.0+(a3/K1)^q",  # meta sub, must be ordered properly
			"v2" :  "k2*s2*n1",
			"v3" :  "k3*s3*a2",
			"v4" :  "k4*s4*n2",
			"v5" :  "k5*a3",
			"v6" :  "k6*s2*n2",
			"v7" :  "k*s5"
		},
		'eqn_strs': {
			"J0 - v1",					#s1
			"2.0*v1 - v2 - v6",			#s2
			"v2 - v3",					#s3
			"v3 - v4 - Ja",				#s4
			"v2 - v4 - v6",				#n2
			"-2.0*v1 + 2.0*v3 - v5",	#a3
			"P*Ja - v7",				#s5
			"a2",						#a2
			"n1",						#n1
		},
		'init_conds': {
			"s1": 5.8,
			"s2": 0.9,
			"s3": 0.2,
			"s4": 0.2,
			"n2": 0.1,
			"a3": 2.4,
			"s5": 0.1,
			"a2": 4.0 - 2.4,			# A - a3
			"n1": 1.0 - 0.1				# N - n2
		},
		'time_end': 10.0,
		'time_step': 0.01,
		'noise': 0.001
	}
	return gen(this, **kwargs)

