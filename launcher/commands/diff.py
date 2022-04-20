import subprocess
import time
from pathlib import Path

import yaml

def diff(
    init: bool = False,
):
    # function that checks what changes have been made to a submodule since the last time we pulled it
    # if there are changes, we display them and ask the user if they want to apply them
    # else we just return

    cmd = subprocess.Popen(["git", "fetch", "origin"], stdout=subprocess.PIPE, cwd="skyportal")
    output = cmd.wait()
    cmd = subprocess.Popen(["git", "diff", "master"], stdout=subprocess.PIPE, cwd="skyportal")
    # get the ouput of the command
    output = cmd.stdout.read()
    output = output.decode("utf-8")
    output = output.split("\n")
    output = [x for x in output if x != ""]
    # find the name of the files that have changed
    changed_files = []
    for line in output:
        if ("a/") in line:
            changed_files.append(line.split("a/")[1].split(" ")[0])
        elif ("b/") in line:
            changed_files.append(line.split("b/")[1].split(" ")[0])

    # check if those files exist in extensions/skyportal/
    exist_in_extensions = []
    for file in set(changed_files):
        if Path("extensions/skyportal/" + file).exists():
            exist_in_extensions.append(file)
    
    # if there are changes, ask the user if he wants to continue, return true or false
    if len(exist_in_extensions) > 0:
        print("The following files from skyportal for which we have a modified version have been changed:")
        for file in exist_in_extensions:
            print(file)
        print("Do you want to continue? If you answer yes, the extensions will overwrite those changes, potentially missing on newer functionnalities. (y/n)")
        answer = input()
        if answer == "y":
            return True
        else:
            return False
    else:
        return True

    


    