 
Install:

sudo apt-get install liblapack3 liblapack-dev libblas3 libblas-dev f2c
cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DLINSOLVERS_RETAIN_MEMORY=0 .
make

int LEVMAR_DER(
  void (*func)(LM_REAL *p, LM_REAL *hx, int m, int n, void *adata),  * functional relation describing measurements. A p \in R^m yields a \hat{x} \in  R^n 
  void (*jacf)(LM_REAL *p, LM_REAL *j, int m, int n, void *adata),   * function to evaluate the Jacobian \part x / \part p 
  LM_REAL *p,          * I/O: initial parameter estimates. On output has the estimated solution 
  LM_REAL *x,          * I: measurement vector. NULL implies a zero vector 
  int m,               * I: parameter vector dimension (i.e. #unknowns) 
  int n,               * I: measurement vector dimension 
  int itmax,           * I: maximum number of iterations 
  LM_REAL opts[4],     * I: minim. options [\mu, \epsilon1, \epsilon2, \epsilon3]. Respectively the scale factor for initial \mu,
                       * stopping thresholds for ||J^T e||_inf, ||Dp||_2 and ||e||_2. Set to NULL for defaults to be used
                       
  LM_REAL info[LM_INFO_SZ],
                      * O: information regarding the minimization. Set to NULL if don't care
                      * info[0]= ||e||_2 at initial p.
                      * info[1-4]=[ ||e||_2, ||J^T e||_inf,  ||Dp||_2, mu/max[J^T J]_ii ], all computed at estimated p.
                      * info[5]= # iterations,
                      * info[6]=reason for terminating: 1 - stopped by small gradient J^T e
                      *                                 2 - stopped by small Dp
                      *                                 3 - stopped by itmax
                      *                                 4 - singular matrix. Restart from current p with increased mu 
                      *                                 5 - no further error reduction is possible. Restart with increased mu
                      *                                 6 - stopped by small ||e||_2
                      *                                 7 - stopped by invalid (i.e. NaN or Inf) "func" values. This is a user error
                      * info[7]= # function evaluations
                      * info[8]= # Jacobian evaluations
                      * info[9]= # linear systems solved, i.e. # attempts for reducing error
                      
  LM_REAL *work,      * working memory at least LM_DER_WORKSZ() reals large, allocated if NULL 
  LM_REAL *covar,     * O: Covariance matrix corresponding to LS solution; mxm. Set to NULL if not needed. 
  void *adata)        * pointer to possibly additional data, passed uninterpreted to func & jacf.
                      * Set to NULL if not needed
