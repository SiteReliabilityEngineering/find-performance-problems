#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Koldo Oteo Orellana (koldo.oteo@gmail.com)
###
import os
### Vars
onemb = 1048576
tenmb = 10485760
hmb = 104857600
onegb = 1073741824
tengb = 10737418240
hgb = 107374182400
###

# Convert bytes to human readable
def bytes_to(bytes):
    if bytes < onemb:
        return ("{:.1f} Bytes".format(bytes))
    elif bytes < onegb:
        return ("{:.1f} Mb".format(bytes / 1024 / 1024, '.2f'))
    elif bytes >= onegb:
        return ("{:.1f} Gb".format(bytes / 1024 / 1024 / 1024, '.2f'))

# Get number of CPUS
def get_cpus():
    cpusn = os.sysconf("SC_NPROCESSORS_ONLN")
    if cpusn > 0:
        return cpusn
