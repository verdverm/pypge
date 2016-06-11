Fitness Experiments
-------------------

The configuration files in this directory
explore the range of fitness metrics
and their combination.

Normalization per component is essential.
It deals with the differences in scales of the values.

Density-based Pareto non-dominated sorting 
has been proven better than vanilla.
We use NSGA-II with log-non-dominated sorting.


#### Fitness Components

Accuracy Components:

1. (ERR) error: (**MAE, MSE, RMAE, RMSE**)
1. (**R2**) r2
1. (**EVAR**) explained variance
1. (**RCHI**) reduced chi-squared
1. (**AIC**) aic
1. (**BIC**) bic

*Accuracy components each have an improvement version.
This is the improvement over the parent's value.
They will be prepended with a **I_**.*

Parsimony Components:

1. (**TS**)   tree-size 
1. (**PTS**)  penalized tree-size
1. (**JTS**)  jacobian penalized tree-size


Mixture and Weighting:

1. Which components should be chosen
    1. Number of components
    1. Mixture of Accuracy
    1. Mixture of Parismony
1. How should each component be weighted
    1. Equal weighting
    1. Balance accuracy & parsimony


#### Benchmarks

Explicit

- Koza_01
- Nguyen_04
- Nguyen_12
- Korns_03



#### Experimental Settings

1. Example Parameters
    - [Component List]
    - [Component Weights]

------

Baseline 2 component

- A_1_1:
    - [TS, MAE]
    - [1.0, 1.0]
- A_1_2:
    - [TS, RMSE]
    - [1.0, 1.0]

Multiple equal-weight accuracy components

- A_2_2a:
    - [TS, RMSE, R2]
    - [1.0, 1.0, 1.0]
- A_2_2b:
    - [TS, RMSE, BIC]
    - [1.0, 1.0, 1.0]
- A_2_3a:
    - [TS, RMSE, R2, BIC]
    - [1.0, 1.0, 1.0, 1.0]
- A_2_3b:
    - [TS, RMSE, R2, EVAR]
    - [1.0, 1.0, 1.0, 1.0]
- A_2_4a:
    - [TS, RMSE, R2, BIC, I_BIC]
    - [1.0, 1.0, 1.0, 1.0, 1.0]
- A_2_4b:
    - [TS, RMSE, RCHI, BIC, I_BIC]
    - [1.0, 1.0, 1.0, 1.0, 1.0]
- A_2_5:
    - [TS, RMSE, RCHI, EVAR, BIC, I_BIC]
    - [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


Multiple balanced-weight accuracy components

- A_3_2a:
    - [TS, RMSE, R2]
    - [2.0, 1.0, 1.0]
- A_3_2b:
    - [TS, RMSE, BIC]
    - [2.0, 1.0, 1.0]
- A_3_3a:
    - [TS, RMSE, R2, BIC]
    - [3.0, 1.0, 1.0, 1.0]
- A_3_3b:
    - [TS, RMSE, R2, EVAR]
    - [4.0, 1.0, 1.0, 1.0]
- A_3_4a:
    - [TS, RMSE, R2, BIC, I_BIC]
    - [4.0, 1.0, 1.0, 1.0, 1.0]
- A_3_4b:
    - [TS, RMSE, RCHI, BIC, I_BIC]
    - [4.0, 1.0, 1.0, 1.0, 1.0]
- A_3_5:
    - [TS, RMSE, RCHI, EVAR, BIC, I_BIC]
    - [5.0, 1.0, 1.0, 1.0, 1.0, 1.0]







Parsimony 2 Component

- P_1_1:
    - [PTS, MAE]
    - [1.0, 1.0]
- P_1_2:
    - [PTS, RMSE]
    - [1.0, 1.0]
- P_1_3:
    - [JTS, MAE]
    - [1.0, 1.0]
- P_1_4:
    - [JTS, RMSE]
    - [1.0, 1.0]


Parsimony Multi-accuracy Component equal-weighted

- P_2_5a:
    - [PTS, RMSE, RCHI, EVAR, BIC, I_BIC]
    - [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
- P_2_5b:
    - [JTS, RMSE, RCHI, EVAR, BIC, I_BIC]
    - [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]


Parsimony Multi-accuracy Component balance-weighted

- P_3_5a:
    - [PTS, RMSE, RCHI, EVAR, BIC, I_BIC]
    - [5.0, 1.0, 1.0, 1.0, 1.0, 1.0]
- P_3_5b:
    - [JTS, RMSE, RCHI, EVAR, BIC, I_BIC]
    - [5.0, 1.0, 1.0, 1.0, 1.0, 1.0]


Parsimony Multi-all Component balance-weighted

- P_4_5a:
    - [PTS, JTS, RMSE, RCHI, EVAR, BIC, I_BIC]
    - [4.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
- P_4_5b:
    - [PTS, JTS, RMSE, RCHI, EVAR, BIC, I_BIC]
    - [3.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0]
- P_4_5c:
    - [PTS, JTS, RMSE, RCHI, EVAR, BIC, I_BIC]
    - [2.5, 2.5, 1.0, 1.0, 1.0, 1.0, 1.0]
- P_4_5c:
    - [JTS, PTS, RMSE, RCHI, EVAR, BIC, I_BIC]
    - [2.5, 2.5, 1.0, 1.0, 1.0, 1.0, 1.0]
- P_4_5d:
    - [JTS, PTS, RMSE, RCHI, EVAR, BIC, I_BIC]
    - [3.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0]
- P_4_5e:
    - [JTS, PTS, RMSE, RCHI, EVAR, BIC, I_BIC]
    - [4.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]







