import pandas as pd 
import sys

pgefile=sys.argv[1]
field=sys.argv[2]

df = pd.read_csv(pgefile, delim_whitespace=True)

df2 = df[sys.argv[3:]]

pge = df2.groupby("problem")

print(" Problem      &  A-1-1  & A-1-2  & A-2-1  & A-2-2 &  P-1-1  & P-1-2  & P-2-1  & P-2-2 ")

for name, grp in pge:
	# print(name)

	r2 = grp[field]
	fstr = "{:21s}  &  {:.3f}  &  {:.3f}  &  {:.3f}  &  {:.3f}  &  {:.3f}  &  {:.3f}  &  {:.3f}  &  {:.3f}"
	out = fstr.format(name, r2.iloc[0], r2.iloc[1], r2.iloc[2], r2.iloc[3], r2.iloc[4], r2.iloc[5], r2.iloc[6], r2.iloc[7])
	print(out)
