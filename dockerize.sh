#!/bin/bash

# eval $(docker-machine env default)


docker run --rm -it --name yeast \
	-v `pwd`:/pycode \
	-p 8888:8888 \
	verdverm/pypge-experiments \
	/bin/bash
