from sympy import *
import numpy as np
np.random.seed(23)

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
v = Symbol('v')
w = Symbol('w')

def gen_xpts(xs_params, npts):
	pts = []
	for xp in xs_params:
		xs = np.random.uniform(low=xp[0],high=xp[1],size=npts)
		pts.append(xs)
	xpts = np.array(pts)
	return xpts

def gen(name,eqn_str, xs, xs_params, npts, noise):
	eqn = sympify(eqn_str)
	xpts = gen_xpts(xs_params, npts)
	ypure = lambdify(xs,eqn,"numpy")(*xpts)
	ypts = ypure + np.random.normal(0, noise, len(ypure))

	xs_str = " ".join(str(xi) for xi in xs)

	return {
		'name': name,
		'eqn_str': eqn_str,
		'eqn': eqn,
		'xs': xs,
		'xs_str': xs_str,
		'xs_params': xs_params,
		'xpts': xpts,
		'ypure': ypure,
		'ypts': ypts
	}


# 1 input: x
def Koza_1(noise):
	xs_params = [ (-4.0,4.0) ]
	npts = 200
	eqn_str = "x**4 + x**3 + x**2 + x"
	xs = [x]
	return gen("Koza_1", eqn_str,xs,xs_params,npts,noise)

def Koza_2(noise):
	xs_params = [ (-4.0,4.0) ]
	npts = 200
	eqn_str = "x**5 - 2*x**3 + x"
	xs = [x]
	return gen("Koza_2", eqn_str,xs,xs_params,npts,noise)

def Koza_3(noise):
	xs_params = [ (-4.0,4.0) ]
	npts = 200
	eqn_str = "x**6 - 2*x**4 + x**2"
	xs = [x]
	return gen("Koza_3", eqn_str,xs,xs_params,npts,noise)

def Lipson_1(noise):
	xs_params = [ (-5.0,5.0) ]
	npts = 200
	eqn_str = "1.5 * x**2 - x**3"
	xs = [x]
	return gen("Lipson_1", eqn_str,xs,xs_params,npts,noise)

def Lipson_2(noise):
	xs_params = [ (-9.7,9.7) ]
	npts = 500
	eqn_str = "exp(Abs(x)) * sin(x)"
	xs = [x]
	return gen("Lipson_2", eqn_str,xs,xs_params,npts,noise)

def Lipson_3(noise):
	xs_params = [ (-14.0,14.0) ]
	npts = 500
	eqn_str = "x**2 * exp(sin(x)) + x + sin(pi/4.0 - x**3)"
	xs = [x]
	return gen("Lipson_3", eqn_str,xs,xs_params,npts,noise)

def Nguyen_01(noise):
	xs_params = [ (-5.0,5.0) ]
	npts = 200
	eqn_str = "x**3 + x**2 + x"
	xs = [x]
	return gen("Nguyen_01", eqn_str,xs,xs_params,npts,noise)

def Nguyen_02(noise):
	xs_params = [ (-5.0,5.0) ]
	npts = 200
	eqn_str = "x**4 + x**3 + x**2 + x"
	xs = [x]
	return gen("Nguyen_02", eqn_str,xs,xs_params,npts,noise)

def Nguyen_03(noise):
	xs_params = [ (-5.0,5.0) ]
	npts = 200
	eqn_str = "x**5 + x**4 + x**3 + x**2 + x"
	xs = [x]
	return gen("Nguyen_03", eqn_str,xs,xs_params,npts,noise)

def Nguyen_04(noise):
	xs_params = [ (-5.0,5.0) ]
	npts = 200
	eqn_str = "x**6 + x**5 + x**4 + x**3 + x**2 + x"
	xs = [x]
	return gen("Nguyen_04", eqn_str,xs,xs_params,npts,noise)

def Nguyen_05(noise):
	xs_params = [ (-5.0,5.0) ]
	npts = 1000 
	eqn_str = "sin(x**2)*cos(x) - 1"
	xs = [x]
	return gen("Nguyen_05", eqn_str,xs,xs_params,npts,noise)

def Nguyen_06(noise):
	xs_params = [ (-5.0,5.0) ]
	npts = 1000 
	eqn_str = "sin(x) + sin(x + x**2)"
	xs = [x]
	return gen("Nguyen_06", eqn_str,xs,xs_params,npts,noise)

def Nguyen_07(noise):
	xs_params = [ (0.0,1000.0) ]
	npts = 1000 
	eqn_str = "ln(x+1) + ln(x**2 + 1)"
	xs = [x]
	return gen("Nguyen_07", eqn_str,xs,xs_params,npts,noise)

def Nguyen_08(noise):
	xs_params = [ (0.0001,10000.0) ]
	npts = 1000 
	eqn_str = "sqrt(x)"
	xs = [x]
	return gen("Nguyen_08", eqn_str,xs,xs_params,npts,noise)


# 2 inputs: x,y
def Nguyen_09(noise):
	xs_params = []
	xs_params.append( (-10.0,10.0) )
	xs_params.append( (-6.0,6.0) )
	npts = 1000
	eqn_str = "sin(x) + sin(y**2)"
	xs = [x,y]
	return gen("Nguyen_09", eqn_str,xs,xs_params,npts,noise)

def Nguyen_10(noise):
	xs_params = []
	xs_params.append( (-7.0,7.0) )
	xs_params.append( (-7.0,7.0) )
	npts = 1000
	eqn_str = "2*sin(x)*cos(y)"
	xs = [x,y]
	return gen("Nguyen_10", eqn_str,xs,xs_params,npts,noise)

def Nguyen_11(noise):
	xs_params = []
	xs_params.append( (0.0,4.0) )
	xs_params.append( (1.0,4.0) )
	npts = 1000
	eqn_str = "x**y"
	xs = [x,y]
	return gen("Nguyen_11", eqn_str,xs,xs_params,npts,noise)

def Nguyen_12(noise):
	xs_params = []
	xs_params.append( (-8.0,8.0) )
	xs_params.append( (-8.0,8.0) )
	npts = 1000
	eqn_str = "x**4 - x**3 + 0.5*y**2 - y"
	xs = [x,y]
	return gen("Nguyen_12", eqn_str,xs,xs_params,npts,noise)

def Pagie_1(noise):
	xs_params = []
	xs_params.append( (0.0001,3.0) )
	xs_params.append( (0.0001,3.0) )
	npts = 1000
	eqn_str = "1 / (1 + x**-4) + 1 / (1 + y**-4)"
	xs = [x,y]
	return gen("Pagie_1", eqn_str,xs,xs_params,npts,noise)


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








