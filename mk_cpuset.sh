
BASE=/dev/cpuset
UID=$1  ; shift
CORES=$1; shift
CMD=$*

test -z "$CMD"     && echo "no cmd"
test -z "$CMD"     && exit 1

test -d $BASE      || echo "cpuset not available"
test -d $BASE      || exit 1

test -d $BASE/$UID || mkdir $BASE/$UID

echo "$CORES" >> $BASE/$UID/cpuset.cpus
echo "$CORES" >> $BASE/$UID/cpuset.mems
echo "$$"     >> $BASE/$UID/tasks
exec $cmd

