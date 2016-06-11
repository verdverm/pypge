#!/bin/bash

set -e 

# nocache="--no-cache"


# BUILD base docker
# docker build $nocache -t verdverm/pypge-base      base

# BUILD data docker
# cp -r ../data data
# docker build $nocache -t verdverm/pypge-data      data

# BUILD evaluator docker
# rm -rf eval/evaluator && cp -r ../evaluator eval/evaluator
docker build $nocache -t verdverm/pypge-eval      eval

# BUILD python, competitiors, and pypge dockers
docker build $nocache -t verdverm/pypge-python2   python2
docker build $nocache -t verdverm/pypge-python3   python3

docker build $nocache -t verdverm/pypge           pypge

