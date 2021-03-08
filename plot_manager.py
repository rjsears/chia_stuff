#!/usr/bin/python3

# -*- coding: utf-8 -*-

__author__ = 'Richard J. Sears'
VERSION = "0.1 (2021-03-07)"


### Simple python script that helps to move my chia plots from my plotter to
### my nas. I wanted to use netcat as it was much faster on my 10GBe link than
### rsync and the servers are secure so I wrote this script to manage that
### move process. It will get better with time as I add in error checking and
### other things like notifications and stuff.

import os
import subprocess

# This is where our plots live before we move them
plot_dir = "/mnt/ssdraid/array0/"


def get_list_of_plots():
    plot_to_process = (os.listdir(plot_dir)[0])
    if os.path.getsize(plot_dir + plot_to_process) >= 108644374730:
        return (plot_to_process)
    else:
        return False

def process_plot():
    if get_list_of_plots() and not check_process_status():
        set_running_status('start')
        plot = get_list_of_plots()
        plot_path = plot_dir + plot
        subprocess.call(['/home/chia/send_file.sh', plot_path, plot])
        set_running_status('stop')
        os.remove(plot_path)
    else:
        return

def check_process_status():
    status_file = "job_running"
    if os.path.isfile(status_file):
        status = True
    else:
        status = False
    return status

def set_running_status(status):
    if status == "start":
        os.open("job_running", os.O_CREAT)
    if status == "stop":
        os.remove("job_running")


def main():
    process_plot()


if __name__ == '__main__':
    main()
