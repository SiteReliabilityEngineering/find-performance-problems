import time
import os
import psutil
import subprocess


class Vmstat(object):
    """With this class we are going to create some methods, that
       query the vmstat system command. We will query cpu, memory and
       swap performance data"""
       
    def __init__(self):
        self.vm = subprocess.Popen(["vmstat", "-n", "2", "9"], shell=False, stdout=subprocess.PIPE).stdout
        self.vmstat_lst = [[elem.split()] for elem in self.vm.read().splitlines() if (not elem.startswith(b'procs')) if (not elem.startswith(b' r'))]
        self.lst_len = len(self.vmstat_lst)
        
        ''' We create a list into a dict with the next data:
        r_col: 'r' column with number of processes waiting for run time
        si/so_col: swapped in/out, us_col: user cpu time
        sy_col: kernel cpu time ; st_col: Time stolen from a vmachine'''
        
        self.real_data = {'r_col': [], 'si_col': [], 'so_col': [], 'us_col': [], 'sy_col': [], 'st_col': []}
        for elem in self.vmstat_lst[1:self.lst_len + 1]:
            self.real_data['r_col'].append(int(elem[0][0])) # r_col
            self.real_data['si_col'].append(int(elem[0][6])) # si_col
            self.real_data['so_col'].append(int(elem[0][7])) # so_col
            self.real_data['us_col'].append(int(elem[0][12])) # us_col
            self.real_data['sy_col'].append(int(elem[0][13])) # sy_col
            self.real_data['st_col'].append(int(elem[0][16])) # st_col

    def chkprocwa(self):
        '''First we loop the vmstat_lst multidimensional array and we
           set every column into a var'''
        for elem in self.vmstat_lst[1:self.lst_len + 1]:
            self.proc_w == int(elem[0][0]) #The number of processes waiting for run time
            return self.proc_w
