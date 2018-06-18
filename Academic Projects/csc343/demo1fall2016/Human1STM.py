# CSC343.template.txt, D. Parson, Fall 2013
# This file is a template for CSC343Compile.py that compiles a
# state machine into a Python simulation framework,
# for use in CSC 343 Operating Systems, beginning Fall 2013.
# See CSC343Compile.py and CSC343Sim.py.
# http://faculty.kutztown.edu/parson
# package state2codeV10

import os
import sys
import types
import random
import math
import operator
import functools
# ^^^ partial & reduce in 2.[67]
import traceback
from state2codeV10.CSC343Sim import __simulationScheduler__,                 \
    __ThreadRetireException__, _Processor_, _IOunit_, _Thread_,             \
    __simulationLogger__, gentestSampleDistribution, __scheduledObject__,   \
    Queue, _SubGraph_, __DEBUGLEVEL__

class processor(_Processor_):
    '''
    CSC343Compile.py generates the __init__ and run methods of
    class processor from a programmer-supplied state machine.
    '''
    def __init__(self, scheduler, logger, factory, contextLength,           \
            seed=None):
        '''
        Initialize variables from the state machine, and the contextCount,
        contextsFree, and fastio[] _IOunit_ fields, after calling the
        _Processor_ constructor.
        Parameter contextLength gives the number of contextCount & contextsFree
        (hardware thread) slots.
        See _Processor_'s constructor for the other parameters.
        Field fastiounits is the actual array of iounit objects
        for use in the processor's fastio[] vector. See setIOunits().
        '''
        _Processor_.__init__(self, scheduler, logger, factory,               \
            seed=seed)
        self.contextCount = contextLength
        self.contextsFree = contextLength
        self.__generator__ = self.run()     # Added August 2015
        if type(self.__generator__) != types.GeneratorType:
            raise AttributeError, ("ERROR, generated processor performs "
                + "no blocking operations, DEBUG info: "
                + str(type(self.__generator__)))
    def setIOunits(self, fastiounits):
        '''
        Set the fastio [] vector for this processor to fastiounits [].
        The constructor cannot do this because the iounit() constructor
        requires a reference to the processor; there is a circular
        dependency.
        '''
        self.fastio = fastiounits
    def run(self):
        '''
        This run() method runs the thread of the active processor object.
        CSC343Compile.py generates this method from a custom state machine.
        '''
        globals = {
            'math'      :   math,                   # module
            'functools' :   functools,              # module
            'operator'  :   operator,               # module
            'fork'      :   self.fork,              # method
            'idle'      :   self.idle,              # method
            'trigger'   :   self.trigger,           # method
            'time'      :   self.time,              # method
            'sample'    :   self.sample,            # method
            'msg'       :   self.msg,               # method
            'waitForEvent' : self.waitForEvent,     # method
            'signalEvent' : __scheduledObject__.signalEvent,       # method
            'assign'    :   self.assign,            # method
            'noop'      : __scheduledObject__.noop,       # method
            "pcb"       :   self.pcb,               # field
            "child"     :   self.child,             # field
            'fastio'    :   self.fastio,            # field
            'contextCount' : self.contextCount,     # field
            'contextsFree' : self.contextsFree,       # field
            'Queue'     :   Queue,                  # class
            'processor' :   self,                   # this object
            'self'      :   self                    # this object
        }
        self.globals = globals
        locals = {
            'threadsToGo' : 1,
        }
        self.__eventSet__ = set(['fork', 'init'])
        self.locals = locals
        __lastMissedEvent__ = None
        try:
            try:
                self.state = 'init'
                self.waitingon = 'init'
                self.logger.log(self, tag="APPROACH")
                self.logger.log(self, tag="ARRIVE")
                stime = None        # simulation time
                event = None        # event is the event that got us here
                args = None         # args are the args passed from event
                while True:         # processor runs until sys.exit.
                    if self.__sleepResult__:
                        stime, event, args = self.__sleepResult__
                        # DEPRECATED self.logger.log(self)
                    else:
                        stime = self.scheduler.time
                        event = None
                        args = None
                    # CSC343Compile.py generates custom run() code here.
                    if self.state == 'init':
                        if event == 'init':
                            self.logger.log(self, tag="DEPART")
                            self.state = 'makingThreads'
                            self.logger.log(self, tag="APPROACH")
                            exec('threadsToGo -= 1',globals,locals)
                            exec('fork()',globals,locals)
                            self.logger.log(self, tag="ARRIVE")
                            yield None
                            __lastMissedEvent__ = None
                            continue
                        if event != __lastMissedEvent__ and self.logger.getLevel() >= (__DEBUGLEVEL__-1):
                            self.msg("INFO: Missed event: " + event + " From state: " + self.state)
                            __lastMissedEvent__ = event
                    elif self.state == 'doneStartingThreads':
                        self.logger.log(self, tag="DEPART")
                        return
                    elif self.state == 'makingThreads':
                        if event == 'fork':
                            locals["pid"] = args[0]
                            locals["tid"] = args[1]
                            if eval('threadsToGo > 0',globals,locals):
                                self.logger.log(self, tag="REPEAT")
                                exec('threadsToGo -= 1',globals,locals)
                                exec('fork()',globals,locals)
                                yield None
                                __lastMissedEvent__ = None
                                continue
                        if event == 'fork':
                            locals["pid"] = args[0]
                            locals["tid"] = args[1]
                            if eval('threadsToGo == 0',globals,locals):
                                self.logger.log(self, tag="DEPART")
                                self.state = 'doneStartingThreads'
                                self.logger.log(self, tag="APPROACH")
                                self.logger.log(self, tag="ARRIVE")
                                __lastMissedEvent__ = None
                                continue
                        if event != __lastMissedEvent__ and self.logger.getLevel() >= (__DEBUGLEVEL__-1):
                            self.msg("INFO: Missed event: " + event + " From state: " + self.state)
                            __lastMissedEvent__ = event
            except Exception, xxx:
                if self.logger.isOpen():
                    self.logger.log(self)
                    self.state = '<defunct on Exception ' + str(xxx) + '>'
                    self.logger.log(self)
                    traceback.print_exc(file=self.logger.getFile())
                    self.logger.flush()
                    raise
        finally:
            if self.logger.isOpen() and not self.state.startswith('<defunct'):
                # DEPRECATED self.logger.log(self)
                self.state = '<defunct>'
                self.waitingon = None
                self.logger.log(self)
                self.logger.flush()
            # DEPRECATED self.scheduler.notifyOfTerminatingSimThread()
            # Unblock sched for another Python Thread.

