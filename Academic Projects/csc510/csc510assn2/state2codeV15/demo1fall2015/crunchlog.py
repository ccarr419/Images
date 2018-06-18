# crunchlog.py, D. Parson, fall 2013, 2015
# Collect and reduce data in a log file from a csc 343 STM simulation run.

import copy
import math
import sys
from diffset import DIFFSET, DIFF_TOLERANCE

def mode(valueList):
    '''
    Return the mode of valueList, where mode is the most frequently
    appearing value. If valueList is multimodal, this function returns
    a list of all equally-most-frequent values; otherwise, it returns
    the scalar mode.
    '''
    histogram = {}
    results = []
    for v in valueList:
        if v in histogram:
            histogram[v] = histogram[v] + 1
        else:
            histogram[v] = 1
    counts = list(histogram.values())
    counts.sort(reverse=True)
    highcount = counts[0]
    for k in histogram.keys():
        if histogram[k] == highcount:
            results.append(k)
    if len(results) == 1:
        return results[0]
    return results

def median(valueList):
    '''
    Return the median of valueList, where median is the center value
    after sorting a copy of valueList. If there are an even number of elements,
    median returns the mean of the two central elements. Otherwise, any
    element type amenable to a sort may be in the valueList.
    '''
    vl = copy.copy(valueList)
    vl.sort()
    if ((len(vl) & 1) == 1):        # odd number of elements
        return vl[int(len(vl) / 2)]
    upper = int(len(vl) / 2)
    if vl[upper-1] == vl[upper]:
        return vl[upper]
    sum = vl[upper-1] + vl[upper]
    untyper = sum / 2
    floater = sum / 2.0
    if floater == untyper:
        return untyper
    else:
        return floater

def mean(valueList):
    '''
    Return the mean of valueList.
    '''
    sum = 0
    for v in valueList:
        sum = sum + v
    divisor = len(valueList) if len(valueList) else 1
    untyper = sum / divisor
    floater = sum / float(divisor)
    if floater == untyper:
        return untyper
    else:
        return floater

def stddev(valueList, average=None):
    '''
    Return the population standard deviation of valueList.
    If the caller supplies the average parameter, stddev uses that as the
    mean in computing the standard deviation. Otherwise, stddev invokes
    mean() to compute the mean, but returns only the standard devaition.
    '''
    if average == None:
        avg = mean(valueList)
    else:
        avg = average
    variance = 0.0
    for v in valueList:
        diff = v - avg
        variance = variance + (diff * diff)
    divisor = len(valueList) if len(valueList) else 1
    result = math.sqrt(variance / float(divisor))
    return result

def minmax(valueList):
    '''
    Return the ordered pair (minimum, maximum) of valueList as an ordered pair.
    '''
    min = valueList[0]
    max = valueList[0]
    for v in valueList[1:]:
        if v < min:
            min = v
        if v > max:
            max = v
    return((min, max))

