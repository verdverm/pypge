#!/bin/bash

# https://github.com/docker/docker/issues/8710

docker run -it --rm \
    --name postproc \
    -v $HOME/pypge:/pycode \
    -v $HOME/dissertation_output:/dissertation_output \
	-e DISPLAY=192.168.99.1:0 \
    -p 8080:8080 \
    verdverm/pypge /bin/bash
