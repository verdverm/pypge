from __future__ import print_function

import sys, os, time

import argparse
import yaml

import pandas as pd
import numpy as np


# 0. Setup CLI args
# -----------------------
parser = argparse.ArgumentParser()

parser.add_argument("-t", "--timing", help="output timing details", action="store_true")

func_choices = ["linear","nonlin"]
level_choices = ["low","med","high"]
parser.add_argument("--func_level", help="complexity of initial models", choices=func_choices)
parser.add_argument("--init_level", help="complexity of initial models", choices=level_choices)
parser.add_argument("--grow_level", help="complexity of model expansion", choices=level_choices)
parser.add_argument("--target", help="target variable to regress")
# parser.add_argument("--iterations", help="number of iterations to run the search for")


parser.add_argument("config", help="a YAML configuration file")
parser.add_argument("input", help="input data file [csv,json]")
parser.add_argument("output", help="output directory")

args = parser.parse_args()
# print args




# 1a. reading config file 
# -----------------------
cf = open(args.config, "r")
config = yaml.load(cf)
cf.close()
print(config)

# 1a. override config with args
# -----------------------
if args.func_level is not None:
	config["func_level"] = args.func_level
if args.init_level is not None:
	config["init_level"] = args.init_level
if args.grow_level is not None:
	config["grow_level"] = args.grow_level


# 2. read and setup data
# -----------------------
df = None
if args.input[-4:] == ".csv":
	df = pd.read_csv(args.input, skipinitialspace=True)
else:
	print("Unknown input data file type")

# print df.columns


target = df.columns[-1]
if args.target is not None:
	if args.target in df.columns:
		target = args.target
	else:
		sys.exit("target not found") 

cols = [col for col in df.columns if not (col == target or col in config["excluded_cols"])]

print("ins:", cols)
print("target:", target)

ins = df[cols].as_matrix().T
outs = df[target].values

normOuts = outs / np.linalg.norm(outs)


print(ins.shape)
print(outs.shape)
print(normOuts.shape)




# 3. setup output directory
# -----------------------
directory = args.output
if not os.path.exists(directory):
    os.makedirs(directory)
if directory[-1] != '/':
    directory += '/'



# 4. setup PGE
# -----------------------


from pypge.search import PGE
from pypge import expand
from pypge import fitness_funcs as FF
import sympy


pge = PGE(
    search_vars = target,
    usable_vars = cols,
    log_dir=directory,

    ## unpack config values
    **config
)


print(pge)


# sys.exit("DEVELOPER ROAD BLOCK")



# 5. run PGE
# -----------------------

start = time.time()

pge.fit(ins,normOuts)

end = time.time()
print("\n\nTotal Runtime: ", end - start, "seconds\n\n")