usage = "python crunchlog.py LOGFILE.log" 
if __name__ == '__main__':
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".log"):
        sys.stderr.write(usage + '\n')
        sys.exit(1)
    crunchfilename = sys.argv[1][:-3] + 'crunch'
    reffilename = crunchfilename + '.ref'
    flog = open(sys.argv[1], 'rU')
    fcrunch = open(crunchfilename, 'w')
    threaddata = {} # map thread to a map of the lists of its various states' times
    threadcurrent = {} # map thread to [state, starttime]
    threadlife = {} # map thread to [inittime, endtime] for turnaround time
    line = flog.readline()
    lineno = 1
    while line:
        fields = line.strip().split(',')
        if len(fields) < 5 or fields[1] != 'LOG'        \
                or not fields[2].strip().startswith('thread'):
            line = flog.readline()
            lineno += 1
            continue
        simtime = int(fields[0].strip())
        pidtid = fields[2].strip()
        state = fields[3].strip()
        action = fields[4].strip()
        if not pidtid in threadlife.keys():
            threadlife[pidtid] = [simtime, simtime]
        else:
            threadlife[pidtid][1] = simtime
        if action == 'APPROACH':
            threadcurrent[pidtid] = [state, simtime]
        elif action == 'DEPART':
            if state != threadcurrent[pidtid][0]:
                raise ValueError("Departing state " + state
                    + " does not match arriving state "
                    + threadcurrent[pidtid][0] + ' at line '
                    + str(lineno) + ' in file ' + sys.argv[1])
            interval = simtime - threadcurrent[pidtid][1]
            if pidtid not in threaddata.keys():
                threaddata[pidtid] = {}
            if state not in threaddata[pidtid].keys():
                threaddata[pidtid][state] = []
            threaddata[pidtid][state].append(interval)
            threadcurrent[pidtid] = None
        line = flog.readline()
        lineno += 1
    flog.close()
    for tid in threadlife.keys():
        threadlife[tid] = threadlife[tid][1] - threadlife[tid][0]
    sumthreads = {'TURNAROUNDTIME' : 0}
    listthreads = {'TURNAROUNDTIME' : []}
    for tid in threaddata.keys():
        sumthreads['TURNAROUNDTIME'] += threadlife[tid]
        listthreads['TURNAROUNDTIME'].append(threadlife[tid])
        for state in threaddata[tid].keys():
            if state not in sumthreads.keys():
                sumthreads[state] = 0
                listthreads[state] = []
            sumthreads[state] += reduce(lambda a, b : a+b, threaddata[tid][state])
            listthreads[state].extend(threaddata[tid][state])
    reportkeys = list(sumthreads.keys())
    reportkeys.sort()
    for state in reportkeys:
        fcrunch.write('SUM_' + state + '=' + str(sumthreads[state]) + '\n')
        fcrunch.write('MEAN_' + state + '=' + str(mean(listthreads[state])) + '\n')
        fcrunch.write('STDDEV_' + state + '=' + str(stddev(listthreads[state])) + '\n')
        fcrunch.write('MEDIAN_' + state + '=' + str(median(listthreads[state])) + '\n')
        min, max = minmax(listthreads[state])
        fcrunch.write('MIN_' + state + '=' + str(min) + '\n')
        fcrunch.write('MAX_' + state + '=' + str(max) + '\n')
    def despace(string):
        spaceloc = string.find(' ')
        while spaceloc > -1:
            string = string[:spaceloc] + '_' + string[spaceloc+1:]
            spaceloc = string.find(' ')
        return string
    reportkeys = list(threaddata.keys())
    reportkeys.sort()
    for tid in reportkeys:
        tidns = despace(tid)
        fcrunch.write('SUM_TURNAROUNDTIME' + '_' + tidns + '='
            + str(threadlife[tid]) + '\n')
        statekeys = list(threaddata[tid].keys())
        statekeys.sort()
        for state in statekeys:
            fcrunch.write('SUM_' + state + '_' + tidns + '='
                + str(reduce(lambda a,b : a+b, threaddata[tid][state])) + '\n')
            fcrunch.write('MEAN_' + state + '_' + tidns + '='
                + str(mean(threaddata[tid][state])) + '\n')
            fcrunch.write('STDDEV_' + state + '_' + tidns + '='
                + str(stddev(threaddata[tid][state])) + '\n')
            fcrunch.write('MEDIAN_' + state + '_' + tidns + '='
                + str(median(threaddata[tid][state])) + '\n')
            min, max = minmax(threaddata[tid][state])
            fcrunch.write('MIN_' + state + '_' + tidns + '='
                + str(min) + '\n')
            fcrunch.write('MAX_' + state + '_' + tidns + '='
                + str(max) + '\n')
    fcrunch.close()
    # Read back in and compare to ref file
    fcrunch = open(crunchfilename, 'rU')
    newstats = {}
    line = fcrunch.readline()
    while line:
        line = line.strip()
        if line:
            exec(line, newstats, newstats)
        line = fcrunch.readline()
    fcrunch.close()
    fcrunch = open(reffilename, 'rU')
    oldstats = {}
    line = fcrunch.readline()
    while line:
        line = line.strip()
        if line:
            exec(line, oldstats, oldstats)
        line = fcrunch.readline()
    fcrunch.close()
    sys.stderr.write('\nDIFFing ' + crunchfilename + ' ' + reffilename + '\n')
    iswarn = False
    for prop in DIFFSET:
        old = None
        new = None
        try:
            old = oldstats[prop]
        except KeyError, kstr:
            sys.stderr.write('ERROR, no value for ' + prop      \
                + ' in old data set.\n')
            iswarn = True
            sys.exit(1)
        try:
            new = newstats[prop]
        except KeyError, kstr:
            sys.stderr.write('ERROR, no value for ' + prop      \
                + ' in new data set.\n')
            iswarn = True
            sys.exit(1)
        diff = (old-new) if (old >= new) else (new-old)
        # Watch out for divide by 0 on old!
        if old == 0:
            old = 1
        if (float(diff) / float(old)) > DIFF_TOLERANCE and diff >= 10:
            sys.stderr.write('WARNING, ' + prop + ' = ' + str(new)      \
                + ' in ' + crunchfilename + ', = ' + str(old) + ' in '     \
                + reffilename + '.\n')
            iswarn = True
        else:
            sys.stderr.write('OK: ' + prop + '\n')
    sys.stderr.write('\n')
    if iswarn:
        sys.exit(1)
    sys.exit(0)
