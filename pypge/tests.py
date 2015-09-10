from __future__ import division

from sympy import *
init_printing(use_unicode=True)

import numpy as np
np.random.seed(23)

from evaluate import Eval, Score

x = symbols('x')

F_1 = 1.5 * x**2 - x**3
F_2 = exp(Abs(x)) * sin(x)
F_3 = x**2 * exp(sin(x)) + x + sin(pi/4.0 - x**3)

F_1_X = np.linspace(-5., 5., num=200)
F_2_X = np.linspace(-3., 3., num=200)
F_3_X = np.linspace(-10., 10., num=200)

F_1_Y_pure = Eval(x,F_1,F_1_X)
F_2_Y_pure = Eval(x,F_2,F_2_X)
F_3_Y_pure = Eval(x,F_3,F_3_X)

F_1_Y = F_1_Y_pure + np.random.normal(0, 0.05, 200)
F_2_Y = F_2_Y_pure + np.random.normal(0, 0.05, 200)
F_3_Y = F_3_Y_pure + np.random.normal(0, 0.05, 200)

S_1 = Score(F_1_Y_pure,F_1_Y)
S_2 = Score(F_2_Y_pure,F_2_Y)
S_3 = Score(F_3_Y_pure,F_3_Y)

print S_1, F_1
print S_2, F_2
print S_3, F_3
