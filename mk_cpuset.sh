#!/bin/sh

BASE=/dev/cpuset
NAME=$1  ; shift
CORES=$1; shift
CMD=$*

test -z "$CMD"      && echo "no cmd"
test -z "$CMD"      && exit 1

test -d $BASE       || echo "cpuset not available"
test -d $BASE       || exit 1

test -d $BASE/$NAME || mkdir $BASE/$NAME

echo "$CORES" | sudo tee -a $BASE/$NAME/cpuset.cpus
echo "$CORES" | sudo tee -a $BASE/$NAME/cpuset.mems
echo "$$"     | sudo tee -a $BASE/$NAME/tasks
exec $cmd

