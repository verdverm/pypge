import pandas as pd 
import sys

pgefile=sys.argv[1]

df = pd.read_csv(pgefile, delim_whitespace=True)

df2 = df[sys.argv[2:]]

pge = df2.groupby("problem")

for name, grp in pge:
	# print(name)
	# print(grp)

	ac_t = grp["elapsed_seconds"].iloc[2]/grp["elapsed_seconds"].iloc[0] 
	ac_m = grp["evald_models"].iloc[2]/grp["evald_models"].iloc[0]
	ac_r = ac_m / ac_t 
	bd_t = grp["elapsed_seconds"].iloc[3]/grp["elapsed_seconds"].iloc[1] 
	bd_m = grp["evald_models"].iloc[3]/grp["evald_models"].iloc[1] 
	bd_r = bd_m / bd_t 
	fstr = "{:21s}  &  {:.2f}  &  {:.2f}  &  {:.2f}  &  {:.2f}  &  {:.2f}  &  {:.2f}"
	out = fstr.format(name, ac_t, ac_m, ac_r, bd_t, bd_m, bd_r)
	print(out)
	# print(name, ac_t)
	# print(name, ac_t, ac_m, ac_r, bd_t, bd_m, bd_r)


print("\n\n")
for name, grp in pge:
	# print(name)
	# print(grp)

	r2 = grp["best_r2"]
	fstr = "{:21s}  &  {:.3f}  &  {:.3f}  &  {:.3f}  &  {:.3f}"
	out = fstr.format(name, r2.iloc[0], r2.iloc[1], r2.iloc[2], r2.iloc[3])
	print(out)

print("\n\n")
for name, grp in pge:
	# print(name)
	# print(grp)

	r2 = grp["ave_size"]
	fstr = "{:21s}  &  {:.0f}  &  {:.0f}  &  {:.0f}  &  {:.0f}"
	out = fstr.format(name, r2.iloc[0], r2.iloc[1], r2.iloc[2], r2.iloc[3])
	print(out)
