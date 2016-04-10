import pandas as pd 
import numpy as np
# import matplotlib.pyplot as plt


pgefile="table.txt"

df = pd.read_csv(pgefile, delim_whitespace=True)

df2 = df[["problem", "ave_size", "ave_err", "ave_r2", "best_err", "best_r2"]]

print(df2.to_latex())
