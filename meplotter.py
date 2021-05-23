import os
import sys
import yaml
import glob
import time
import argparse
import subprocess

from pathlib import Path
from durations import Duration

'''
Usage: python3 meplotter.py Plotter1 --delay 30m

If you want to delete temp folder
python3 meplotter.py Plotter1 --cleanup 1 --delay 30m

'''

parser = argparse.ArgumentParser(description='Manage your Plotting')
parser.add_argument('plotters', nargs='*', help='The name(s) of the plotter(s) as specified in the settings')

parser.add_argument('--delay', help='Time to delay before starting (e.g 10m, 3h)')
parser.add_argument('--cleanup', help='Delete all tmp files in the temporary directory')
parser.add_argument("--settings", help="Specify the settings file")

args = parser.parse_args()


chia_folder = os.path.join(Path.home(), "chia-blockchain/")
k_type = "32"
queue_length = 10
memory_size = 3389
number_threads = 2
settings_file = "plotters.yaml"

print("Welcome to the MePlotter")

print("Starting " + str(args.plotters))

if args.settings:
    settings_file = args.settings

commands = []

for i, plotter in enumerate(args.plotters):

    # Read settings file
    with open(settings_file, 'r') as stream:
        print("Loaded settings file: " + settings_file)
        plotting_settings = yaml.safe_load(stream)

        plotter_settings = plotting_settings[plotter]

        tmp_folder = plotter_settings['Tmp']
        dst_folder = plotter_settings['Dst']

        if 'Type' in plotter_settings:
            k_type = plotter_settings['Type']

        if 'Queue' in plotter_settings:
            queue_length = plotter_settings['Queue']

        if 'Memory' in plotter_settings:
            memory_size = plotter_settings['Memory']

        if 'Threads' in plotter_settings:
            number_threads = plotter_settings['Threads']

        print("Executing " + plotter)

    if not tmp_folder or not dst_folder:
        print("Your destination or temp folders are not set")
        exit()

    if args.cleanup:
        print("Cleaning up the folders")
        files = glob.glob(os.path.join(tmp_folder, "*.tmp"))
        for f in files:
            os.remove(f)

    try:
        os.makedirs(tmp_folder)
    except:
        pass

    try:
        os.makedirs(dst_folder)
    except:
        pass

    sleep_cmd = ""
    if args.delay:
        
        delay = Duration(args.delay)
        delay_s = delay.to_seconds()
        if len(args.plotters) > 1:
            delay_s += delay_s*(i-1)

        print("Waiting for " + str(delay))
        sleep_cmd = "echo MePlotter. " + plotter + " waiting for " + str(delay_s) + "s... && sleep " + str(delay_s) + " && "

    
    command = sleep_cmd + ". " + os.path.join(chia_folder, 'activate') + " && " + \
                os.path.join(chia_folder, 'venv/bin/chia') + \
                " plots create" + \
                " -k " + str(k_type) + \
                " -n " + str(queue_length) + \
                " -t " + tmp_folder + \
                " -d " + dst_folder + \
                " -b " + str(memory_size) + \
                " -u 128" + \
                " -r " + str(number_threads)

    commands.append(command)

terminal_cmd = "gnome-terminal"
for cmd in commands:
    terminal_cmd = terminal_cmd + " --tab -e 'bash -c \"" + cmd + "; read -n1\"'"
print(terminal_cmd)

subprocess.run([terminal_cmd], shell=True, stdout=sys.stdout)