class thread(_Thread_):
    '''
    CSC343Compile.py generates the __init__ and run methods of
    class thread from a programmer-supllied state machine.
    '''
    def __init__(self, scheduler, logger, factory, processor, pcb,          \
            processNumber, threadNumber, terminal, seed=None):
        '''
        See _Thread_.__init__ documentation for parameters.
        '''
        _Thread_.__init__(self, scheduler, logger, factory, processor,      \
            pcb, processNumber, threadNumber, terminal, seed=seed)
        self.__generator__ = self.run()     # Added August 2015
        if type(self.__generator__) != types.GeneratorType:
            raise AttributeError, ("ERROR, generated thread performs "
                + "no blocking operations, DEBUG info: "
                + str(type(self.__generator__)))
    def run(self):
        '''
        This run() method runs the thread of the active thread object.
        CSC343Compile.py generates this method from a custom state machine.
        '''
        __lastMissedEvent__ = None
        globals = {
            'math'      :   math,                   # module
            'functools' :   functools,              # module
            'operator'  :   operator,               # module
            'fork'      :   self.fork,              # method
            'spawn'     :   self.spawn,             # method
            'retire'    :   self.retire,            # method
            'cpu'       :   self.cpu,               # method
            'io'        :   self.io,                # method
            'sleep'     :   self.sleep,             # method
            'yieldcpu'  :   self.yieldcpu,          # method
            'trigger'   :   self.trigger,           # method
            'sample'    :   self.sample,            # method
            'time'      :   self.time,              # method
            'getid'     :   self.getid,             # method
            'waitForEvent' : self.waitForEvent,     # method
            'wait'      :   self.wait,              # method
            'exit'      :   self.exit,              # method
            'kill'      :   self.kill,              # method
            'join'      :   self.join,              # method
            'signalEvent' : __scheduledObject__.signalEvent,       # method
            'assign'    :   self.assign,            # method
            'noop'      : __scheduledObject__.noop,       # method
            'msg'       :   self.msg,               # method
            "pcb"       :   self.pcb,               # field
            'processor' :   self.processor,         # field
            'thread'    :   self,                   # this object
            'Queue'     :   Queue,                  # class
            'self'      :   self                    # this object
        }
        self.globals = globals
        locals = {
            'hoursInDay' : 24,
            'daysInYear' : 365,
            'hoursToSleep' : 0,
            'hoursInYear' : 0,
            'yearsToSleep' : 10,
        }
        self.__eventSet__ = set(['init', 'sleep'])
        self.locals = locals
        try:
            try:
                self.state = 'init'
                self.waitingon = 'init'
                self.logger.log(self, tag="APPROACH")
                self.logger.log(self, tag="ARRIVE")
                stime = None        # simulation time
                event = None        # event is the event that got us here
                args = None         # args are the args passed from event
                while not self.__isdead__:
                    # Run until state machine sets __isdead__ or return.
                    self.exclusiveWait = False
                    if self.__sleepResult__:
                        stime, event, args = self.__sleepResult__
                        # DEPRECATED self.logger.log(self)
                    else:
                        stime = self.scheduler.time
                        event = None
                        args = None
                    # CSC343Compile.py generates custom run() code here.
                    if self.state == 'teen':
                        if event == 'sleep':
                            if eval('(time() / hoursInYear) < 20',globals,locals):
                                self.logger.log(self, tag="REPEAT")
                                exec('msg("teen years " + str(time() / hoursInYear) + ", sleep some more.")',globals,locals)
                                exec('sleep(hoursToSleep)',globals,locals)
                                yield None
                                __lastMissedEvent__ = None
                                continue
                        if event == 'sleep':
                            if eval('(time() / hoursInYear) >= 20',globals,locals):
                                self.logger.log(self, tag="DEPART")
                                self.state = 'youngAdult'
                                self.logger.log(self, tag="APPROACH")
                                exec('msg("teen->youngAdult years " + str(time() / hoursInYear) + ", growing up.")',globals,locals)
                                exec('sleep(0)',globals,locals)
                                self.logger.log(self, tag="ARRIVE")
                                yield None
                                __lastMissedEvent__ = None
                                continue
                        if event != __lastMissedEvent__ and self.logger.getLevel() >= (__DEBUGLEVEL__-1):
                            self.msg("INFO: Missed event: " + event + " From state: " + self.state)
                            __lastMissedEvent__ = event
                    elif self.state == 'infant':
                        if event == 'sleep':
                            if eval('(time() / hoursInYear) < 13',globals,locals):
                                self.logger.log(self, tag="REPEAT")
                                exec('msg("infant years " + str(time() / hoursInYear) + ", sleep some more.")',globals,locals)
                                exec('sleep(hoursToSleep)',globals,locals)
                                yield None
                                __lastMissedEvent__ = None
                                continue
                        if event == 'sleep':
                            if eval('(time() / hoursInYear) >= 13',globals,locals):
                                self.logger.log(self, tag="DEPART")
                                self.state = 'teen'
                                self.logger.log(self, tag="APPROACH")
                                exec('msg("infant years " + str(time() / hoursInYear) + ", growing up.")',globals,locals)
                                exec('sleep(0)',globals,locals)
                                self.logger.log(self, tag="ARRIVE")
                                yield None
                                __lastMissedEvent__ = None
                                continue
                        if event != __lastMissedEvent__ and self.logger.getLevel() >= (__DEBUGLEVEL__-1):
                            self.msg("INFO: Missed event: " + event + " From state: " + self.state)
                            __lastMissedEvent__ = event
                    elif self.state == 'midLife':
                        if event == 'sleep':
                            if eval('(time() / hoursInYear) < 50',globals,locals):
                                self.logger.log(self, tag="REPEAT")
                                exec('msg("midLife years " + str(time() / hoursInYear)             + ", sleep some more.")',globals,locals)
                                exec('sleep(hoursToSleep)',globals,locals)
                                yield None
                                __lastMissedEvent__ = None
                                continue
                        if event == 'sleep':
                            if eval('(time() / hoursInYear) >= 50',globals,locals):
                                self.logger.log(self, tag="DEPART")
                                self.state = 'gettingOld'
                                self.logger.log(self, tag="APPROACH")
                                exec('msg("midLife years " + str(time() / hoursInYear) + ", growing up.")',globals,locals)
                                exec('sleep(0)',globals,locals)
                                self.logger.log(self, tag="ARRIVE")
                                yield None
                                __lastMissedEvent__ = None
                                continue
                        if event != __lastMissedEvent__ and self.logger.getLevel() >= (__DEBUGLEVEL__-1):
                            self.msg("INFO: Missed event: " + event + " From state: " + self.state)
                            __lastMissedEvent__ = event
                    elif self.state == 'gettingOld':
                        if event == 'sleep':
                            if eval('(time() / hoursInYear) < 90',globals,locals):
                                self.logger.log(self, tag="REPEAT")
                                exec('msg("gettingOld years " + str(time() / hoursInYear)             + ", sleep some more.")',globals,locals)
                                exec('sleep(hoursToSleep)',globals,locals)
                                yield None
                                __lastMissedEvent__ = None
                                continue
                        if event == 'sleep':
                            if eval('(time() / hoursInYear) >= 90',globals,locals):
                                self.logger.log(self, tag="DEPART")
                                self.state = 'deadInTheWater'
                                self.logger.log(self, tag="APPROACH")
                                exec('msg("gettingOld years " + str(time() / hoursInYear) + ", done.")',globals,locals)
                                self.logger.log(self, tag="ARRIVE")
                                __lastMissedEvent__ = None
                                continue
                        if event != __lastMissedEvent__ and self.logger.getLevel() >= (__DEBUGLEVEL__-1):
                            self.msg("INFO: Missed event: " + event + " From state: " + self.state)
                            __lastMissedEvent__ = event
                    elif self.state == 'youngAdult':
                        if event == 'sleep':
                            if eval('(time() / hoursInYear) < 35',globals,locals):
                                self.logger.log(self, tag="REPEAT")
                                exec('msg("youngAdult years " + str(time() / hoursInYear)             + ", sleep some more.")',globals,locals)
                                exec('sleep(hoursToSleep)',globals,locals)
                                yield None
                                __lastMissedEvent__ = None
                                continue
                        if event == 'sleep':
                            if eval('(time() / hoursInYear) >= 35',globals,locals):
                                self.logger.log(self, tag="DEPART")
                                self.state = 'midLife'
                                self.logger.log(self, tag="APPROACH")
                                exec('msg("youngAdult years " + str(time() / hoursInYear)             + ", growing up.")',globals,locals)
                                exec('sleep(0)',globals,locals)
                                self.logger.log(self, tag="ARRIVE")
                                yield None
                                __lastMissedEvent__ = None
                                continue
                        if event != __lastMissedEvent__ and self.logger.getLevel() >= (__DEBUGLEVEL__-1):
                            self.msg("INFO: Missed event: " + event + " From state: " + self.state)
                            __lastMissedEvent__ = event
                    elif self.state == 'init':
                        if event == 'init':
                            self.logger.log(self, tag="DEPART")
                            self.state = 'infant'
                            self.logger.log(self, tag="APPROACH")
                            exec('hoursInYear = hoursInDay * daysInYear',globals,locals)
                            exec('hoursToSleep = hoursInYear * yearsToSleep',globals,locals)
                            exec('sleep(hoursInYear * 3)',globals,locals)
                            self.logger.log(self, tag="ARRIVE")
                            yield None
                            __lastMissedEvent__ = None
                            continue
                        if event != __lastMissedEvent__ and self.logger.getLevel() >= (__DEBUGLEVEL__-1):
                            self.msg("INFO: Missed event: " + event + " From state: " + self.state)
                            __lastMissedEvent__ = event
                    elif self.state == 'deadInTheWater':
                        self.logger.log(self, tag="DEPART")
                        return
            except __ThreadRetireException__, ignoreme:
                pass
            except Exception, xxx:
                if self.logger.isOpen():
                    self.logger.log(self)
                    self.state = '<defunct on Exception ' + str(xxx) + '>'
                    self.logger.log(self)
                    traceback.print_exc(file=self.logger.getFile())
                    self.logger.flush()
                    raise
        finally:
            if self.logger.isOpen() and not self.state.startswith('<defunct'):
                # DEPRECATED self.logger.log(self)
                self.state = '<defunct>'
                self.waitingon = None
                self.logger.log(self)
                self.logger.flush()
            try:
                self.retire()       # make sure any join()ers are released.
            except __ThreadRetireException__, IdontCare:
                pass
            # DEPRECATED self.scheduler.notifyOfTerminatingSimThread()
            # Unblock sched for another Python Thread.

