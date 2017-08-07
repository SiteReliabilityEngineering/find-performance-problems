#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Koldo Oteo Orellana (koldo.oteo@gmail.com)
###
import time
import os, sys
import psutil
import subprocess
from collections import namedtuple

# Get number of CPUS
def g_cpu():
    cpusn = os.sysconf("SC_NPROCESSORS_ONLN")
    if cpusn > 0:
        return cpusn

# With this class we are going to create some methods, that query,
# the vmstat system command. We will query cpu, memory and swap,
# performance data
class Vmstat(object):
    
    def __init__(self):
        ''' We create a list into a dict with the next data:
        r_col: 'r' column with number of processes waiting for run time
        si/so_col: swapped in/out, us_col: user cpu time
        sy_col: kernel cpu time ; st_col: Time stolen from a vmachine'''
        self.real_data = {'r_col': [], 'b_col': [], 'si_col': [], 'so_col': [], 'us_col': [], 'sy_col': [], 'st_col': []}
        self.cpusn = g_cpu()

# Execute vmstat and save the data into a list inside a dictionary
    def exec_vmstat(self):
        self.vm = subprocess.Popen(['vmstat', '-n', '2', '9'], shell=False, stdout=subprocess.PIPE).stdout
        try:
            self.vmstat_lst = [[elem.split()] for elem in self.vm.read().splitlines() if (not elem.startswith(b'procs'))
                               if (not elem.startswith(b' r'))]
            self.lst_len = len(self.vmstat_lst)
            for elem in self.vmstat_lst[1:self.lst_len + 1]:
                self.real_data['r_col'].append(int(elem[0][0])) # r_col
                self.real_data['b_col'].append(int(elem[0][1])) # b_col
                self.real_data['si_col'].append(int(elem[0][6])) # si_col
                self.real_data['so_col'].append(int(elem[0][7])) # so_col
                self.real_data['us_col'].append(int(elem[0][12])) # us_col
                self.real_data['sy_col'].append(int(elem[0][13])) # sy_col
                self.real_data['st_col'].append(int(elem[0][16])) # st_col
        except Exception as e:
            print ('{} ERROR!!!'.format(e))

# Check if you have processes waiting. (CPU Bottleneck)  
    def chk_procs_waiting(self):
        self.count_r = 0
        self.count_b = 0
        for r, b in zip(self.real_data['r_col'], self.real_data['b_col']):
            if (r / self.cpusn) > 1:
                self.count_r +=1
                if self.count_r >=2:
                    return '''r column is high, maybe you have a cpu 
                              bottleneck. Maybe you need more CPUS'''
            elif (b > r):
                self.count_b +=1
                if self.count_b >=2:
                    return '''b column is higher than r, maybe you 
                              have a cpu bottleneck or slow disks'''
            else:
                return 'No processes waiting at this moment'
            
# Check if CPU usage is high.
    def chk_cpu_use(self):
        self.calc_cpuavg = sum(self.real_data['us_col'] + self.real_data['sy_col'] + self.real_data['st_col']) \
                           / (self.lst_len - 1)
        if self.calc_cpuavg >= 80 and self.calc_cpuavg < 90:
            return "Look your CPU usage, it's high. CPU usage: %.2f%%" % (self.calc_cpuavg)
        elif self.calc_cpuavg > 90:
            return "Look your CPU usage, it's VERY high. CPU usage: %.2f%%" % (self.calc_cpuavg)
        else:
            return "The CPU usage is below 80%%. CPU usage: %.2f%%" % (self.calc_cpuavg)
        
# Check if there's swapping in/out activity        
    def chk_swapping(self):
        self.count_si = 0
        self.count_so = 0
        for so, si in zip(self.real_data['so_col'], self.real_data['si_col']):
            if so > 0:
                self.count_so +=1
                if self.count_so >=2:
                    return 'Check the swap, the server is swapping out'
            elif si > 0:
                self.count_si +=1
                if self.count_si >=2:
                    return 'Check the swap, the server is swapping in'
            else:
                return 'At this moment the server is not swapping in/out'
            
# Print Message when you delete the Instance with del (instanceName)            
        def __del__(self):
            print ("Instance of Class Vmstat,  Removed")

