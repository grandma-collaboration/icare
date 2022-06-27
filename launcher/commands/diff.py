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

    cmd = subprocess.Popen(
        ["git", "fetch"], stdout=subprocess.PIPE, cwd="skyportal"
    )
    output = cmd.wait()
    cmd = subprocess.Popen(
        ["git", "diff", "main"], stdout=subprocess.PIPE, cwd="skyportal"
    )
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
    if len(exist_in_extensions) > 0 and len(changed_files) > 0:
        print(
            "The following files from skyportal for which we have a modified version have been changed:"
        )
        for file in exist_in_extensions:
            print(file)
        print(
            "Do you want to update those files now ? If yes, we won't start the app but instead attempt to automatically merge the new changes in the extensions folder. If no, the update will be cancelled and skyportal with start as is (y/n)"
        )
        print(
            "Otherwise, just hit enter and this will be ignored and force the update, potentially overwriting new changes\n"
        )
        answer = input()
        if answer.lower() == "y" or answer.lower() == "yes":
            return True, True, False, exist_in_extensions
        elif answer.lower() == "n" or answer.lower() == "no":
            return False, False, True, None
        else:
            return True, False, True, None
    elif len(changed_files) > 0:
        return True, False, True, None
    else:
        return False, False, True, None
