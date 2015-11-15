#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#include "levmar-2.6/levmar.h"
#include "levmar_h.h"






void callback_eqn_func(double *p, double *x, int m, int n, void *data) {
  CallbackEqn_func(p,x,data);
}

void callback_eqn_jacfunc(double *p, double *jac, int m, int n, void *data) {
  CallbackEqn_jacfunc(p,jac,data);
}

void levmar_eqn_der( double* ygiven, double* p, const int m, const int n, double* ret_info, void* data ) {
  double opts[LM_OPTS_SZ], info[LM_INFO_SZ];
  // printf("LM_OPTS_SZ: %d   LM_INFO_SZ: %d  LM_INIT_MU: %f\n", LM_OPTS_SZ, LM_INFO_SZ, LM_INIT_MU);

  // optimization control parameters; passing to levmar NULL instead of opts reverts to defaults
  opts[0]=LM_INIT_MU;   // 0.001000
  opts[1]=1E-15;
  opts[2]=1E-15;
  opts[3]=1E-20;
  opts[4]=LM_DIFF_DELTA; // relevant only if the finite difference Jacobian version is used

  // invoke the optimization function
  dlevmar_der(callback_eqn_func, callback_eqn_jacfunc, p, ygiven, m, n, 32, opts, info, NULL, NULL, data); // with analytic Jacobian

  memcpy(ret_info, &info, sizeof(double)*LM_INFO_SZ);
  // printf("Levenberg-Marquardt returned in %g iter, reason %g, sumsq %g [%g]\n", info[5], info[6], info[1], info[0]);

}

void levmar_eqn_dif( double* ygiven, double* p, const int m, const int n, double* ret_info, void* data ) {
  double opts[LM_OPTS_SZ], info[LM_INFO_SZ];

  // optimization control parameters; passing to levmar NULL instead of opts reverts to defaults
  opts[0]=LM_INIT_MU; opts[1]=1E-15; opts[2]=1E-15; opts[3]=1E-20;
  opts[4]=LM_DIFF_DELTA; // relevant only if the finite difference Jacobian version is used

  // invoke the optimization function
  dlevmar_dif(callback_eqn_func, p, ygiven, m, n, 128, opts, info, NULL, NULL, data); // without Jacobian

  memcpy(ret_info, &info, sizeof(double)*LM_INFO_SZ);
  // printf("Levenberg-Marquardt returned in %g iter, reason %g, sumsq %g [%g]\n", info[5], info[6], info[1], info[0]);

}






