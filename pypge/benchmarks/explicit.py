import sympy
import numpy as np
import pandas as pd
np.random.seed(23)

import pprint
pp = pprint.PrettyPrinter(indent=4)


x = sympy.Symbol('x')
y = sympy.Symbol('y')
z = sympy.Symbol('z')
v = sympy.Symbol('v')
w = sympy.Symbol('w')

def gen(prob_params, **kwargs):

	prob_params = prep_params(prob_params, **kwargs)
	pp.pprint(prob_params)

	eqn = sympy.sympify(prob_params['eqn_str'])
	xpts = gen_xpts(prob_params['xs_params'], prob_params['npts'])
	ypure = sympy.lambdify(prob_params['xs'],eqn,"numpy")(*xpts)

	ypts = ypure
	if prob_params['noise_type'] == "var":
		yvar = np.var(ypure) * prob_params['noise']**2
		ypts = ypure + np.random.normal(0, yvar, len(ypure))
	elif prob_params['noise_type'] == "percent":
		ypts = ypure * np.random.normal(1, prob_params['noise'], len(ypure))

	prob_params['eqn'] = eqn
	prob_params['xpts'] = xpts
	prob_params['ypure'] = ypure
	prob_params['ypts'] = ypts

	df = pd.DataFrame(xpts.T,columns=prob_params['xs_str'])
	df['pure'] = ypure
	df['target'] = ypts
	prob_params['df'] = df

	return prob_params


def prep_params(prob_params, **kwargs):
	prob_params['xs'] = sympy.symbols(prob_params['xs_str'])
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


def gen_xpts(xs_params, npts):
	pts = []
	for xp in xs_params:
		xs = np.random.uniform(low=xp[0],high=xp[1],size=npts)
		pts.append(xs)
	xpts = np.array(pts)
	return xpts



def Explicit_1D(**kwargs):
	this = {
		'name': "line",
		'xs_str': ["x"],
		'eqn_str': "x",
		'xs_params': [ (-4.0,4.0) ],
		'npts': 200,
		'noise': 0.1
	}
	return gen(this,**kwargs)


# 1 input: x
def Koza_01(**kwargs):
	this = {
		'name': "Koza_01",
		'xs_str': ["x"],
		'eqn_str': "x**4 + x**3 + x**2 + x",
		'xs_params': [ (-4.0,4.0) ],
		'npts': 200,
		'noise': 5.0
	}
	return gen(this,**kwargs)

def Koza_02(**kwargs):
	this = {
		'name': "Koza_02",
		'xs_str': ["x"],
		'eqn_str': "x**5 - 2*x**3 + x",
		'xs_params': [ (-6.0,6.0) ],
		'npts': 200,
		'noise': 10.0
	}
	return gen(this,**kwargs)

def Koza_03(**kwargs):
	this = {
		'name': "Koza_03",
		'xs_str': ["x"],
		'eqn_str': "x**6 - 2*x**4 + x**2",
		'xs_params': [ (-4.0,4.0) ],
		'npts': 200,
		'noise': 10.0
	}
	return gen(this,**kwargs)

def Lipson_01(**kwargs):
	this = {
		'name': "Lipson_01",
		'xs_str': ["x"],
		'eqn_str': "1.5 * x**2 - x**3",
		'xs_params': [ (-5.0,5.0) ],
		'npts': 200,
		'noise': 3.0
	}
	return gen(this,**kwargs)

def Lipson_02(**kwargs):
	this = {
		'name': "Lipson_02",
		'xs_str': ["x"],
		'eqn_str': "0.1*exp(Abs(x)) * sin(x)",
		'xs_params': [ (-9.7,9.7) ],
		'npts': 500,
		'noise': 20.0
	}
	return gen(this,**kwargs)

def Lipson_03(**kwargs):
	this = {
		'name': "Lipson_03",
		'xs_str': ["x"],
		'eqn_str': "x**2 * exp(sin(x)) + x + sin(pi/4.0 - x**3)",
		'xs_params': [ (-14.0,14.0) ],
		'npts': 500,
		'noise': 5.0
	}
	return gen(this,**kwargs)


def Nguyen_01(**kwargs):
	this = {
		'name': "Nguyen_01",
		'xs_str': ["x"],
		'eqn_str': "x**3 + x**2 + x",
		'xs_params': [ (-5.0,5.0) ],
		'npts': 200,
		'noise': 3.0
	}
	return gen(this,**kwargs)