class iounit(_IOunit_):
    '''
    Class iounit simply uses base class _IOunit_ as is to provide
    iounit behavior. Later versions of this class will extend iounit
    to run according to custom state machine specifications.
    '''
    def __init__(self, scheduler, logger, factory, processor, isfast,       \
            seed=None):
        '''
        Invoke the base class _IOunit_ constructor without extension.
        See constructor _IOunit_.__init__ for parameter documentation.
        '''
        _IOunit_.__init__(self, scheduler, logger, factory, processor,      \
            isfast, seed=seed)
        self.__generator__ = self.run()     # Added August 2015
        if type(self.__generator__) != types.GeneratorType:
            raise AttributeError, ("ERROR, generated iounit performs "
                + "no blocking operations, DEBUG info: "
                + str(type(self.__generator__)))

def __processorFactory__(scheduler, logger, factory, contextLength,         \
        seed=None):
    ''' See processor and _Processor_. '''
    return processor(scheduler, logger, factory, contextLength,             \
        seed=seed)

def __threadFactory__(scheduler, logger, factory, processor, pcb,           \
        processNumber, threadNumber, terminal, seed=None):
    ''' See thread and _Thread_. '''
    return thread(scheduler, logger, factory, processor,                    \
        pcb, processNumber, threadNumber, terminal,                         \
            seed=(seed if seed is None else (seed ^ processNumber ^ (threadNumber < 1) ^ 1)))

