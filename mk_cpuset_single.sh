#!/bin/sh

BASE=/dev/cpuset
NAME=single
CORES=0

test -d $BASE || (
    mkdir $BASE
    sudo mount -t cpuset none $BASE
    )

test -d $BASE/$NAME || (
    mkdir          $BASE/$NAME
    echo $CORES >> $BASE/$NAME/cpuset.cpus
    echo 0      >> $BASE/$NAME/cpuset.mems 
    )

echo $$ >> $BASE/$NAME/tasks 

