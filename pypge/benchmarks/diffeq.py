import sympy

from scipy.integrate import odeint

import numpy as np
np.random.seed(23)

T = sympy.Symbol("T")

import pprint
pp = pprint.PrettyPrinter(indent=4)



def gen(prob_params, **kwargs):
	prob_params = prep_params(prob_params, **kwargs)

	pp.pprint(prob_params)

	eqns = []
	for estr in prob_params['eqn_strs']:
		e = sympy.sympify(estr)
		eqns.append(e)

	time_pts = np.arange(0., prob_params['time_end'], prob_params['time_step'])
	win_sz = len(time_pts)/10
	if win_sz % 2 == 0:
		win_sz += 1

	xs_pure = gen_pts(eqns, prob_params['xs'], prob_params['params'], prob_params['init_conds'], time_pts)
	xs_pure = xs_pure.T
	xs_pts = []
	for data in xs_pure:
		dpts = data + np.random.normal(0, prob_params['noise'], len(data))
		xs_pts.append(dpts)
	xs_pts = np.array(xs_pts)

	prob_params['eqns'] = eqns
	prob_params['time_pts'] = time_pts
	prob_params['xs_pure'] = xs_pure
	prob_params['xs_pts'] = xs_pts

	return prob_params

def prep_params(prob_params, **kwargs):
	prob_params['xs'] = sympy.symbols(prob_params['xs_str'])
	prob_params['dxs_str'] = ["d"+x for x in prob_params['xs_str']]
	prob_params['dxs'] = sympy.symbols(prob_params['dxs_str'])

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
		return derivs

	iconds = [val for k,val in init_conds.items()]

	pts = odeint(evalr, iconds, time_pts)
	return pts



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
		'noise': 0.1
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
		'noise': 0.1
	}
	return gen(this, **kwargs)



# import matplotlib.pyplot as plt

# stuff = SimplePendulum(params={'M':0.2})
# stuff = ChaoticPendulum()


# t_pts = stuff['time_pts']
# x_pts = stuff['xs_pts']
# xs_pts_smooth = stuff['xs_pts_smooth']
# dx_pts = stuff['xs_pts_deriv']

# print t_pts.shape, x_pts.shape, dx_pts.shape

# fig = plt.figure(1, figsize=(8,8))

# # Plot velocity as a function of time
# ax1 = fig.add_subplot(311)
# ax1.plot(t_pts, x_pts[0])
# ax1.plot(t_pts, xs_pts_smooth[0])
# ax1.plot(t_pts, dx_pts[0], 'r')
# ax1.set_xlabel('time')
# ax1.set_ylabel('velocity')

# # Plot angle as a function of time
# ax2 = fig.add_subplot(312)
# ax2.plot(t_pts, xs_pts_smooth[1])
# ax2.plot(t_pts, dx_pts[1], 'r')
# ax2.set_xlabel('time')
# ax2.set_ylabel('angle')

# # Plot velocity vs angle
# ax3 = fig.add_subplot(313)
# ax3.plot(x_pts[0], x_pts[1], '.', ms=2)
# ax3.set_xlabel('velocity')
# ax3.set_ylabel('angle')

# plt.show()



# this matches the output of the chaotic_pendulum.py
#   however it contains physical unrealities
# ps = {
# 	"M": 1.0,
# 	"R": 1.0,
# 	"g": -1.0, # THIS IS BOGUS
# 	"a": 1.5,
# 	"b": 0.5,
# 	"k": 0.65
# }
# stuff = ChaoticPendulum(time_end=200.0, time_step=0.05, params=ps)


# t_pts = stuff['time_pts']
# x_pts = stuff['xs_pure']

# fig = plt.figure(1, figsize=(8,8))

# # Plot velocity as a function of time
# ax1 = fig.add_subplot(311)
# ax1.plot(t_pts, x_pts[0])
# ax1.set_xlabel('time')
# ax1.set_ylabel('velocity')

# # Plot angle as a function of time
# ax2 = fig.add_subplot(312)
# ax2.plot(t_pts, x_pts[1])
# ax2.set_xlabel('time')
# ax2.set_ylabel('angle')

# # Plot velocity vs angle
# ax3 = fig.add_subplot(313)
# twopi = 2.0*np.pi
# ax3.plot(x_pts[0]%twopi, x_pts[1], '.', ms=3)
# ax3.set_xlabel('velocity')
# ax3.set_ylabel('angle')
# ax3.set_xlim(0., twopi)

# plt.show()





