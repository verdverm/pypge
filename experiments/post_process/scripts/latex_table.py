import pandas as pd 
import sys

pgefile=sys.argv[1]

df = pd.read_csv(pgefile, delim_whitespace=True)

df2 = df[sys.argv[2:]]

print(df2.to_latex())
