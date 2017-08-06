#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Koldo Oteo Orellana (koldo.oteo@gmail.com)
import os, time, glob, re
import psutil

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
