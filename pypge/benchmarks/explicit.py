from sympy import *
import numpy as np

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
v = Symbol('v')
w = Symbol('w')

def gen_problem(eqn_str, xs, xmin, xmax, npts, noise):
	eqn_str = eqn_str,
	return {
		'eqn_str': eqn_str,
		'eqn': sympify(eqn_str),
		'xs': xs,
		'xpts': np.linspace(xmin, xmax, num=npts),
		'ypure': lambdify(x,eqn,"numpy")(xpts),
		'ypts': ypure + np.random.normal(0, noise, len(ypure))	
	}


# 1 input: x
def Koza_1(xmin,xmax,npts,noise):
	eqn_str = "x^4 + x^3 + x^2 + x"
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Koza_2(xmin,xmax,npts,noise):
	eqn_str = "x^5 - 2x^3 + x",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Koza_3(xmin,xmax,npts,noise):
	eqn_str = "x^6 - 2x^4 + x^2",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Lipson_1(xmin,xmax,npts,noise):
	eqn_str = "1.5 * x**2 - x**3"
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Lipson_2(xmin,xmax,npts,noise):
	eqn_str = "exp(Abs(x)) * sin(x)",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Lipson_3(xmin,xmax,npts,noise):
	eqn_str = "x**2 * exp(sin(x)) + x + sin(pi/4.0 - x**3)",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Nguyen_01(xmin,xmax,npts,noise):
	eqn_str = "x^3 + x^2 + x",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Nguyen_02(xmin,xmax,npts,noise):
	eqn_str = "x^4 + x^3 + x^2 + x",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Nguyen_03(xmin,xmax,npts,noise):
	eqn_str = "x^5 + x^4 + x^3 + x^2 + x",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Nguyen_04(xmin,xmax,npts,noise):
	eqn_str = "x^6 + x^5 + x^4 + x^3 + x^2 + x",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Nguyen_05(xmin,xmax,npts,noise):
	eqn_str = "sin(x^2)*cos(x) - 1",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Nguyen_06(xmin,xmax,npts,noise):
	eqn_str = "sin(x) + sin(x + x^2)",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Nguyen_07(xmin,xmax,npts,noise):
	eqn_str = "ln(x+1) + ln(x^2 + 1)",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Nguyen_08(xmin,xmax,npts,noise):
	eqn_str = "sqrt(x)",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)


# 2 inputs: x,y
def Nguyen_09(xmin,xmax,npts,noise):
	eqn_str = "sin(x) + sin(y^2)",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Nguyen_10(xmin,xmax,npts,noise):
	eqn_str = "2*sin(x)*cos(y)",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Nguyen_11(xmin,xmax,npts,noise):
	eqn_str = "x^y",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Nguyen_12(xmin,xmax,npts,noise):
	eqn_str = "x^4 - x^3 + 0.5*y^2 - y",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Pagie_1(xmin,xmax,npts,noise):
	eqn_str = "1 / (1 + x^-4) + 1 / (1 + y^-4)",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)


# 5 inputs: x,y,z,v,w
def Korns_01(xmin,xmax,npts,noise):
	eqn_str = "1.57 + 24.3*v",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Korns_02(xmin,xmax,npts,noise):
	eqn_str = "0.23 + 14.2*(v+y)/3w",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Korns_03(xmin,xmax,npts,noise):
	eqn_str = "-5.41 + 4.9*(v-x+y/w)/3w",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Korns_04(xmin,xmax,npts,noise):
	eqn_str = "-2.3 + 0.13sin(z)",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Korns_05(xmin,xmax,npts,noise):
	eqn_str = "3 + 2.13*ln(w)",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Korns_06(xmin,xmax,npts,noise):
	eqn_str = "1.3 + 0.13*sqrt(x)",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Korns_07(xmin,xmax,npts,noise):
	eqn_str = "213.80940889*(1 - e^(-0.54723748542*x))",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Korns_08(xmin,xmax,npts,noise):
	eqn_str = "6.87 + 11*sqrt(7.23*x*v*w)",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Korns_09(xmin,xmax,npts,noise):
	eqn_str = "(sqrt(x)/ln(y)) * (e^z / v^2)",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Korns_10(xmin,xmax,npts,noise):
	eqn_str = "0.81 + 24.3*(2y+3*z^2)/(4*(v)^3+5*(w)^4)",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Korns_11(xmin,xmax,npts,noise):
	eqn_str = "6.87 + 11*cos(7.23*x^3)",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Korns_12(xmin,xmax,npts,noise):
	eqn_str = "2 - 2.1*cos(9.8*x)*sin(1.3*w)",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Korns_13(xmin,xmax,npts,noise):
	eqn_str = "32 - 3*(tan(x)*tan(z))/(tan(y)*tan(v))",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Korns_14(xmin,xmax,npts,noise):
	eqn_str = "22 - 4.2*(cos(x)-tan(y))*(tanh(z)/sin(v))",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)

def Korns_15(xmin,xmax,npts,noise):
	eqn_str = "12 - 6*(tan(x)/e^y)(ln(z)-tan(v))",
	xs = [x]
	return gen(eqn_str,xs,xmin,xmax,npts,noise)








