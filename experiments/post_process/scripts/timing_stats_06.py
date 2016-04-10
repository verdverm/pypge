import pandas as pd 
import sys

pgefile=sys.argv[1]
field = sys.argv[2]
df = pd.read_csv(pgefile, delim_whitespace=True)

df2 = df[sys.argv[3:]]

pge = df2.groupby("problem")

for name, grp in pge:
	# print(grp)

	lhf = grp[field].iloc[0]
	lht = grp[field].iloc[1]
	lmf = grp[field].iloc[2]
	lmt = grp[field].iloc[3]
	mhf = grp[field].iloc[4]
	mht = grp[field].iloc[5]
	mmf = grp[field].iloc[6]
	mmt = grp[field].iloc[7]

	fstr = "{:21s}  &  {:5.0f}  &  {:5.0f}  &  {:5.0f}  &  {:5.0f}  &  {:5.0f}  &  {:5.0f}  &  {:5.0f}  &  {:5.0f}"
	out = fstr.format(name, lmf, lmt, lhf, lht, mmf, mmt, mhf, mht)
	print(out, sep="  &  ")
