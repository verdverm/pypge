import pandas as pd 
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

import sys



cols = [
    "group",
    "seconds",
    "models"
]

def plot_graph(df, name):
    N=len(df["group"])
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    # plt.figure()
    fig, ax1 = plt.subplots()

    ax1.bar(ind, df["models"], width, color='r');

    ax1.set_xlabel("group",fontsize=12)
    ax1.set_ylabel("models",fontsize=12)
    # ax1.set_yscale('log')
    ax1.grid(b=False)

    ax2 = ax1.twinx()
    ax2.bar(ind + width, df["seconds"], width);
    ax2.set_ylabel("seconds",fontsize=12)
    ax2.grid(b=False)

    ax1.set_xticks(ind + width)
    ax1.set_xticklabels(df["group"], rotation=45,fontsize=12)

    # locs, labels = plt.xticks()
    # ax1.setp(labels, rotation=45,fontsize=12)

    # Shrink current axis by 20%
    box = ax1.get_position()
    ax1.set_position([box.x0, box.y0 + box.height * 0.2, box.width * 0.8, box.height * 0.8])
    ax2.set_position([box.x0, box.y0 + box.height * 0.2, box.width * 0.8, box.height * 0.8])

    # Put a legend to the right of the current axis
    # ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))


    fig.savefig('imgs/progressive_expansion/'+name+'.png')
    fig.savefig('imgs/progressive_expansion/'+name+'.pdf')


pgefile=sys.argv[1]


df = pd.read_csv(pgefile, delim_whitespace=True)

df["seconds"] = df["elapsed_seconds"]
df["models"] = df["evald_models"]

problems = df.groupby("problem")

for pname, prob in problems:
    print(pname)
    plot_graph(prob[cols], pname)

