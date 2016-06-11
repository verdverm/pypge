from pypge.benchmarks import diffeqs

import numpy as np

# visualization libraries
import matplotlib.pyplot as plt



# Set your output directories
img_dir = "../img/diffeqs/"
data_dir = "../benchmarks/diffeqs/"

names = [
	"yeast",
]

def get_generator(name):
	if name == "yeast":
		return diffeqs.YeastMetabolism



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




