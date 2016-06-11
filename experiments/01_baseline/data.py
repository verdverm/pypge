from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import pandas as pd


explicit_problems=[
	"koza_01;out",
	"koza_02;out",
	"koza_03;out",
	"lipson_01;out",
	"lipson_02;out",
	"lipson_03;out",

	"nguyen_01;out",
	"nguyen_02;out",
	"nguyen_03;out",
	"nguyen_04;out",
	"nguyen_05;out",
	"nguyen_06;out",
	"nguyen_07;out",
	"nguyen_08;out",
	"nguyen_09;out",
	"nguyen_10;out",
	"nguyen_11;out",
	"nguyen_12;out",

	"korns_01;out",
	"korns_02;out",
	"korns_03;out",
	"korns_04;out",
	"korns_05;out",
	"korns_06;out",
	"korns_07;out",
	"korns_08;out",
	"korns_09;out",
	"korns_10;out",
	"korns_11;out",
	"korns_12;out",
	"korns_13;out",
	"korns_14;out",
	"korns_15;out",
]

diffeq_problems=[
	"bacresp;D_x",
	"bacresp;D_y",
	"barmags;D_X",
	"barmags;D_Y",
	"ecoli;D_G",
	"ecoli;D_A",
	"ecoli;D_L",
	"lorenz;D_x",
	"lorenz;D_y",
	"lorenz;D_z",
	"vanderpol;D_x",
	"vanderpol;D_y",
	"lotkavolterra;D_x",
	"lotkavolterra;D_y",
	"predpreyfrac;D_x",
	"predpreyfrac;D_y",
	"simplependulum;D_A",
	"simplependulum;D_V",
	"chaoticpendulum;D_A",
	"chaoticpendulum;D_V",
]

DATA_DIR = "../../data/benchmarks/"






# 2. read and setup data
# -----------------------

def read_datafile(systype,probname):
	fn = DATA_DIR + systype + "/" + probname + "_clean.csv"
	df = pd.read_csv(fn, skipinitialspace=True)
	return df


