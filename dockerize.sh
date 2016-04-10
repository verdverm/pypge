#!/bin/bash

# eval $(docker-machine env default)


docker run --rm -it --name yeast \
	-v `pwd`:/pycode \
	verdverm/pypge \
	/bin/bash