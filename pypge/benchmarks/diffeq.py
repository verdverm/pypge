
# from hods paper
glider_dv = -0.5*v**2 - sin(th)
glider_dth= v -cos(th)/v

bacresp_dx = 20 - x - x*y / (1.0 + 0.5*x**2)
bacresp_dy = 10 - x*y / (1.0 + 0.5*x**2)

predprey_dx = x * (4.0 - x - y/(1.0+x))
predprey_dy = y * (x/(1.0+x) - 0.075* y)

barmags_dth1 = 0.5 * sin(th1-th2) - sin(th1)
barmags_dth2 = 0.5 * sin(th2-th1) - sin(th2)

shearflow_dth  = cot(phi)*cos(th)
shearflow_dphi = (cos(phi)**2 + 0.1*sin(phi)**2)*sin(th)

vanderpol_dx = 10 * (y-(1.0/3.0*x**3 - x))
vanderpol_dy = -0.1*x 

lotkaVolt_dx = 3.0*x - 2.0*x*y - x**2
lotkaVolt_dy = 2.0*y - x*y - y**2


########################################
# http://www.myphysicslab.com/index.html
########################################

###  Pendulum
# th = angle of pendulum (0=vertical)
# R = length of rod
# T = tension in rod
# m = mass of pendulum
# g = gravitational constant
# R = length_of_rod
pendulum_dth = w 
pendulum_dw  = -g / R * sin(th)


###  Chaotic Pendulum (dampened & driven)
# θ = angle of pendulum (0 = vertical)
# ω = dθ = angular velocity
# R = length of rod
# m = mass of pendulum
# g = gravitational constant
# b = damping (friction) constant
# A = amplitude of driving force
# k = constant related to frequency of driving force
# t = time in seconds
dt = 1
dθ = ω
dω = −g⁄R*sin(θ) + ( -b*ω + A*cos(k*t) ) / (m*R**2)
### Erik Neumann wants a picture of the completed chaotic graph for this pendulum
### erikn@MyPhysicsLab.com
### maybe also suggest a collaboration for Ipython, Sympy, RK4, and PyPGE


###  Pendulum on a Cart
# N = normal force (from the track the cart is on)
# T = tension in the rod
# M = mass of cart
# m = mass of pendulum
# g = gravitational constant
# d = cart friction constant
# b = pendulum friction constant
# k = spring stiffness
# dx = v
# dθ = ω
# dv_numer = m R ω2 sin θ + m g sin θ cos θ − k x − d v + b⁄R ω cos θ
# dv_denom = M + m sin2θ
# dω_numer = −m R ω2 sin θ cos θ − (m+M)g sin θ + k x cos θ + d v cos θ − (1 + M⁄m)b⁄R ω
# dω_denom = R (M + m sin2θ)


###  Double Pendulum
# x = horizontal position of pendulum mass
# y = vertical position of pendulum mass
# θ = angle of pendulum (0 = vertical downwards, counter-clockwise is positive)
# L = length of rod (constant)
# ω1 = angular velocity of top rod
# ω2 = angular velocity of bottom rod
# x1 = L1 sin θ1
# y1 = −L1 cos θ1
# x2 = x1 + L2 sin θ2
# y2 = y1 − L2 cos θ2
# dθ1 = ω1
# dθ2 = ω2
# dω1_numer = −g (2 m1 + m2) sin θ1 − m2 g sin(θ1 − 2 θ2) − 2 sin(θ1 − θ2) m2 (ω22 L2 + ω12 L1 cos(θ1 − θ2))
# dω1_denom = L1 (2 m1 + m2 − m2 cos(2 θ1 − 2 θ2))
# dω2_numer = 2 sin(θ1−θ2) (ω12 L1 (m1 + m2) + g(m1 + m2) cos θ1 + ω22 L2 m2 cos(θ1 − θ2))
# dω2_denom = L2 (2 m1 + m2 − m2 cos(2 θ1 − 2 θ2))


###  Spring
# x = position of the block
# v = dx = velocity of the block
# m = mass of the block
# R = rest length of the spring
# k = spring stiffness
# b = damping constant (friction)
spring_dx = v
spring_dv = -k/m*x - b/m*v


###  Double Spring
# Define the following variables
# x1, x2 = position (left edge) of blocks
# v1, v2 = velocity of blocks
# F1, F2 = force experienced by blocks
# L1, L2 = how much spring is stretched
# And define the following constants:
# m1, m2 = mass of blocks
# w1, w2 = width of blocks
# k1, k2 = spring constants
# R1, R2 = rest length of springs
dblspring_dx1 = v1
dblspring_dx2 = v2
dblspring_dv1 = −(k1 ⁄ m1) (x1 − R1) + (k2 ⁄ m1) (x2 − x1 − w1 − R2)
dblspring_dv2 = −(k2 ⁄ m2) (x2 − x1 − w1 − R2)


### 2-Dim Spring
# θ = angle (0 = vertical, increases counter-clockwise)
# S = spring stretch (displacement from rest length)
# L = length of spring
# u = position of bob
# v = u'= velocity of bob
# a = u''= acceleration of bob
# R = rest length of spring
# T = position of anchor point
# m = mass of bob
# k = spring constant
# b = damping constant
# g = gravitational constant
S = L − R
L = sqrt( (u_x - T_x)**2 + (u_y - T_y)**2 )
sin(θ) = (u_x − T_x)/L
cos(θ) = (u_y − T_y)/L
du_x = v_x
du_y = v_y
dv_x = − k⁄m * S * sin(θ) − b⁄m*v_x
dv_y = g − k⁄m*S*cos(θ) − b⁄m*v_y


763832







