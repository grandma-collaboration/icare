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

    cmd = subprocess.Popen(["git", "fetch"], stdout=subprocess.PIPE, cwd="skyportal")
    output = cmd.wait()
    cmd = subprocess.Popen(
        ["git", "diff", "origin/main"], stdout=subprocess.PIPE, cwd="skyportal"
    )
    # get the ouput of the command
    output = cmd.stdout.read()
    output = output.decode("utf-8")
    output = output.split("\n")
    output = [x for x in output if x != ""]
    # find the name of the files that have changed
    changed_files = []
    new_baselayer = None
    for i in range(len(output)):
        if "diff --git a/baselayer b/baselayer" in output[i]:
            new_baselayer = output[i + 1].split(" ")[1].split("..")[0]
        elif ("a/") in output[i]:
            changed_files.append(output[i].split("a/")[1].split(" ")[0])
        elif ("b/") in output[i]:
            changed_files.append(output[i].split("b/")[1].split(" ")[0])

    #'diff --git a/baselayer b/baselayer', 'index a9100c56..29045fa6 160000'
    # find the hash of the baselayer pinned in the main branch
    if new_baselayer is not None:
        cmd = subprocess.Popen(
            ["git", "diff", new_baselayer],
            stdout=subprocess.PIPE,
            cwd="skyportal/baselayer",
        )
        # get the ouput of the command
        output = cmd.stdout.read()
        output = output.decode("utf-8")
        output = output.split("\n")
        output = [x for x in output if x != ""]
        # find the name of the files that have changed
        for line in output:
            if ("a/") in line:
                changed_files.append("baselayer/" + line.split("a/")[1].split(" ")[0])
            elif ("b/") in line:
                changed_files.append("baselayer/" + line.split("b/")[1].split(" ")[0])

    # remove "baselayer" from the list of changed files
    changed_files = [x for x in changed_files if x != "baselayer"]
    # check if those files exist in extensions/skyportal/
    exist_in_extensions = []
    for file in set(changed_files):
        if Path("extensions/skyportal/" + file).exists():
            exist_in_extensions.append(file)

    # if there are changes, ask the user if he wants to continue, return true or false
    if len(exist_in_extensions) > 0 and len(changed_files) > 0:
        print(
            "The following files from skyportal for which we have a modified version have been changed:\n"
        )
        for file in exist_in_extensions:
            print(file)
        while True:
            print(
                "\n1. Cancel starting the app to attempt automatically merging the new changes in the extensions folder"
            )
            print("2. Cancel the update and start skyportal as is")
            print(
                "3. Ignore and force the update, potentially overwriting new change and breaking the app\n"
            )
            choice = input("Please choose an option: ")
            if choice.lower() == "1":
                return True, True, False, exist_in_extensions
            elif choice.lower() == "2":
                return False, False, True, None
            elif choice.lower() == "3":
                return True, False, True, None
            else:
                print("Invalid answer. Select again: ")

    elif len(changed_files) > 0:
        return True, False, True, None
    else:
        return False, False, True, None
