from pypge.benchmarks import explicit

import numpy as np
import json

# visualization libraries
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import gridspec



# Set your output directories
img_dir = "../img/explicit/"
data_dir = "../benchmarks/explicit/"

names = [
	"Korns_01",
	"Korns_02",
	"Korns_03",
	"Korns_04",
	"Korns_05",
	"Korns_06",
	"Korns_07",
	"Korns_08",
	"Korns_09",
	"Korns_10",
	"Korns_11",
	"Korns_12",
	"Korns_13",
	"Korns_14",
	"Korns_15"
]

def get_generator(name):
	if name == "korns_01":
		return explicit.Korns_01
	elif name == "korns_02":
		return explicit.Korns_02
	elif name == "korns_03":
		return explicit.Korns_03
	elif name == "korns_04":
		return explicit.Korns_04
	elif name == "korns_05":
		return explicit.Korns_05
	elif name == "korns_06":
		return explicit.Korns_06
	elif name == "korns_07":
		return explicit.Korns_07
	elif name == "korns_08":
		return explicit.Korns_08
	elif name == "korns_09":
		return explicit.Korns_09
	elif name == "korns_10":
		return explicit.Korns_10
	elif name == "korns_11":
		return explicit.Korns_11
	elif name == "korns_12":
		return explicit.Korns_12
	elif name == "korns_13":
		return explicit.Korns_13
	elif name == "korns_14":
		return explicit.Korns_14
	elif name == "korns_15":
		return explicit.Korns_15


def output_graphs(prob):
	xs = prob['xpts'][0]
	ys = prob['xpts'][1]
	zs = prob['ypure']

	fig = plt.figure()
	fig.set_size_inches(16, 12)
	gs = gridspec.GridSpec(4, 2)
	fig.suptitle(prob['name'] + " Clean", fontsize=36)

	ax1 = fig.add_subplot(gs[0:2,:], projection='3d')
	ax1.scatter(xs, ys, zs, c='b', marker='.')
	ax1.set_xlabel('X')
	ax1.set_ylabel('Y')
	ax1.set_zlabel('Z')

	ax2 = fig.add_subplot(gs[2,:])
	ax2.scatter(xs, zs, marker='.')
	ax2.set_xlabel('X')
	ax2.set_ylabel('Z')

	ax3 = fig.add_subplot(gs[3,:])
	ax3.scatter(ys, zs, marker='.')
	ax3.set_xlabel('Y')
	ax3.set_ylabel('Z')
	plt.savefig(img_dir + prob['name'].lower() + "_clean.png", dpi=200)


	zs = prob['ypts']
	fig = plt.figure()
	fig.set_size_inches(16, 12)
	gs = gridspec.GridSpec(4, 2)
	fig.suptitle(prob['name'] + " Noisy", fontsize=36)

	ax = fig.add_subplot(gs[0:2,:], projection='3d')
	ax.scatter(xs, ys, zs, c='b', marker='.')
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')

	ax2 = fig.add_subplot(gs[2,:])
	ax2.scatter(xs, zs, marker='.')
	ax2.set_xlabel('X')
	ax2.set_ylabel('Z')

	ax3 = fig.add_subplot(gs[3,:])
	ax3.scatter(ys, zs, marker='.')
	ax3.set_xlabel('Y')
	ax3.set_ylabel('Z')
	plt.savefig(img_dir + prob['name'].lower() + "_noisy.png", dpi=200)



def output_noisy_data(prob):
	data = np.array([prob['xpts'][0],prob['xpts'][1],prob['xpts'][2],prob['xpts'][3],prob['xpts'][4], prob['ypts']]).T

	cols = [['x', 'y', 'z', 'v', 'w', 'out']]
	out_data = cols + data.tolist()
	out_data = cols + data.tolist()
	json_out = json.dumps( out_data, indent=4)
	# print json_out

	f_json = open(data_dir + prob['name'].lower() + "_noisy.json", 'w')
	f_json.write(json_out)
	f_json.close()

	f_csv = open(data_dir + prob['name'].lower() + "_noisy.csv", 'w')
	for row in out_data:
	    line = ", ".join([str(col) for col in row]) + "\n"
	    f_csv.write(line)
	f_csv.close()


def output_clean_data(prob):
	data = np.array([prob['xpts'][0],prob['xpts'][1],prob['xpts'][2],prob['xpts'][3],prob['xpts'][4], prob['ypure']]).T

	cols = [['x', 'y', 'z', 'v', 'w', 'out']]
	out_data = cols + data.tolist()
	out_data = cols + data.tolist()
	json_out = json.dumps( out_data, indent=4)

	f_json = open(data_dir + prob['name'].lower() + "_clean.json", 'w')
	f_json.write(json_out)
	f_json.close()

	f_csv = open(data_dir + prob['name'].lower() + "_clean.csv", 'w')
	for row in out_data:
	    line = ", ".join([str(col) for col in row]) + "\n"
	    f_csv.write(line)
	f_csv.close()


for name in names:
	gen = get_generator(name)
	prob = gen(noise=0.01)
	# output_graphs(prob)
	output_clean_data(prob)
	output_noisy_data(prob)




