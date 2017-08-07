#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Koldo Oteo Orellana (koldo.oteo@gmail.com)
###

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

def get_cpus():
    return psutil.cpu_count(logical=True)