def Nguyen_02(**kwargs):
	this = {
		'name': "Nguyen_02",
		'xs_str': ["x"],
		'eqn_str': "x**4 + x**3 + x**2 + x",
		'xs_params': [ (-5.0,5.0) ],
		'npts': 200,
		'noise': 5.0
	}
	return gen(this,**kwargs)

def Nguyen_03(**kwargs):
	this = {
		'name': "Nguyen_03",
		'xs_str': ["x"],
		'eqn_str':  "x**5 + x**4 + x**3 + x**2 + x",
		'xs_params': [ (-5.0,5.0) ],
		'npts': 200,
		'noise': 10.0
	}
	return gen(this,**kwargs)

def Nguyen_04(**kwargs):
	this = {
		'name': "Nguyen_04",
		'xs_str': ["x"],
		# 'eqn_str':  "0.04*x**6 + 0.2*x**5 - 0.4*x**4 + 0.8*x**3 + 3.2*x**2 + x",
		'eqn_str':  "x**6 + x**5 + x**4 + x**3 + x**2 + x",
		'xs_params': [ (-5.0,5.0) ],
		'npts': 200,
		'noise': 10.0
	}
	return gen(this,**kwargs)

def Nguyen_05(**kwargs):
	this = {
		'name': "Nguyen_05",
		'xs_str': ["x"],
		'eqn_str': "3.3*sin(x**2)*cos(x) - 1",
		'xs_params': [ (-5.0,5.0) ],
		'npts': 1000,
		'noise': 0.025
	}
	return gen(this,**kwargs)

def Nguyen_06(**kwargs):
	this = {
		'name': "Nguyen_06",
		'xs_str': ["x"],
		'eqn_str': "3.2*sin(x) + 1.4*sin(x + x**2)",
		'xs_params': [ (-5.0,5.0) ],
		'npts': 1000,
		'noise': 0.1
	}
	return gen(this,**kwargs)

def Nguyen_07(**kwargs):
	this = {
		'name': "Nguyen_07",
		'xs_str': ["x"],
		'eqn_str': "ln(x+1) + ln(x**2 + 1)",
		'xs_params': [ (0.0,1000.0) ],
		'npts': 1000,
		'noise': 1.0
	}
	return gen(this,**kwargs)

def Nguyen_08(**kwargs):
	this = {
		'name': "Nguyen_08",
		'xs_str': ["x"],
		'eqn_str': "sqrt(x)",
		'xs_params': [ (0.0001,10000.0) ],
		'npts': 1000,
		'noise': 1.0
	}
	return gen(this,**kwargs)



# 2 inputs: x,y
def Nguyen_09(**kwargs):
	this = {
		'name': "Nguyen_09",
		'xs_str': ["x", "y"],
		'eqn_str': "sin(x) + sin(y**2)",
		'xs_params': [ (-10.0,10.0), (-6.0,6.0) ],
		'npts': 2000,
		'noise': 0.1
	}
	return gen(this,**kwargs)

def Nguyen_10(**kwargs):
	this = {
		'name': "Nguyen_10",
		'xs_str': ["x", "y"],
		'eqn_str': "2*sin(x)*cos(y)",
		'xs_params': [ (-7.0,7.0), (-7.0,7.0) ],
		'npts': 2000,
		'noise': 0.1
	}
	return gen(this,**kwargs)

def Nguyen_11(**kwargs):
	this = {
		'name': "Nguyen_11",
		'xs_str': ["x", "y"],
		'eqn_str': "x**y",
		'xs_params': [ (0.0,4.0), (1.0,4.0) ],
		'npts': 2000,
		'noise': 1.0
	}
	return gen(this,**kwargs)

def Nguyen_12(**kwargs):
	this = {
		'name': "Nguyen_12",
		'xs_str': ["x", "y"],
		'eqn_str': "0.09*x**4 + 0.3*x**3 + 0.1*y**2 - y",
		'xs_params': [ (-8.0,8.0), (-8.0,8.0) ],
		'npts': 2000,
		'noise': 5.0
	}
	return gen(this,**kwargs)




