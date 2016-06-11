from pypge.benchmarks import explicit

import numpy as np

# visualization libraries
import matplotlib.pyplot as plt



# Set your output directories
img_dir = "../img/explicit/"
data_dir = "../benchmarks/explicit/"

names = [
	"koza_01",
	"koza_02",
	"koza_03",
	"lipson_01",
	"lipson_02",
	"lipson_03",
	"nguyen_01",
	"nguyen_02",
	"nguyen_03",
	"nguyen_04",
	"nguyen_05",
	"nguyen_06",
	"nguyen_07",
	"nguyen_08"
]

def get_generator(name):
	if name == "koza_01":
		return explicit.Koza_01
	elif name == "koza_02":
		return explicit.Koza_02
	elif name == "koza_03":
		return explicit.Koza_03
	elif name == "lipson_01":
		return explicit.Lipson_01
	elif name == "lipson_02":
		return explicit.Lipson_02
	elif name == "lipson_03":
		return explicit.Lipson_03
	elif name == "nguyen_01":
		return explicit.Nguyen_01
	elif name == "nguyen_02":
		return explicit.Nguyen_02
	elif name == "nguyen_03":
		return explicit.Nguyen_03
	elif name == "nguyen_04":
		return explicit.Nguyen_04
	elif name == "nguyen_05":
		return explicit.Nguyen_05
	elif name == "nguyen_06":
		return explicit.Nguyen_06
	elif name == "nguyen_07":
		return explicit.Nguyen_07
	elif name == "nguyen_08":
		return explicit.Nguyen_08



def output_graphs(prob):
	fig = plt.figure()
	fig.set_size_inches(16, 12)

	plt.plot(prob['xpts'][0], prob['ypure'], 'r.')
	plt.legend(loc='center left', bbox_to_anchor=(0.67, 0.12))

	plt.title(prob['name'] + " Clean", fontsize=36)
	plt.savefig(img_dir + prob['name'].lower() + "_clean.png", dpi=200)

	fig = plt.figure()
	fig.set_size_inches(16, 12)

	plt.plot(prob['xpts'][0], prob['ypts'], 'b.')
	plt.legend(loc='center left', bbox_to_anchor=(0.67, 0.12))

	plt.title(prob['name'] + " Noisy", fontsize=36)
	plt.savefig(img_dir + prob['name'].lower() + "_noisy.png", dpi=200)



def output_data(prob,ypts,label):
	data = np.array([prob['xpts'][0],ypts]).T

	cols = [['x', 'out']]
	out_data = cols + data.tolist()

	f_csv = open(data_dir + prob['name'].lower() + "_" + label + ".csv", 'w')
	for row in out_data:
	    line = ", ".join([str(col) for col in row]) + "\n"
	    f_csv.write(line)
	f_csv.close()


for name in names:
	print(name)
	gen = get_generator(name)
	prob = gen(noise=0.025, npts=1000)
	output_graphs(prob)
	output_data(prob, prob['ypure'], 'clean')
	output_data(prob, prob['ypts'], 'noisy')




