import pandas as pd 
import sys

pgefile=sys.argv[1]

df = pd.read_csv(pgefile, delim_whitespace=True)

df2 = df[sys.argv[2:]]

pge = df2.groupby("problem")

for name, prob_group in pge:
    print(prob_group.to_latex())

