#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Koldo Oteo Orellana (koldo.oteo@gmail.com)
###
import psutil
import os
import time
###

### Vars
num_cpu = psutil.cpu_count(logical=True)
#
onemb = 1048576
tenmb = 10485760
hmb = 104857600
onegb = 1073741824
tengb = 10737418240
hgb = 107374182400
###

# Convert bytes to human readable
def bytes_mb(bytes):
    if bytes < onemb:
        return ("{:.1f} Bytes".format(bytes))
    elif bytes < onegb:
        return ("{:.1f} Mb".format(bytes / 1024 / 1024, '.2f'))
    elif bytes >= onegb:
        return ("{:.1f} Gb".format(bytes / 1024 / 1024 / 1024, '.2f'))


# Print swap usage information
def prt_swp():
    swp = psutil.swap_memory()
    tot_swp = bytes_mb(swp.total)
    us_swp = bytes_mb(swp.used)

    print ("Total SWAP: {} - Used SWAP: {}".format(tot_swp, us_swp))


# Print memory usage information
def prt_mem():
    memo = psutil.virtual_memory()
    tot_mem = bytes_mb(memo.total)
    us_mem = bytes_mb(memo.used)
    cach_mem = bytes_mb(memo.cached)

    print ("Total Memory: {} - Used Memory: {}".format(tot_mem, us_mem))
    print ("Cached Memory: {}".format(cach_mem))


# Print CPU usage information
def cpu_use():
    use_cpu = psutil.cpu_percent(interval=1, percpu=True)
    len_use_cpu = len(use_cpu)
    avg_use_cpu = (sum(i for i in use_cpu) / len_use_cpu)

    print ("The CPU Average is: {} %".format(avg_use_cpu))


# Print LOAD AVERAGE information
def load_avg():
    load_av = os.getloadavg()[0]
    print ("Last minute Load Average: {}".format(load_av))
    if (load_av / num_cpu) <= 1:
        print ("Your system Load Avg seams to be good, but try to check it in different periods of time (sar/top).")
    else:
        print ("Check the cpu usage and iowait, maybe you have a problem")


# Print Disk's load information
def disk_use():
    s = subprocess.Popen(["iostat -dx -y 1 4"], shell=True, stdout=subprocess.PIPE).stdout
    iostat_lst = [[elem.split()] for elem in s.read().splitlines() if (not elem.startswith(b'Linux')) if
                  (not elem.startswith(b'Device:'))]

    for line in iostat_lst:
        if len(line[0]) == 14 and float(line[0][13]) > 40:
            print ("Take a look at Disk: {}. Device %util is {}% and maybe you have a problem".format(
                line[0][0].decode("utf-8"), float(line[0][13])))
            print ("You have {} read requests per second (r/s)".format(float(line[0][3])))
            print ("You have {} writes requests per second (w/s)".format(float(line[0][4])))
            print ('\n')


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
