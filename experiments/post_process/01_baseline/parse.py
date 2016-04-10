import pandas as pd 
import numpy as np
# import matplotlib.pyplot as plt


print( "parsing 01_baseline GP" )

datadir="/dissertation_output/01_baseline/"
gpfile = datadir + "gp_results_all.txt"

cols = [
    "run",
    "name",
    "seed",
    "iter",
    "rmse",
    "r2"
]

df = pd.read_csv(gpfile, header=None, names=cols, delim_whitespace=True)

df2 = df[["name", "rmse", "r2"]]

# print(df2)

gp = df2.groupby('name')

# print(gp.groups)

# for name, group in gp:
#     print(name)
#     print(group)


gp_min = gp.aggregate(np.min)
gp_max = gp.aggregate(np.max)
gp_ave = gp.aggregate(np.mean)

frames = [gp_ave, gp_min["rmse"], gp_max["r2"]]
gp_fin = pd.concat(frames, axis=1)

# print(gp_min)
# print(gp_max)
# print(gp_ave)

print(gp_fin.to_latex())