import os
import sys
import yaml
import glob
import time
import argparse
import subprocess

from pathlib import Path
from durations import Duration

parser = argparse.ArgumentParser(description='Manage your Plotting')
parser.add_argument('name', help='The name of the plotter as specified in the settings')

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

if args.settings:
    settings_file = args.settings

if args.delay:
    delay = Duration(args.delay)
    print("Waiting for " + str(delay))
    time.sleep(delay.to_seconds())

# Read settings file
with open(settings_file, 'r') as stream:
    print("Loaded settings file: " + settings_file)
    plotting_settings = yaml.safe_load(stream)

    plotter_settings = plotting_settings[0][args.name]

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

if not tmp_folder or not dst_folder:
    print("Your destination or temp folders are not set")
    exit()

if args.cleanup:
    try:
        os.makedirs(tmp_folder)
    except FileExistsError:
        pass

    try:
        os.makedirs(dst_folder)
    except FileExistsError:
        pass

print("Welcome to the MePlotter")

files = glob.glob(os.path.join(tmp_folder, "*.tmp"))
for f in files:
    os.remove(f)

command = ". " + os.path.join(chia_folder, 'activate') + " && " + \
            os.path.join(chia_folder, 'venv/bin/chia') + \
            " plots create" + \
            " -k " + str(k_type) + \
            " -n " + str(queue_length) + \
            " -t " + tmp_folder + \
            " -d " + dst_folder + \
            " -b " + str(memory_size) + \
            " -u 128" + \
            " -r " + str(number_threads)

subprocess.run([command], shell=True, stdout=sys.stdout)