import subprocess
import time
from pathlib import Path

import yaml

from launcher.commands import update
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
    if do_update:
        update(init=init, repo=repo, branch=branch)

    patch_skyportal()

    if init:
        # run the command make run in skyportal dir
        cmd = subprocess.Popen(["make", "db_init"], cwd="skyportal")
        cmd.wait()
    


    


