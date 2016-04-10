import pandas as pd 
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

import sys

phases = [
    "expand",
    "evaluate",
    "other",
    "loop_total"
]

pgefile=sys.argv[1]
outfile=sys.argv[2]

of = open(outfile, "w", 1)

df = pd.read_csv(pgefile, delim_whitespace=True)

other = df["loop_total"] - ( df["expand"] + df["evaluate"] )
df["other"] = other

# df = df[cols2]

problems = df.groupby("problem")

print("problem  group  expand  evaluate  other  total", file=of)
for pname, prob in problems:
    # print(pname)
    # print(prob)

    pgroups = prob.groupby("group")
    for gname, grp in pgroups:
        sums = grp[phases].sum()
        print(pname, gname, sums[0], sums[1], sums[2], sums[3], file=of)
        # print(sums)



