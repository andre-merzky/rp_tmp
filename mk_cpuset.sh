
BASE=/dev/cpuset

test -d $BASE || (
    mkdir $BASE
    sudo mount -t cpuset none $BASE
    )

test -d $BASE/quad || (
    mkdir       $BASE/quad
    echo 0-3 >> $BASE/quad/cpuset.cpus
    echo 0   >> $BASE/quad/cpuset.mems 
    )

echo $$ >> $BASE/quad/tasks 

