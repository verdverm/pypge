import pandas as pd 
import numpy as np
# import matplotlib.pyplot as plt


pgefile="table.txt"

df = pd.read_csv(pgefile, delim_whitespace=True)

# print(df.columns)

df2 = df[[ "problem", "iteration", "group", "ave_size", "best_err", "best_r2", "total_point_evals" ]]

pge = df2.groupby("problem")

for name, group in pge:
    # print(name)
    # print(group)

    lv2 = group.groupby("group")

    first = True
    fs = []
    for name2, group2 in lv2:
        mid = group2.set_index(["iteration"])
        if first:
            mid = mid[[ "problem", "ave_size", "best_r2", "total_point_evals" ]]
            first = False
        else:
            mid = mid[[ "ave_size", "best_r2", "total_point_evals" ]]
        
        # print(mid)
        fs.append(mid)

    lv2_fin = pd.concat(fs, axis=1, ignore_index=True)

    for i in range(0,24):
        row = lv2_fin.iloc[i]
        for item in row:
            print( item, end=" " )
        print("")
    print("")

    # break


# print(df2)
