
  * Threads and Signals:

    - signal handlers on C-level do *not* clal back into Python 

      - instead, they set a flag, and the Python interpreter
        opportunistically checks for those flags (~100 op-codes)

            #include <signal.h>
            int  term_seen = 0;
            void term_handle(int signum) {
                 term_seen = 1;
                 }
            signal(SIGTERM, term_handle);


    - why Ctrl-C (SIGINT) doesn't work:
      
      - if the main thread blocks on an uninterruptible thread-join or
        lock, it never gets a Python-level signal handler scheduled.
        - logging uses locks
        - thread.join, process.wait, time.sleep, select -- all block

      - the interpreter soon attempts to thread-switch after *every*
        tick --> consume 100% CPU, grinds to a halt, never gets
        unlocked

            if interpreter.term_seen:
              while True:
                if main_thread.get_gil():
                  main_thread.deliver_signal(SIGINT, current_stack)

      - same holds for other signals (SIGTERM, SIGUSR, 

      - apart from that: SIGINT handler conflicts with thread
        ineterruption


