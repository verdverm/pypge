import sys, os, time

import argparse
import yaml

import pandas as pd


# 0. Setup CLI args
# -----------------------
parser = argparse.ArgumentParser()

parser.add_argument("-t", "--timing", help="output timing details", action="store_true")

depth_choices = ["low","med","high"]
parser.add_argument("--init_depth", help="complexity of initial models", choices=depth_choices)
parser.add_argument("--expand_depth", help="complexity of model expansion", choices=depth_choices)


parser.add_argument("--target", help="the target variable")

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
print config

# 1a. override config with args
# -----------------------
if args.init_depth is not None:
	config["init_depth"] = args.init_depth
if args.expand_depth is not None:
	config["expand_depth"] = args.expand_depth


# 2. read and setup data
# -----------------------
df = None
if args.input[-5:] == ".json":
	df = pd.read_json(args.input)
elif args.input[-4:] == ".csv":
	df = pd.read_csv(args.input)
else:
	print "Unknown input data file type"

# print df.columns

target = df.columns[-1]
if args.target is not None:
	if args.target in df.columns:
		target = args.target
	else:
		sys.exit("target not found") 

cols = [col for col in df.columns if col != target]

print "ins:", cols
print "target:", target

ins = df[cols].as_matrix().T
outs = df[target].values

print ins.shape
print outs.shape




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
    system_type = config["system_type"],
    search_vars = target,
    usable_vars = cols,
    # usable_funcs = [sympy.exp, sympy.cos, sympy.sin, sympy.Abs],
    init_depth = config["init_depth"],
    expand_depth = config["expand_depth"],
    algebra_methods = config["algebra_methods"],
    pop_count = config["pop_count"],
    peek_count = config["peek_count"],
    peek_npts = config["peek_npts"],
    max_iter = config["max_iter"],
    print_timing = config["print_timing"],
    log_details = config["log_details"],
    log_dir=directory,
    fitness_func = FF.normalized_size_score
)


# sys.exit("DEVELOPER ROAD BLOCK")



# 5. run PGE
# -----------------------

start = time.time()

pge.fit(ins,outs)

end = time.time()
print "\n\nTotal Runtime: ", end - start, "seconds\n\n"
