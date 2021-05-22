import os
import yaml
import time
import subprocess


settings_file = "sync.yaml"

while True:

    print("Checking for new files...\n")

    with open(settings_file, 'r') as stream:
        print("Loaded settings file: " + settings_file)
        sync_settings = yaml.safe_load(stream)

    for sync_name, sync in sync_settings.items():
        src = os.path.join(sync["Src"], "*.plot")
        dst = sync["Dst"]
        host = sync["Host"]
        username = sync["Username"]

        command = "rsync -av --progress --remove-source-files " + src + " " + username + "@" + host + ":" + dst
        print("Running: " + command)
        subprocess.call(command, shell=True)
    
    time.sleep(180)


    