# pypge

[![Build Status](https://travis-ci.org/verdverm/pypge.svg)](https://travis-ci.org/verdverm/pypge)
[![PyPI](https://img.shields.io/pypi/v/pypge.svg)](https://pypi.python.org/pypi/pypge)
[![PyPI](https://img.shields.io/pypi/dm/pypge.svg)](https://pypi.python.org/pypi/pypge)


Python implementation of the [PGE algorithm](http://dl.acm.org/citation.cfm?id=2463486) 
(voted Best Paper Gecco 2013)

If you publish using this library, please cite the above paper.

PGE stands for Prioritized Grammar Enumeration and is *the* method for solving the Symbolic Regression problem. 

__This package is under heavy development until this comment is removed__


### Installation

Clone the repository.

_Pip is no longer the recommended method._

#### Dependencies

Docker.


### Running PyPGE

You will want to run an evaluation server, runtime is much better this way.

`docker run -d -p 8080:8080 --name evalr verdverm/pypge-eval`

Then you can run the experimenter container:

```
docker run --rm -it --name pypge \
	-v `pwd`:/pycode \
	-p 8888:8888 \
	verdverm/pypge-experiments \
	/bin/bash
```

You will find a `run.sh` bash script.
Running from within the docker is the best place to run pypge at the moment.
There is a lot of parameteriztion matching that happens behind the scenes.
Much of the configuration change and file moving can happen outside of
the docker because we mount the repository into the docker.
All scripts should be run from inside, however,
out put will also persist outside of the container.


`run -x <config_folder> -s <problem_type> -p <problem_set>`

The `<config_folder>` should contain one or more yaml configuration files.

The `<problem_type>` must be `explicit` or `diffeq`.
Your yaml config filenames must contain one of these strings.

The `<problem_set>` is a file in the `prob_sets` directory
and is a simple bash list.

You can also use the `-P` option to see what experiments will be performed 
without actually running anything.

##### Running Directly

For those interested, follow the flow:

```
experiments/megarun.sh
experiments/run.sh
experiments/scripts/helpers.sh
experiments/main.py
```


### Create a New Experiment

Right now, namimg is a bit intertwined with the configuration
and where PyPGE run script looks for different files and directories.

You will need to create a directory in the experiments folder.
It's name should match the `<config_folder>` arg.
Inside of this folder, you will have your config files for PyPGE.

You will need to place your data in the 
`data/benchmarks/{diffeq,explicit}/<problem_name>.csv`

You will also need to create a `<problem_set>` in the `experiments/prob_sets`


#### Config files

These are the recommended default settings.
You should change the workers and remote cores to match the
machine you are using.
Be careful when changing other parameters.
Both logical and runtime performance
are very sensative.

Sample config file:

```
name: "explicit_final"

workers: 4
queue_size: 4096
remote_eval: true
remote_cores: 4
remote_host: "ws://172.17.0.1:8080/echo"

max_iter: 12

pop_count: 3
peek_count: 12
peek_npts: 0

min_size: 1
max_size: 64
min_depth: 1
max_depth: 6

max_power: 6
zero_epsilon: 0.000001

excluded_cols: []

usable_funcs: []
 - "sin"
 - "cos"

algebra_methods: []

multi_expander_params:
  - name: "level_1"
    pop_count: 3
    usable_funcs: 
     - "sin" 
     - "cos"
    grow_params:
      func_level: "linear"
      init_level: "med"
      grow_level: "med"
      subs_level: "med"
      shrinker: false
      add_xtop: true
      grow_filter: false
      limiting_depth: 4

err_method: "rmse"

fitness_func_params:
 - "normalize" 
 - "-(1)jpsz" 
 - "-score" 
 - "+bic"
 - "-(1)psz" 


print_timing: true
log_details: true
```

### Things to know

* When pretty printing, sympy performs simplification, which can remove terms if the floating point print precision is not sufficient (looks like __zero__)

### Todo

The biggest todo on my list is moving the main loop
back to Golang. Python will then only be used for the SymPy functionality.

The reason for this is that Python is slow as shit
and there will be a massive performance boost by switching back to Golang.

_Sometimes implementation matters._


### Contributing

Branching practices follow the methodology outlined at: http://nvie.com/posts/a-successful-git-branching-model/


