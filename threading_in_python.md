
# Multithreading in Python

## Python natively supports threads
  
  - Python threads are actual system threads
  - all threads share a lock (GIL), only *one* thread is ever active
    - GIL locks   on libc calls, Python op-codes
    - GIL unlocks on I/O wait
    - GIL does *not* unlock on signals, events, exceptions, ...


  - interpreter switches threads:

        while True:

          OPCODE_MAX = 100
          waiting    = list()
          active     = None

          for thread in threads:
            if thread.is_waiting():
              waiting.append(thread)
            if thread.has_gil:
              active = thread

          if not waiting:
            # single threaded
            break

          sort(waiting, priority)

          # try to get gil:
          if not active.release_gil():
            # no luck, active remains active
            break

            active.release_gil()
          elif active.op_codes >= OPCODE_MAX:
            active.release_gil()
          else:
            active.op_codes += active.tick(max=OPCODE_MAX)
            break

          # the gil is released here
          waiting[0].get_gil()

  
  
    - thread_is_waiting()

      - implies a system call 'gil.lock()' in each thread

      - several threads on single core:
        - thread_1 unlocks
        - thread_2 locks
        - thread_1 locks -> wait

      - several threads on multiple cores:
        - thread_1 unlocks
        - OS communicates unlock to core_2
        - thread_1 locks
        - thread_2 locks -> wait

      - threads battle for GIL
      - CPU-bound threads always loose
      - a single CPU bound thread almost always wins
      - I/O threads are *slow* if any thread is CPU bound 
        - millions (!) of ticks before 'gil.lock()' succeeds


    - this is the case since about 20 years, well known and
      understood, and unlikely to change.  Holds for Python 2 and 3


## Simple Performance Experiments:

  - tools:
    - python 2.7, `time`, `threading`, `multiprocessing`
    - cpuset

  - workload:

    - cpu: simple counter

        def workload(load):
            while load > 0:
              load -= 1

    - i/o: read/write to file

        def workload(load):
            while load > 0:
              load -= 1

        # run n times serial
        N    = 4
        LOAD = 1000 * 1000 * 1000
        load = LOAD / N
        for n in range(N):
            workload(load)


   - results:

     - cpu bound

+--------+--------+--------+--------+--------+
| cores  |      N | serial | thread | procs  |
|        |        | sec    | sec    | sec    |
+--------+--------+--------+--------+--------+
|     1  |      1 |     29 |     31 |     33 |
|        |      2 |     27 |     30 |     29 |
|        |      4 |     33 |     33 |     31 |
+--------+--------+--------+--------+--------+
|     2  |      1 |     30 |     28 |     34 |
|        |      2 |     30 |     43 |     17 |
|        |      4 |     30 |     52 |     16 |
+--------+--------+--------+--------+--------+
|     4  |      1 |     29 |     30 |     31 |
|        |      2 |     29 |     46 |     15 |
|        |      4 |     29 |     55 |     11 |
+--------+--------+--------+--------+--------+
|     8  |      1 |        |        |        |
|        |      2 |        |        |        |
|        |      4 |     27 |     58 |     11 |
+--------+--------+--------+--------+--------+


    - io bound

      +--------+--------+--------+--------+--------+
      | cores  |      N | serial | thread | procs  |
      |        |        | sec    | sec    | sec    |
      +--------+--------+--------+--------+--------+
      |     1  |      1 |     -- |     -- |     -- |
      |        |      2 |     -- |     36 |     48 |
      |        |      4 |     -- |     37 |     54 |
      +--------+--------+--------+--------+--------+
      |     2  |      1 |     -- |     -- |     -- |
      |        |      2 |     -- |     23 |     30 |
      |        |      4 |     -- |     33 |     12 |
      +--------+--------+--------+--------+--------+
      |     4  |      1 |     -- |     -- |     -- |
      |        |      2 |     -- |     28 |      9 |
      |        |      4 |     -- |     38 |     10 |
      +--------+--------+--------+--------+--------+
      |     8  |      1 |     -- |     -- |     -- |
      |        |      2 |     -- |        |        |
      |        |      4 |     -- |     55 |     11 |
      +--------+--------+--------+--------+--------+


    - io / cpu mix

      +--------+--------+--------+--------+--------+
      | cores  |      N | serial | thread | procs  |
      |        |        | sec    | sec    | sec    |
      +--------+--------+--------+--------+--------+
      |     1  |      1 |     -- |     -- |     -- |
      |        |      2 |     -- |     -- |     -- |
      |        |      4 |     -- |     28 |     40 |
      +--------+--------+--------+--------+--------+
      |     2  |      1 |     -- |     -- |     -- |
      |        |      2 |     -- |     -- |     -- |
      |        |      4 |     -- |     35 |     19 |
      +--------+--------+--------+--------+--------+
      |     4  |      1 |     -- |     -- |     -- |
      |        |      2 |     -- |     -- |     -- |
      |        |      4 |     -- |     45 |     13 |
      +--------+--------+--------+--------+--------+
      |     8  |      1 |     -- |     -- |     -- |
      |        |      2 |     -- |     -- |     -- |
      |        |      4 |     -- |     55 |     13 |
      +--------+--------+--------+--------+--------+



