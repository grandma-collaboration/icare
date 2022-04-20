import subprocess
import time
from pathlib import Path

import yaml

from launcher.commands.update import update
from launcher.config import check_config
from launcher.skyportal import (
    patch as patch_skyportal,
)


def build(
    init: bool = False,
    repo: str = "origin",
    branch: str = "master",
    do_update: bool = False,
):
    """Build grandma
    :param init: Initialize grandma
    :param repo: Remote repository to pull from
    :param branch: Branch on the remote repository
    :param traefik: Build grandma to run behind Traefik
    :param no_kowalski: Do not build images for Kowalski
    :param do_update: pull <repo>/<branch>, autostash SP and update submodules
    :param skyportal_tag: Tag to apply to SkyPortal docker image
    :param yes: agree with all potentially asked questions
    """
    new_changes = False
    if do_update and not init:
        new_changes = update(init=init, repo=repo, branch=branch)

    # if patched_skyportal directory exists, patch it
    patched_skyportal_dir = Path("patched_skyportal")
    if not patched_skyportal_dir.exists():
        patched_skyportal_dir.mkdir()

    if new_changes:
        # copy skyportal to patched_skyportal
        cmd = subprocess.Popen(["cp", "-a","skyportal/.","patched_skyportal/"])
        cmd.wait()
        patch_skyportal("extensions/skyportal/", "patched_skyportal/")
    else: 
        print("No changes detected, skipping patching")

    if init:
        cmd = subprocess.Popen(["cp", "-a","skyportal/.","patched_skyportal/"])
        cmd.wait()
        # run the command make run in skyportal dir
        cmd = subprocess.Popen(["make", "db_init"], cwd="patched_skyportal")
        cmd.wait()
    


    


