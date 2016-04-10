import pandas as pd 
import numpy as np
# import matplotlib.pyplot as plt


pgefile="table.txt"

df = pd.read_csv(pgefile, delim_whitespace=True)

# print(df.columns)

df2 = df[["problem", "iteration", "group", "elapsed_seconds"]]

pge = df2.groupby("problem")

headers = True
print("problem", end=" ")

for name, group in pge:
    name = name[:-4]

    # print(name)
    # print(group)

    lv2 = group.groupby("group")

    first = True
    fs = []
    for name2, group2 in lv2:
        name2 = name2[9:-4]
        name2 = name2.replace("000","")
        if headers:
            print(name2, end=" ")
        mid = group2.set_index(["iteration"])
        if first:
            # mid = mid[[ "problem", "elapsed_seconds" ]]
            first = False
        # else:
        #     mid = mid[[ "elapsed_seconds"]]
        
        mid = mid[[ "elapsed_seconds"]]
        # print(mid)
        fs.append(mid)

    headers = False
    print("")

    lv2_fin = pd.concat(fs, axis=1, ignore_index=True)

    row = lv2_fin.iloc[11]
    print(name, end=" ")
    for item in row:
        print( item, end=" " )
    print("")
 


# print(df2)