def __iounitFactory__(scheduler, logger, factory, processor, isfast,        \
        seed=None):
    ''' See iounit and _IOunit_. '''
    return iounit(scheduler, logger, factory, processor, isfast, seed=seed)

usage = 'USAGE: python THISFILE.py NUMCONTEXTS NUMFASTIO SIMTIME SEED|None LOGLEVEL'
#<<<<<USAGE>>>>>

def main():
    if len(sys.argv) != 6 or len(sys.argv[0]) < 4                           \
            or not sys.argv[0].endswith('.py'):
        sys.stderr.write(usage + '\n')
        sys.exit(1)
    else:
        sys.stderr.write('MSG cmd line: ' + str(sys.argv) + ", usage " + usage + '\n')
    numcontexts = None
    try:
        numcontexts = int(sys.argv[1])
        if numcontexts < 1:
            raise ValueError, ("ERROR, invalid number of contexts: "        \
                + str(numcontexts))
    except Exception, xxx:
        sys.stderr.write('ERROR: ' + str(xxx) + '\n')
        sys.stderr.write(usage + '\n')
        sys.exit(2)
    numfastio = None
    try:
        numfastio = int(sys.argv[2])
        if numfastio < 1:
            raise ValueError, ("ERROR, invalid number of fast IO units: "   \
                + str(numfastio))
    except Exception, xxx:
        sys.stderr.write('ERROR: ' + str(xxx) + '\n')
        sys.stderr.write(usage + '\n')
        sys.exit(3)
    simtime = None
    try:
        simtime = int(sys.argv[3])
        if simtime < 1:
            raise ValueError, ("ERROR, invalid simulation time limit: "     \
                + str(simtime))
    except Exception, xxx:
        sys.stderr.write('ERROR: ' + str(xxx) + '\n')
        sys.stderr.write(usage + '\n')
        sys.exit(4)
    loglevel = None
    try:
        loglevel = int(sys.argv[5])
        if loglevel < 0:    # Currently everything > 3 treated as 3
            raise ValueError, ("ERROR, invalid simulation logging level: "  \
                + str(loglevel))
    except Exception, xxx:
        sys.stderr.write('ERROR: ' + str(xxx) + '\n')
        sys.stderr.write(usage + '\n')
        sys.exit(6)
    seed = None
    if sys.argv[4] != 'None':
        try:
            seed = int(sys.argv[4])
        except Exception, xxx:
            sys.stderr.write('ERROR: ' + str(xxx) + '\n')
            sys.stderr.write(usage + '\n')
            sys.exit(5)
    basename = sys.argv[0][:-2]
    logfilename = basename + 'log'
    if os.environ.has_key('STMLOGDIR'):
        logdir = os.environ['STMLOGDIR'] + '/'
    else:
        logdir = './'
    logfiletmp = logdir + os.environ['USER'] + '_STM_' + logfilename
    try:
        os.system('rm -f ' + logfilename + ' ; ln -s ' + logfiletmp
            + ' ' + logfilename)
    except Exception, estr:
        sys.stderr.write('WARNING(ignored) on ln -s ' + logfiletmp
            + ' ' + logfilename + '\n')
    # logger = __simulationLogger__(logfilename, loglevel)
    logger = __simulationLogger__(logfiletmp, loglevel)
    scheduler = __simulationScheduler__(logger, simtime)
    logger.setScheduler(scheduler)
    factory = {"processor" : __processorFactory__,
        "thread" : __threadFactory__, "io" : __iounitFactory__}
    p = __processorFactory__(scheduler, logger, factory, numcontexts,
        seed=seed-1)
    # Do not use identical seed. That makes all IOunits have the same numbers!
    io = [__iounitFactory__(scheduler, logger, factory, p, True, seed=seed+i)
        for i in range (0, numfastio)]
    p.setIOunits(io)
    # DEPRECATED for eieio in io:
        # DEPRECATED eieio.start()
    # DEPRECATED p.start()
    scheduler.sleep(0, p, 'init', None)
    scheduler.__run__()
    sys.exit(0)
if __name__ == "__main__":
    main()
