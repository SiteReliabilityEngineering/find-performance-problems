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
from koteo import __version__
from koteo import Resources
from koteo import SomePerf
from koteo import Iostat
from koteo import Vmstat
import os

def cls():
    os.system('cls')


def menu():
    cls()

    print ("Welcome to Find Performance Problems Tool v{} for Linux and Python 3.x".format(__version__))
    print ("\tSelect an option: ")
    print ("\t\t1) I will show you a basic view of your resources (cpu/mem/swap) ")
    print ("\t\t2) All in one 'Deep analysis' Menu ")
    print ("\t\t3) CPU Bottleneck Menu 'Deep analysis' Menu ")
    print ("\t\t4) Memory 'Deep analysis' Menu")
    print ("\t\t5) Swap 'Deep analysis' Menu")
    print ("\t\t6) Disk 'Deep analysis' Menu")
    print ("\t\t7) Exit ")


def resources_menu():
    cls()

    res = Resources()
    res.cpu_use()
    res.prt_mem()
    res.prt_swp()


menu()