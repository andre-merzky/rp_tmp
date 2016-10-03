
BASE=/dev/cpuset

test -d $BASE || (
    mkdir $BASE
    sudo mount -t cpuset none $BASE
    )

test -d $BASE/single || (
    mkdir       $BASE/single
    echo 0   >> $BASE/single/cpuset.cpus
    echo 0   >> $BASE/single/cpuset.mems 
    )

echo $$ >> $BASE/single/tasks 

