import pandas as pd 
import numpy as np

import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

cols1 = [
    "problem",
    "p1_e1",
    "p1_e2",
    "p1_e3",
    "p1_e4",
    "p2_e2",
    "p2_e3",
    "p2_e4",
    "p3_e3",
    "p3_e4",
    "p4_e4",
    "p4_e6",
    "p4_e8",
    "p4_e12",
    "p4_e16"
]

cols2 = [
    "problem",
    "p1_e1",
    "p1_e2",
    "p1_e3",
    "p1_e4",
]

cols3 = [
    "problem",
    "p1_e2",
    "p2_e2",
    "p3_e2",
    "p4_e2",
]

pgefile="table.txt"

def plot_graph(df, name):

    plt.figure()
    ax = df.plot.bar()

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    fig = ax.get_figure()
    fig.savefig('imgs/'+name+'.png')


pgefile=sys.argv[1]

df = pd.read_csv(pgefile, delim_whitespace=True)


df1 = orig[cols1]
plot_graph(df1,"speedup_1")

df2 = orig[cols2]
plot_graph(df2,"speedup_2")

df3 = orig[cols3]
plot_graph(df3,"speedup_3")







# probs = df.groupby("problem")

# for name, group in probs:
#     print(name)
#     # print(group)

#     # total = group.iloc[10]
#     # 11 korns_03/out 1066.5562 663.3041 499.1974 443.6554 817.5235 570.0893 396.5658 340.222 844.5291 419.0411 860.9846 429.665 730.2238 637.1927 618.7788 457.5316 261.5758 268.1977 347.4204 385.6246 268.5382 

#     print(group)

#     plt.figure()
        
#     # ax = total.plot.area(stacked=False)
#     # ax = total.plot(kind="bar")
#     ax = group.plot.bar()

#     # Shrink current axis by 20%
#     box = ax.get_position()
#     ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

#     # Put a legend to the right of the current axis

#     ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

#     fig = ax.get_figure()
#     fig.savefig('imgs/'+name+'.png')









    # lv2 = group.groupby("group")

    # first = True
    # fs = []
    # for name2, group2 in lv2:
    #     mid = group2.set_index(["iteration"])
    #     if first:
    #         mid = mid[[ "problem", "elapsed_seconds" ]]
    #         first = False
    #     else:
    #         mid = mid[[ "elapsed_seconds"]]
        
    #     # print(mid)
    #     fs.append(mid)

    # lv2_fin = pd.concat(fs, axis=1, ignore_index=True)

    # for i in range(0,11):
    #     row = lv2_fin.iloc[i]
    #     for item in row:
    #         print( item, end=" " )
    #     print("")
    # print("")

    # break


# print(df2)