# 5 inputs: x,y,z,v,w
def Korns_01(**kwargs):
	this = {
		'name': "Korns_01",
		'xs_str': ["x", "y", "z", "v", "w"],
		'eqn_str': "1.57 + 24.3*v",
		'xs_params': [ 
			(-5.0,5.0),
			(-5.0,5.0),
			(-5.0,5.0),
			(-5.0,5.0),
			(-5.0,5.0)
		],
		'npts': 10000,
		'noise': 1.0
	}
	return gen(this,**kwargs)

def Korns_02(**kwargs):
	this = {
		'name': "Korns_02",
		'xs_str': ["x", "y", "z", "v", "w"],
		'eqn_str': "0.23 + 14.2*(v+y)/(3*w)",
		'xs_params': [ 
			(-0.4, 0.4),
			(-0.4, 0.4),
			(-0.4, 0.4),
			(-0.4, 0.4),
			(-0.4, 0.4)
		],
		'npts': 10000,
		'noise': 1.0
	}
	return gen(this,**kwargs)

def Korns_03(**kwargs):
	this = {
		'name': "Korns_03",
		'xs_str': ["x", "y", "z", "v", "w"],
		'eqn_str': "-5.41 + 4.9*(v-x+y/w)/(3*w)",
		'xs_params': [ 
			(-0.4, 0.4),
			(-0.4, 0.4),
			(-0.4, 0.4),
			(-0.4, 0.4),
			(-0.4, 0.4)
		],
		'npts': 10000,
		'noise': 1.0
	}
	return gen(this,**kwargs)

def Korns_04(**kwargs):
	this = {
		'name': "Korns_04",
		'xs_str': ["x", "y", "z", "v", "w"],
		'eqn_str': "-2.3 + 0.13*sin(z)",
		'xs_params': [ 
			(-10.0,10.0),
			(-10.0,10.0),
			(-10.0,10.0),
			(-10.0,10.0),
			(-10.0,10.0)
		],
		'npts': 10000,
		'noise': 0.0025
	}
	return gen(this,**kwargs)

def Korns_05(**kwargs):
	this = {
		'name': "Korns_05",
		'xs_str': ["x", "y", "z", "v", "w"],
		'eqn_str': "3 + 2.13*ln(w)",
		'xs_params': [ 
			(0.0001,5000.0),
			(0.0001,5000.0),
			(0.0001,5000.0),
			(0.0001,5000.0),
			(0.0001,5000.0)
		],
		'npts': 1000,
		'noise': 0.1
	}
	return gen(this,**kwargs)

def Korns_06(**kwargs):
	this = {
		'name': "Korns_06",
		'xs_str': ["x", "y", "z", "v", "w"],
		'eqn_str': "1.3 + 0.13*sqrt(x)",
		'xs_params': [ 
			(0.0001,5000.0),
			(0.0001,5000.0),
			(0.0001,5000.0),
			(0.0001,5000.0),
			(0.0001,5000.0)
		],
		'npts': 1000,
		'noise': 0.1
	}
	return gen(this,**kwargs)

def Korns_07(**kwargs):
	this = {
		'name': "Korns_07",
		'xs_str': ["x", "y", "z", "v", "w"],
		'eqn_str': "213.80940889*(1 - exp(-0.54723748542*x))",
		'xs_params': [ 
			(0.0001,10.0),
			(0.0001,10.0),
			(0.0001,10.0),
			(0.0001,10.0),
			(0.0001,10.0)
		],
		'npts': 1000,
		'noise': 1.0
	}
	return gen(this,**kwargs)

def Korns_08(**kwargs):
	this = {
		'name': "Korns_08",
		'xs_str': ["x", "y", "z", "v", "w"],
		'eqn_str': "6.87 + 11*sqrt(7.23*x*v*w)",
		'xs_params': [ 
			(0.0001,10.0),
			(0.0001,10.0),
			(0.0001,10.0),
			(0.0001,10.0),
			(0.0001,10.0)
		],
		'npts': 10000,
		'noise': 1.0
	}
	return gen(this,**kwargs)

def Korns_09(**kwargs):
	this = {
		'name': "Korns_09",
		'xs_str': ["x", "y", "z", "v", "w"],
		'eqn_str': "(sqrt(x)/ln(y)) * (exp(z) / v**2)",
		'xs_params': [ 
			(0.1,4.0),
			(0.1,4.0),
			(0.1,4.0),
			(0.1,4.0),
			(0.1,4.0)
		],
		'npts': 10000,
		'noise': 1.0
	}
	return gen(this,**kwargs)

