import subprocess
import time
from pathlib import Path

import yaml

from launcher.commands.update import update
from launcher.commands.clear import clear as clear_db
from launcher.config import check_config
from launcher.skyportal import (
    patch as patch_skyportal,
)


def build(
    init: bool = False,
    repo: str = "origin",
    branch: str = "master",
    do_update: bool = False,
    clear: bool = False,
):
    """Build grandma
    :param init: Initialize grandma
    :param repo: Remote repository to pull from
    :param do_update: pull <repo>/<branch>, autostash SP and update submodules
    :param clear: Clear the database
    """
    new_changes = True
    if do_update and not init:
        new_changes = update(repo=repo, branch=branch)

    # if patched_skyportal directory exists, patch it
    patched_skyportal_dir = Path("patched_skyportal")
    if not patched_skyportal_dir.exists():
        patched_skyportal_dir.mkdir()

    if new_changes:
        # copy skyportal to patched_skyportal
        cmd = subprocess.Popen(["cp", "-a","skyportal/.","patched_skyportal/"])
        cmd.wait()
        cmd = subprocess.Popen(["rm", "-rf","patched_skyportal/.git"])
        patch_skyportal("extensions/skyportal/", "patched_skyportal/")
    else: 
        print("No changes detected, skipping patching")

    if clear:
        clear_db()

    if init:
        # run the command make run in skyportal dir
        cmd = subprocess.Popen(["make", "db_init"], cwd="patched_skyportal")
        cmd.wait()
    


    


