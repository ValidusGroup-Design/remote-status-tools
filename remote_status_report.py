#!/usr/bin/env python3
# ------------------------------------------------------------------------------
# remote_status_report.py
#
# A lightweight remote CLI system status tool for Linux-based SBCs and servers.
# Developed by Validus Group Inc. for internal monitoring and diagnostic use.
#
# Copyright (c) 2025 Validus Group Inc. <ffisher@validusgroup.com>
#
# MIT License
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ------------------------------------------------------------------------------

import os
import socket
import shutil
import subprocess
from glob import glob

def get_hostname():
    return socket.gethostname()

def get_uptime():
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
    except Exception as e:
        return f"Error: {e}"

def get_cpu_info():
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "cpu model" in line.lower():
                    return line.split(":", 1)[1].strip()
        return "Unknown CPU"
    except Exception as e:
        return f"Unavailable ({e})"

def get_cpu_cores():
    try:
        return os.cpu_count()
    except:
        return "Unavailable"

def get_load_average():
    try:
        load1, load5, load15 = os.getloadavg()
        return f"1 min: {load1:.2f}, 5 min: {load5:.2f}, 15 min: {load15:.2f}"
    except:
        return "Unavailable"

def get_cpu_temp():
    try:
        thermal_zones = sorted(glob("/sys/class/thermal/thermal_zone*/temp"))
        for zone in thermal_zones:
            with open(zone) as f:
                millidegrees = int(f.read().strip())
                if millidegrees > 0:
                    return f"{millidegrees / 1000.0:.1f}°C"
        return "Unavailable"
    except:
        return "Unavailable"

def get_memory_usage():
    try:
        with open("/proc/meminfo") as f:
            lines = {line.split(':')[0]: int(line.split()[1]) for line in f}
        total = lines["MemTotal"] // 1024
        free = lines["MemAvailable"] // 1024
        used = total - free
        return f"Used: {used} MB / Total: {total} MB"
    except:
        return "Unavailable"

def get_disk_usage():
    try:
        total, used, free = shutil.disk_usage("/")
        return f"Used: {used // (2**30)} GB / Total: {total // (2**30)} GB"
    except:
        return "Unavailable"

def get_ip_address():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        if ip.startswith("127."):
            ip = subprocess.check_output("hostname -I", shell=True).decode().split()[0]
        return ip
    except:
        return "Unavailable"

def main():
    print("\n===== REMOTE STATUS REPORT =====\n")
    print(f"Hostname        : {get_hostname()}")
    print(f"Uptime          : {get_uptime()}")
    print(f"CPU             : {get_cpu_info()}")
    print(f"CPU Cores       : {get_cpu_cores()}")
    print(f"Load Average    : {get_load_average()}")
    print(f"CPU Temp        : {get_cpu_temp()}")
    print(f"Memory          : {get_memory_usage()}")
    print(f"Disk            : {get_disk_usage()}")
    print(f"IP Address      : {get_ip_address()}")
    print("\n=================================\n")

if __name__ == "__main__":
    main()
