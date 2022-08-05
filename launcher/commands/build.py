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
    branch: str = "main",
    do_update: bool = False,
    clear: bool = False,
    update_prod: bool = False,
):
    """Build Icare
    :param init: Initialize Icare
    :param repo: Remote repository to pull from
    :param do_update: pull <repo>/<branch>, autostash SP and update submodules
    :param clear: Clear the database
    """
    # if previous_skyportal directory doesnt exist, create it and copy the skyportal files in it
    previous_skyportal_dir = Path("previous_skyportal")
    if not previous_skyportal_dir.exists():
        previous_skyportal_dir.mkdir()
        cmd = subprocess.Popen(["cp", "-a", "skyportal/.", "previous_skyportal/"])
        cmd.wait()

    new_changes = False
    skyportal_start = True
    if do_update:
        new_changes, skyportal_start = update(repo=repo, branch=branch)
    if update_prod:
        print("Stamping current database state")
        cmd = subprocess.Popen(
            ["alembic", "-x", "config=config.yaml", "stamp", "head"],
            cwd="patched_skyportal",
        )
        cmd.wait()
        print("Updating submodules")
        cmd = subprocess.Popen(["git", "submodule", "update", "--init", "--recursive"])
        cmd.wait()
    # if patched_skyportal directory exists, patch it
    patched_skyportal_dir = Path("patched_skyportal")
    exists = patched_skyportal_dir.exists()
    if not exists:
        patched_skyportal_dir.mkdir()

    if new_changes or not exists or update_prod:
        # copy skyportal to patched_skyportal
        cmd = subprocess.Popen(["cp", "-a", "skyportal/.", "patched_skyportal/"])
        cmd.wait()
        cmd = subprocess.Popen(["rm", "-rf", "patched_skyportal/.git"])
    else:
        print(
            "No changes detected, not copying skyportal to patched_skyportal, but still patching it"
        )

    patch_skyportal("extensions/skyportal/", "patched_skyportal/")

    if clear and skyportal_start:
        clear_db()

    if init and skyportal_start:
        # run the command make run in skyportal dir
        cmd = subprocess.Popen(["make", "db_init"], cwd="patched_skyportal")
        cmd.wait()

    return skyportal_start
