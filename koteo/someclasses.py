#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Koldo Oteo Orellana (koldo.oteo@gmail.com)
import os, time, glob, re
import psutil
from .somefunctions import bytes_to
from .somefunctions import get_cpus

class SomePerf(object):

    proc_d = "/proc"

    def __init__(self):
        pass

    # Find process in 'D' State
    # Processes that are waiting for I/O are commonly in an "uninterruptible sleep" state or "D"
    def d_state_proc(self):
        try:
            for i in range(1, 9):
                self.stat_f = glob.glob('/proc/[0-9]*/status')
                for stat in self.stat_f:
                    with open(stat) as f:
                        if 'disk sleep' in f.read():
                            find_p = re.search(r'\d+', stat)
                            print ("The process with pid: {} in 'D' State. Try using iotop!".format(find_p.group(0)))
                            print ("Trace the process, and see if it could be, a disk problem, cpu or network (nfs??)")
                time.sleep(2)
        except FileNotFoundError as e:
            print ('{} ERROR!!!'.format(e))
            pass

    # How many open files you have in the system
    # lsof -X -a  -d ^mem -d ^cwd -d ^rtd -d ^txt -d ^DEL |wc -l
    # for p in /proc/[0-9]* ; do echo $(ls $p/fd | wc -l) $(cat $p/cmdline) ; done | sort -n  |awk '{ SUM += $1} END { print SUM }'
    def files_open(self):
        with open('/proc/sys/fs/file-max', 'r') as f:
            self.fmax = f.read().strip()
        self.files_lst = []
        try:
            for proc in psutil.process_iter():
                self.files_lst.append(proc.num_fds())
            print ("You have {} files open".format(sum(self.files_lst)))
            if sum(self.files_lst) >= int(self.fmax):
                print ("Take a look of your user's limit with ulimit -a, or maybe you need to increase your system "
                       "limits(max open files). sysctl -w fs.file-max=NEW_VALUE")
        except psutil.AccessDenied:
            print ("Login as root, or use sudo, to execute this Script!!!")

    # Print LOAD AVERAGE information
    def load_avg(self):
        self.cpus_num = get_cpus()
        self.load_av = os.getloadavg()[0]
        print ("Last minute Load Average: {}".format(self.load_av))
        if (self.load_av / self.cpus_num) <= 1:
            print ("Your system Load Avg seams to be good, but try to check it in different periods of time (sar/top).")
        else:
            print ("Check the cpu usage and iowait, maybe you have a problem")

# Class to use in Resources menu
class Resources(object):
    def __init__(self):
        pass

    # Print swap usage information
    def prt_swp(self):
        self.swp = psutil.swap_memory()
        self.tot_swp = bytes_to(self.swp.total)
        self.us_swp = bytes_to(self.swp.used)

        print ("Total SWAP: {} - Used SWAP: {}".format(self.tot_swp, self.us_swp))

    # Print memory usage information
    def prt_mem(self):
        self.memo = psutil.virtual_memory()
        self.tot_mem = bytes_to(self.memo.total)
        self.us_mem = bytes_to(self.memo.used)
        self.cach_mem = bytes_to(self.memo.cached)

        print ("Total Memory: {} || Used Memory: {}".format(self.tot_mem, self.us_mem))
        print ("Cached Memory: {}".format(self.cach_mem))

    # Print CPU usage information
    def cpu_use(self):
        self.use_cpu = psutil.cpu_percent(interval=1, percpu=True)
        self.len_use_cpu = len(self.use_cpu)
        self.avg_use_cpu = (sum(i for i in self.use_cpu) / self.len_use_cpu)

        print ("The CPU Average is: {} %".format(self.avg_use_cpu))
