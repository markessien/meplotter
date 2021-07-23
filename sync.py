import os
import yaml
import time
import subprocess


settings_file = "sync.yaml"

while True:

    print("Checking for new files...\n")

    start_time = time.time()

    with open(settings_file, 'r') as stream:
        print("Loaded settings file: " + settings_file)
        sync_settings = yaml.safe_load(stream)


    for sync_name, sync in sync_settings.items():
        src = os.path.join(sync["Src"], "*.plot")
        dst = sync["Dst"]
        host = sync["Host"]
        username = sync["Username"]

        command = "rsync -av --progress --remove-source-files " + src + " " + dst
        print("Running: " + command)
        subprocess.call(command, shell=True)
    
    exec_time = time.time() - start_time
    if exec_time < 180:
        time.sleep(180)


    