def Korns_10(**kwargs):
	this = {
		'name': "Korns_10",
		'xs_str': ["x", "y", "z", "v", "w"],
		'eqn_str': "0.81 + 24.3*(2*y+3*z**2)/(4*(v)**3+5*(w)**4)",
		'xs_params': [ 
			(-1.0,1.0),
			(-1.0,1.0),
			(-1.0,1.0),
			(-1.0,1.0),
			(-1.0,1.0)
		],
		'npts': 10000,
		'noise': 1.0
	}
	return gen(this,**kwargs)

def Korns_11(**kwargs):
	this = {
		'name': "Korns_11",
		'xs_str': ["x", "y", "z", "v", "w"],
		'eqn_str': "6.87 + 11*cos(7.23*x**3)",
		'xs_params': [ 
			(-1.47,1.47),
			(-1.47,1.47),
			(-1.47,1.47),
			(-1.47,1.47),
			(-1.47,1.47)
		],
		'npts': 10000,
		'noise': 1.0
	}
	return gen(this,**kwargs)

def Korns_12(**kwargs):
	this = {
		'name': "Korns_12",
		'xs_str': ["x", "y", "z", "v", "w"],
		'eqn_str': "2 - 2.1*cos(9.8*x)*sin(1.3*w)",
		'xs_params': [ 
			(-1.47,1.47),
			(-1.47,1.47),
			(-1.47,1.47),
			(-1.47,1.47),
			(-1.47,1.47)
		],
		'npts': 10000,
		'noise': 0.1
	}
	return gen(this,**kwargs)

def Korns_13(**kwargs):
	this = {
		'name': "Korns_13",
		'xs_str': ["x", "y", "z", "v", "w"],
		'eqn_str': "32 - 3*(tan(x)*tan(z))/(tan(y)*tan(v))",
		'xs_params': [ 
			(-3.14,3.14),
			(-3.14,3.14),
			(-3.14,3.14),
			(-3.14,3.14),
			(-3.14,3.14)
		],
		'npts': 10000,
		'noise': 1.0
	}
	return gen(this,**kwargs)

def Korns_14(**kwargs):
	this = {
		'name': "Korns_14",
		'xs_str': ["x", "y", "z", "v", "w"],
		'eqn_str': "22 - 4.2*(cos(x)-tan(y))*(tanh(z)/sin(v))",
		'xs_params': [ 
			(-3.14,3.14),
			(-3.14,3.14),
			(-3.14,3.14),
			(-3.14,3.14),
			(-3.14,3.14)
		],
		'npts': 10000,
		'noise': 1.0
	}
	return gen(this,**kwargs)

def Korns_15(**kwargs):
	this = {
		'name': "Korns_15",
		'xs_str': ["x", "y", "z", "v", "w"],
		'eqn_str': "12 - 6*(tan(x)/exp(y))*(ln(z)-tan(v))",
		'xs_params': [ 
			(-3.14,3.14),
			(-3.14,3.14),
			(-3.14,3.14),
			(-3.14,3.14),
			(-3.14,3.14)
		],
		'npts': 10000,
		'noise': 1.0
	}
	return gen(this,**kwargs)








# 1. filip
# 1. longley
# 1. norris
# 1. pontius
# 1. wampler1
# 1. wampler2
# 1. wampler3
# 1. wampler4
# 1. wampler5

# 1. bennett5.tsv
# 1. boxbod.tsv
# 1. chwirut1.tsv
# 1. chwirut2.tsv
# 1. danwood.tsv
# 1. eckerle4.tsv
# 1. gauss1.tsv
# 1. gauss2.tsv
# 1. gauss3.tsv
# 1. hahn1.tsv
# 1. kirby2.tsv
# 1. lanczos1.tsv
# 1. lanczos2.tsv
# 1. lanczos3.tsv
# 1. mgh09.tsv
# 1. mgh10.tsv
# 1. mgh17.tsv
# 1. misrala.tsv
# 1. misralb.tsv
# 1. misralc.tsv
# 1. misrald.tsv
# 1. nelson.tsv
# 1. rat42.tsv
# 1. rat43.tsv
# 1. roszman1.tsv
# 1. thurber.tsv
