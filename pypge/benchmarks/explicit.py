import sympy
import numpy as np
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
	ypts = ypure + np.random.normal(0, prob_params['noise'], len(ypure))

	prob_params['eqn'] = eqn
	prob_params['xpts'] = xpts
	prob_params['ypure'] = ypure
	prob_params['ypts'] = ypts

	return prob_params


def prep_params(prob_params, **kwargs):
	prob_params['xs'] = sympy.symbols(prob_params['xs_str'])

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
		'name': "Koza_01",
		'xs_str': ["x"],
		'eqn_str': "x**4 + x**3 + x**2 + x",
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
		'xs_params': [ (-4.0,4.0) ],
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
		'eqn_str': "exp(Abs(x)) * sin(x)",
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
		'eqn_str': "sin(x**2)*cos(x) - 1",
		'xs_params': [ (-5.0,5.0) ],
		'npts': 1000,
		'noise': 0.025
	}
	return gen(this,**kwargs)

def Nguyen_06(**kwargs):
	this = {
		'name': "Nguyen_06",
		'xs_str': ["x"],
		'eqn_str': "sin(x) + sin(x + x**2)",
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
		'npts': 1000,
		'noise': 1.0
	}
	return gen(this,**kwargs)

def Nguyen_10(**kwargs):
	this = {
		'name': "Nguyen_10",
		'xs_str': ["x", "y"],
		'eqn_str': "2*sin(x)*cos(y)",
		'xs_params': [ (-7.0,7.0), (-7.0,7.0) ],
		'npts': 1000,
		'noise': 1.0
	}
	return gen(this,**kwargs)

def Nguyen_11(**kwargs):
	this = {
		'name': "Nguyen_11",
		'xs_str': ["x", "y"],
		'eqn_str': "x**y",
		'xs_params': [ (0.0,4.0), (1.0,4.0) ],
		'npts': 1000,
		'noise': 1.0
	}
	return gen(this,**kwargs)

def Nguyen_12(**kwargs):
	this = {
		'name': "Nguyen_12",
		'xs_str': ["x", "y"],
		'eqn_str': "x**4 - x**3 + 0.5*y**2 - y",
		'xs_params': [ (-8.0,8.0), (-8.0,8.0) ],
		'npts': 1000,
		'noise': 1.0
	}
	return gen(this,**kwargs)


def Pagie_01(noise):
	this = {
		'name': "Pagie_01",
		'xs_str': ["x", "y"],
		'eqn_str': "1 / (1 + x**-4) + 1 / (1 + y**-4)",
		'xs_params': [ (0.0001,3.0), (0.0001,3.0) ],
		'npts': 1000,
		'noise': 1.0
	}
	return gen(this,**kwargs)


# 5 inputs: x,y,z,v,w
def Korns_01(xs_params,npts,noise):
	eqn_str = "1.57 + 24.3*v"
	xs = [x,y,z,v,w]
	return gen("Korns_01", eqn_str,xs,xs_params,npts,noise)

def Korns_02(xs_params,npts,noise):
	eqn_str = "0.23 + 14.2*(v+y)/3w"
	xs = [x,y,z,v,w]
	return gen("Korns_02", eqn_str,xs,xs_params,npts,noise)

def Korns_03(xs_params,npts,noise):
	eqn_str = "-5.41 + 4.9*(v-x+y/w)/3w"
	xs = [x,y,z,v,w]
	return gen("Korns_03", eqn_str,xs,xs_params,npts,noise)

def Korns_04(xs_params,npts,noise):
	eqn_str = "-2.3 + 0.13sin(z)"
	xs = [x,y,z,v,w]
	return gen("Korns_04", eqn_str,xs,xs_params,npts,noise)

def Korns_05(xs_params,npts,noise):
	eqn_str = "3 + 2.13*ln(w)"
	xs = [x,y,z,v,w]
	return gen("Korns_05", eqn_str,xs,xs_params,npts,noise)

def Korns_06(xs_params,npts,noise):
	eqn_str = "1.3 + 0.13*sqrt(x)"
	xs = [x,y,z,v,w]
	return gen("Korns_06", eqn_str,xs,xs_params,npts,noise)

def Korns_07(xs_params,npts,noise):
	eqn_str = "213.80940889*(1 - e**(-0.54723748542*x))"
	xs = [x,y,z,v,w]
	return gen("Korns_07", eqn_str,xs,xs_params,npts,noise)

def Korns_08(xs_params,npts,noise):
	eqn_str = "6.87 + 11*sqrt(7.23*x*v*w)"
	xs = [x,y,z,v,w]
	return gen("Korns_08", eqn_str,xs,xs_params,npts,noise)

def Korns_09(xs_params,npts,noise):
	eqn_str = "(sqrt(x)/ln(y)) * (e**z / v**2)"
	xs = [x,y,z,v,w]
	return gen("Korns_09", eqn_str,xs,xs_params,npts,noise)

def Korns_10(xs_params,npts,noise):
	eqn_str = "0.81 + 24.3*(2y+3*z**2)/(4*(v)**3+5*(w)**4)"
	xs = [x,y,z,v,w]
	return gen("Korns_10", eqn_str,xs,xs_params,npts,noise)

def Korns_11(xs_params,npts,noise):
	eqn_str = "6.87 + 11*cos(7.23*x**3)"
	xs = [x,y,z,v,w]
	return gen("Korns_11", eqn_str,xs,xs_params,npts,noise)

def Korns_12(xs_params,npts,noise):
	eqn_str = "2 - 2.1*cos(9.8*x)*sin(1.3*w)"
	xs = [x,y,z,v,w]
	return gen("Korns_12", eqn_str,xs,xs_params,npts,noise)

def Korns_13(xs_params,npts,noise):
	eqn_str = "32 - 3*(tan(x)*tan(z))/(tan(y)*tan(v))"
	xs = [x,y,z,v,w]
	return gen("Korns_13", eqn_str,xs,xs_params,npts,noise)

def Korns_14(xs_params,npts,noise):
	eqn_str = "22 - 4.2*(cos(x)-tan(y))*(tanh(z)/sin(v))"
	xs = [x,y,z,v,w]
	return gen("Korns_14", eqn_str,xs,xs_params,npts,noise)

def Korns_15(xs_params,npts,noise):
	eqn_str = "12 - 6*(tan(x)/e**y)(ln(z)-tan(v))"
	xs = [x,y,z,v,w]
	return gen("Korns_15", eqn_str,xs,xs_params,npts,noise)








