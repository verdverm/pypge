import pandas as pd 
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

import sys

phases = [
    "expand",
    "evaluate",
    "other"
]

pgefile=sys.argv[1]
outfile=sys.argv[2]

of = open(outfile, "w", 1)

df = pd.read_csv(pgefile, delim_whitespace=True)
other = df["loop_total"] - ( df["expand"] + df["evaluate"] )
df["other"] = other


pgroups = df.groupby("group")


def plot_graph(df, name):


    plt.figure()
    ax = df.plot.box();

    ax.set_xlabel("Phase",fontsize=12)
    ax.set_ylabel("seconds",fontsize=12)
    ax.set_title("Phase statistics for " + name, y=1.04)

    locs, labels = plt.xticks()
    plt.setp(labels, rotation=45)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    fig = ax.get_figure()
    fig.savefig('imgs/speedup/'+name+'.png')
    fig.savefig('imgs/speedup/'+name+'.pdf')


# print("problem  expand_min  evaluate_min  other_min  expand_ave  evaluate_ave  other_ave  expand_max  evaluate_max  other_max  expand_std  evaluate_std  other_std  ", file=of)

for gname, grp in pgroups:
    if gname == "p1_e01" or gname == "p3_e04":
        print(gname)
        problems = grp.groupby("problem")
        for pname, prob in problems:
            dfp = prob[phases]
            # means = dfp.mean()
            # mins = dfp.min()
            # maxs = dfp.max()
            # stds = dfp.std()

            plot_graph(dfp, pname + "-" + gname + "-phasestats")

            # print(pname, 
            #     mins[0], mins[1], mins[2], 
            #     means[0], means[1], means[2], 
            #     maxs[0], maxs[1], maxs[2], 
            #     stds[0], stds[1], stds[2], 
            #     file=of )


            # print(pname, sums[0], sums[1], sums[2], sums[3], file=of)
            # print(sums)




# df2 = pd.read_csv(outfile, delim_whitespace=True)

# plot_graph(df2[["expand_min", "expand_max", "expand_ave", "expand_std"]], "expansion")


