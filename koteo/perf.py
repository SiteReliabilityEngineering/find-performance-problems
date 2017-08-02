#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Koldo Oteo Orellana (koldo.oteo@gmail.com)
###
import time
import os, sys
import psutil
import subprocess

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
        
    def exec_vmstat(self):
        self.vm = subprocess.Popen(['vmstat', '-n', '2', '9'], shell=False, stdout=subprocess.PIPE).stdout
        try:
            self.vmstat_lst = [[elem.split()] for elem in self.vm.read().splitlines() if (not elem.startswith(b'procs')) if (not elem.startswith(b' r'))]
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
            
    def chk_cpu_use(self):
        self.calc_cpuavg = sum(self.real_data['us_col'] + self.real_data['sy_col'] + self.real_data['st_col']) / self.lst_len-1
        if self.calc_cpuavg >= 80 and self.calc_cpuavg < 90:
            return "Look your CPU usage, it's high. CPU %s usage" % (self.calc_cpuavg)
        elif self.calc_cpuavg > 90:
            return "Look your CPU usage, it's VERY high. CPU %s usage" % (self.calc_cpuavg)
        else:
            return "The CPU usage is below 80%. CPU %s usage" % (self.calc_cpuavg)
        
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
