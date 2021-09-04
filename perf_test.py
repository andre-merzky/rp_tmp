#!/usr/bin/env python

import zmq
import time
import threading       as mt
import multiprocessing as mp

mode     = ['io', 'cpu', 'mix']
mode     = ['io']

cpusets  = {'/single' : 1,
            '/dual'   : 2,
            '/quad'   : 4,
            '/'       : 8}
myset    = open('/proc/self/cpuset', 'r').read().strip()
C        = cpusets[myset]
N        = 2

LOAD_CPU = 1000 * 1000 * 1000
load_cpu = LOAD_CPU / N

LOAD_IO  = 20 * 1000 * 1000
load_io  = LOAD_IO / N


# ------------------------------------------------------------------------------
#
def workload_io(nio, uid):
  # if uid % 2: read(uid, nio)
  # else      : write(uid, nio)
    if uid % 2: send(uid, nio)
    else      : recv(uid, nio)


def read(uid, nio):
    nio *= 2
    with open('/tmp/in.dat', 'r') as f:
        for cnt in range(nio + 1):
            f.read(1)


def write(uid, nio):
    nio *= 2
    with open('/tmp/out.dat', 'w') as f:
        for cnt in range(nio + 1):
            f.write('%d' % cnt)


def send(uid, nio):
    port       = 5000 + uid
    context    = zmq.Context()
    socket     = context.socket(zmq.PUSH)
    socket.connect("tcp://127.0.0.1:%d" % port)

    for cnt in range(nio + 1):
        socket.send('%d' % cnt)


def recv(uid, nio):
    port       = 5000 + uid + 1
    context    = zmq.Context()
    socket     = context.socket(zmq.PULL)
    socket.bind("tcp://127.0.0.1:%d" % port)

    cnt = 0
    while cnt < nio:
        cnt = int(socket.recv())


# ------------------------------------------------------------------------------
#
def workload_cpu(load, uid):
    while load > 0:
        load -= 1


# ------------------------------------------------------------------------------
#
def workload_mix(ncpu, nio, uid):
    if   (uid % 4) == 0: workload_cpu(ncpu, uid)
    elif (uid % 4) == 1: workload_cpu(ncpu, uid)
    elif (uid % 4) == 2: workload_io (nio,  uid)
    elif (uid % 4) == 3: workload_io (nio,  uid)


# ==============================================================================
#
if 'cpu' in mode:
    # --------------------------------------------------------------------------
    #
    start = time.time()
    for n in range(N):
        workload_cpu(load_cpu, n)
    stop = time.time()
    print('sequential cpu %d @ %d: %5.1f' % (N, C, stop - start))


    # --------------------------------------------------------------------------
    #
    start = time.time()
    threads = list()
    for n in range(N):
        threads.append(mt.Thread(target=workload_cpu, args=[load_cpu, n]))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    stop = time.time()
    print('threaded   cpu %d @ %d: %5.1f' % (N, C, stop - start))


    # --------------------------------------------------------------------------
    #
    start = time.time()
    procs = list()
    for n in range(N):
        procs.append(mp.Process(target=workload_cpu, args=(load_cpu, n)))
    for t in procs:
        t.start()
    for t in procs:
        t.join()
    stop = time.time()
    print('processed  cpu %d @ %d: %5.1f' % (N, C, stop - start))


# ==============================================================================
#
if 'io' in mode and N >= 2:
    # --------------------------------------------------------------------------
    #
    start = time.time()
    threads = list()
    for n in range(N):
        threads.append(mt.Thread(target=workload_io, args=[load_io, n]))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    stop = time.time()
    print('threaded   i/o %d @ %d: %5.1f' % (N, C, stop - start))


    # --------------------------------------------------------------------------
    #
    start = time.time()
    procs = list()
    for n in range(N):
        procs.append(mp.Process(target=workload_io, args=(load_io, n)))
    for t in procs:
        t.start()
    for t in procs:
        t.join()
    stop = time.time()
    print('processed  i/o %d @ %d: %5.1f' % (N, C, stop - start))


# ==============================================================================
#
if 'mix' in mode and N >= 4:

    # --------------------------------------------------------------------------
    #
    start = time.time()
    threads = list()
    for n in range(N):
        threads.append(mt.Thread(target=workload_mix,
                                 args=(load_cpu, load_io, n)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    stop = time.time()
    print('threaded   mix %d @ %d: %5.1f' % (N, C, stop - start))


    # --------------------------------------------------------------------------
    #
    start = time.time()
    procs = list()
    for n in range(N):
        procs.append(mp.Process(target=workload_mix,
                                args=(load_cpu, load_io, n)))
    for t in procs:
        t.start()
    for t in procs:
        t.join()
    stop = time.time()
    print('processed  mix %d @ %d: %5.1f' % (N, C, stop - start))


# ------------------------------------------------------------------------------

