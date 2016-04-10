#!/bin/bash

instance=$1
region="--zone ${2:-us-central1-c}"
gcloud compute copy-files $region $instance:/home/tony/* $HOME/dissertation_output/$instance

