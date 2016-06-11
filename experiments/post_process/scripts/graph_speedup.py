import pandas as pd 
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

import sys


cols = [
    "group",
    "expand",
    "evaluate",
    "other"
]

def plot_graph(df, name):

    plt.figure()
    ax = df.plot.bar(x=df["group"], stacked=True);

    ax.set_xlabel("seconds",fontsize=12)
    ax.set_ylabel("group",fontsize=12)
    # ax.set_title("Phase times for " + name, y=1.04)

    locs, labels = plt.xticks()
    plt.setp(labels, rotation=45)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    fig = ax.get_figure()
    fig.savefig('imgs/speedup/'+name+'.pdf')


pgefile=sys.argv[1]


df = pd.read_csv(pgefile, delim_whitespace=True)

problems = df.groupby("problem")

for pname, prob in problems:
    print(pname)
    plot_graph(prob[cols], pname)


