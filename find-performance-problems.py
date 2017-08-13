#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# title           :find-performance-problems
# author          :Koldo Oteo Orellana <koldo.oteo@gmail.com>
# date            :Aug 13 2017
# version         :0.1
# usage           :./find-performance-problems
# python_version  :3.x
#=============================================================
from koteo import __version__, __author__
from koteo import Resources
from koteo import SomePerf
from koteo import Iostat
from koteo import Vmstat
import os

def cls():
    os.system('clear')


def menu():
    cls()

    print ("Welcome to Find Performance Problems Tool v{} for Linux and Python 3.x".format(__version__))
    print ("Author: {}".format(__author__))
    print ("\tSelect an option: ")
    print ("\t\t1) I will show you a basic view of your resources (cpu/mem/swap) ")
    print ("\t\t2) All in one 'Deep analysis' Menu ")
    print ("\t\t3) CPU Bottleneck Menu 'Deep analysis' Menu ")
    print ("\t\t4) Swap 'Deep analysis' Menu")
    print ("\t\t5) IO 'Deep analysis' Menu")
    print ("\t\t6) Exit ")


def resources_menu():
    cls()

    res = Resources()
    res.cpu_use()
    res.prt_mem()
    res.prt_swp()

def all_in_one():
    cls()

    print ("*" * 15, "CPU analysis", "*" * 15)
    print ('\n')
    vm = Vmstat()
    io = Iostat()
    vm.exec_vmstat()
    print(vm.chk_cpu_use())
    print (vm.chk_procs_waiting())
    print ('\n')

    print ("*" * 15, "Swap analysis", "*" * 15)
    print ('\n')
    print (vm.chk_swapping())
    print ('\n')

    print ("*" * 15, "IO analysis", "*" * 15)
    print ('\n')
    io.exec_iostat()
    io.format_iostat()
    print (io.chk_tps())
    print(io.chk_util())
    print (io.print_tps_util())



menu()
resources_menu()
all_in_one()

