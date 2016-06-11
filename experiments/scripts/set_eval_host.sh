#/bin/bash

# how to use:
#
# set_eval_host.sh <host_ip,host_name>:<host_port>
#

host=$1
echo "changing host to $1"

cd ..
find . -name "*.yml" -exec sed -i '' 's|remote_host.*|remote_host: "ws://'${1}'/echo"|g' {} \;