########################################################################################################################
# With this class we are going to create some methods, that query,
# the vmstat system command. We will query cpu, memory and swap,
# performance data
class Iostat(object):
    rpm72k = '75, 100' # max iops for a 7200 rpm disk
    rpm10k = '125, 150' # max iops for 10k rpm disk
    rpm15k = '175, 200' # max iops for 15k rpm disk
    ssd = 1000 # max 1000's iops for SSD

    def __init__(self):
        self.cpusn = g_cpu()
        self.IostatSchema = namedtuple('IostatSchema', 'Device rrqm wrqm r w rMB wMB avgrqsz avgqusz await r_await w_await svctm util')
        self.TpsSchema = namedtuple('TpsSchema', 'Device tps avgqusz util')

# Execute iostat and save the data into a list inside a dictionary
    def exec_iostat(self):

        self.iost = subprocess.Popen(['iostat', '-ydxmN', '2', '8'], shell=False, stdout=subprocess.PIPE).stdout
        try:
            self.iostat_lst = [dat.split() for dat in self.iost.read().splitlines() if (not dat.startswith(b'Linux')) if (not dat.startswith(b' r')) if
                               (not dat.startswith(b'Device:')) if (dat != b'') if (not dat.startswith(b'fd0'))]
            self.lst_len = len(self.iostat_lst)
            self.iost_tup = tuple(self.IostatSchema(*line) for line in self.iostat_lst[0:self.lst_len] )
        except Exception as e:
            print ('{} ERROR!!!'.format(e))

    def format_iostat(self):
        self.disk_tps_util = []

        # We save device, tps/iops, avgqusz, util into a list
        for line in self.iost_tup:
            self.disk_tps_util.append([line.Device.decode("utf-8"), (float(line.r) + float(line.w)), float(line.avgqusz), float(line.util)])
        # I create a namedtuple with self.disk_tps list
        self.tps_util_tup = tuple( self.TpsSchema(*line) for line in self.disk_tps_util )

    def chk_tps(self):
        self.tps_count = 0 # we count the times that tps are higher than 75

        # It's difficult to know the disk rpms in a virtual machine, that's why I won't check it
        for line in self.tps_util_tup:
            if line.tps > 75:
                self.tps_count +=1
                if self.tps_count >= 3:
                    print ("Check your TPS/IOPS of your disk with iostat! Your tps are higher than 75!!!\n")
                    print ("----- TPS references, depending of disk type -----")
                    print ("Max TPS for a 7.2k rpm disk is: {}".format(Iostat.rpm72k))
                    print ("Max TPS for a 10k rpm disk is: {}".format(Iostat.rpm10k))
                    print ("Max TPS for a 15k rpm disk is: {}".format(Iostat.rpm15k))
                    print ("Max TPS for a SSD disk is: {}".format(Iostat.ssd))
                    break
        if self.tps_count < 3:
            print ("I don't see too much TPS in your disk's, I think they are working well")


    def chk_util(self):
        self.util_count = 0 # we count the times that util is higher than 91

        for line in self.tps_util_tup:
            if line.util > 91:
                self.util_count +=1
                if self.util_count >= 3:
                    print ("Check your %util of your disk with iostat! Your %util is higher than 91%!!!\n")
                    print ("Depending on your disks configuration/type your util column could be high (SSD/RAID) accept higher")
                    break
        if self.tps_count < 3:
            print ("I don't see very high %util in your disk's, I think they are working well")


    def print_tps_util(self):
        print ("Your disks tps, avgqusz and util data")
        for line in self.tps_util_tup:
            if line.tps > 75 or line.util > 91:
                print ("Disk: {} - TPS/IPS: {} - AVGQUSZ: {} - UTIL: {}".format(line.Device, line.tps, line.avgqusz, line.util))
            else:
                print ("Disk: {} - TPS/IPS: {} - AVGQUSZ: {} - UTIL: {}".format(line.Device, line.tps, line.avgqusz, line.util))

# Print Message when you delete the Instance with del (instanceName)
    def __del__(self):
        print ("Instance of Class Iostat,  Removed")
