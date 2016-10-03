
# Motivating the RP Architecture Evolution

## What is RP?  (Main Objectives)

  - RP is a system which performs a series of 
    operations on certain entities (Pilots, CUs, [DUs]):
  
      - Pilot:
        - create
        - submit
        - bootstrap
        - run
        - finalize
    
      - CUs:
        - create
        - bind to pilot
        - stage data
        - assign to core(s)
        - execute and collect
        - stage data
        - finalize


  - RP is a framework + API which is supports application level
    decisions on the ordering and details of the above operations

    - this implies timely information flow from RP (and below) to
      the application


## Performance Constraints

  - handle a few pilots, but *many* CUs.
  - many ops are I/O bound
  - some ops are CPU bound 
    - scheduling many units (most relevant ATM)
    - compressing data 
    - string parsing
    - event filtering
  
  
## Architecture Constraints
  
  - heterogeneous, distributed resources
  - all software lives in userspace
    - no system services
    - no persistent entities
    - submission host might be a small machine
    - network connectivity might be high latency / low bandwidth
    - data can originally sit anywhere
  - API and upper layer of RP in Python
  
  - we will not solve:
    - data transfer over weak links
    - tunnelling through firewalls
    - application / CU level issues (concurrency, logic, performance)
  
  
## Architecture Options:
  
  - tight loop / event loop: single thread, single process
    - see nodejs -- can be fast
    - blocks on data staging (parts of I/O blocking can be handled)
    - blocks on CPU bound activity
    - notifications are late or pull based
    - doubtful it scales with #Pilots/#CUs (at least not in Python)
    --> Ugh, no.

  
  - multithreading

    - op and entity concurrency easy
    - notification flow to application easy (callbacks)

    - Python supports multithreading, but

      - thread-safety is impossibly
        - no sys.exit()  :  https://bugs.python.org/issue6634  (08/2009) 
        - no termination :  https://bugs.python.org/issue23395 (02/2015)
                            https://bugs.python.org/issue21963 (07/2014)
        - non-detacheable:  https://bugs.python.org/issue21963 (07/2014) 
      --> detour 'threads_and_signals.txt'

      - performance *decreases* with threading
      --> detour 'threading_in_python.txt'


  - multiprocessing

    - performance is great
    --> detour 'threading_in_python.txt'

    - concurrency on ops and entities is not simple, but ok
    - information flow to application is not simple either (comm channel)
      - mix with threading / callbacks is *hard*

    - Python supports multiprocessing, but
      - it is broken beyond redemption
        - zombification  : https://bugs.python.org/issue24862 (08/2015)
        - uninterruptable: https://bugs.python.org/issue21895 (07/2014)
                           https://bugs.python.org/issue27889 (08/2016)
        - unthreadable   : https://bugs.python.org/issue23395 (02/2015)
                           https://bugs.python.org/issue21963 (07/2014)
        - segfaulting    : https://bugs.python.org/issue1856  (01/2008)

    - some of the problems can be avoided by fork/exec
      - this would be unexpected for a library
      - solves some of the locking problems
      - signaling and termination problems mostly remain


## Observations:
    
  - Python will not be fixed
  - problems are systematic (almost intentional)
  - C-based (or whatever-based) module implementations cannot 
    significantly improve things


## Ways forward?  (ordered by increased effort)

  - Ignorance:
    - remove all workarounds, use Python as documented
    - code is simple (well, simpler), but unstable and sometimes slow
    - never use for production

  - Acceptance:
    - document shortcomings
    - work around them where architecture / code quality is not compromised
    - never use for production

  - Defiance:
    - attempt to fix in Python
    - this is possible, but a project on its own, out of scope

  - Subversion:
    - drop the 'userspace' requirement: out-of-band deployment of services can
      avoid many of the problems
    - implies services on client and resource side
    - tradeoff between stable/simple and fast remains 
      -> not great for production

  - Capitulation
    - start over in whatever language
    - wrap API in Python (for those poor souls who use Python :P)


