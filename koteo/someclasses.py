#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Koldo Oteo Orellana (koldo.oteo@gmail.com)
import os, time, glob

class SomePerf(object):
    proc_d = "/proc"
    def d_state_proc(self):
        try:
            for i in range(1, 9):
                self.stat_f = glob.glob('/proc/[0-9]*/status')
                for stat in self.stat_f:
                    with open(stat) as f:
                        if 'disk sleep' in f.read():
                            print ("pid: {} in D state".format(stat))
                time.sleep(2)
        except FileNotFoundError as e:
            print ('{} ERROR!!!'.format(e))
            pass




# Find process in 'D' State
# Processes that are waiting for I/O are commonly in an "uninterruptible sleep" state or "D"
def find_io():
    loop_times = 1
    try:
        for i in range(1,6):
            for proc in psutil.process_iter():
                pinfo = proc.as_dict(attrs=['pid', 'name', 'status'])
                if pinfo['status'] == 'disk-sleep':
                    print ("The process: {}, with PID: {} is in 'D' State. Try using iotop!".format(pinfo['name'],
                                                                                                    pinfo['pid']))
                    print ("Look the process and see if it could be a disk problem, cpu or network (nfs??)")
            time.sleep(2)
    except psutil.NoSuchProcess:
        pass

# How many open files you have in the system
# lsof -X -a  -d ^mem -d ^cwd -d ^rtd -d ^txt -d ^DEL |wc -l
# for p in /proc/[0-9]* ; do echo $(ls $p/fd | wc -l) $(cat $p/cmdline) ; done | sort -n  |awk '{ SUM += $1} END { print SUM }'
def files_open():
    with open('/proc/sys/fs/file-max', 'r') as f:
        fmax = f.read().strip()
    files_lst = []
    try:
        for proc in psutil.process_iter():
            files_lst.append(proc.num_fds())
        print ("You have {} files open".format(sum(files_lst)))
        if sum(files_lst) >= int(fmax):
            print ("Take a look of your user's limit with ulimit -a, or maybe you need to increase your system "
                   "limits(max open files). sysctl -w fs.file-max=NEW_VALUE")
    except psutil.AccessDenied:
print ("Login as root, or use sudo, to execute this Script!!!")