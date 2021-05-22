# meplotter
A very simple Chia Plotting script. This script allows you start different
chia plotting instances in different windows, and specify the delay after
which each should start.

It does not try to actively manage the process. Each window is independent.

To use it, go to the plotters.yaml file and configure the folder of your
plotters. Name each plotter differently.

Afterwards, you can run a plotter with this command:

python3 meplotter.py Plotter1 --delay 60m

For now, the script will only run on Ubuntu.

## Sync
The sync.py script can be used to move your completed files to another server.
You need to setup ssh keys for automatic login to make it work.
