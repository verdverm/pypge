lol = []
vvs = []
with open("yeast2000.txt") as the_file:
	first = True
	idx = 0
	cnt = 0
	lcnt = 0
	var = []
	for line in the_file:
		ll = [item.strip() for item in line.split()]
		lcnt += 1

		if first:
			lol.append(ll[:len(ll)-2])
			first = False
			continue

		var.append(ll)
		cnt += 1
		if cnt == 200:
			cnt = 0
			vv = [item for sublist in var for item in sublist]
			vvs.append(vv)
			var = []
			print "flattening", lol[0][idx], idx, len(vv), lcnt
			if len(vvs) == 8:
				break
			idx += 1

for i in range(len(vvs[0])):
	ll = [float(vvs[j][i]) for j in range(len(vvs))]
	lol.append(ll)

import json
str_data = json.dumps(lol, indent=2)

with open('yeast.json', 'w') as the_file:
	the_file.write(str_data)
