#!/bin/bash

# eval $(docker-machine env default)


docker run --rm -it --name pycode \
	-v `pwd`:/pycode \
	pypge/python3 \
	/bin/bash