import pathlib
import subprocess

from launcher.commands.build import build
from launcher.config import check_config_exists


def run(
    init: bool = False,
    repo: str = "origin",
    branch: str = "main",
    do_update: bool = False,
    test: bool = False,
    clear: bool = False,
):
    """🚀 Launch Grandma SkyPortal"""
    if init or do_update:
        build(
            init=init,
            repo=repo,
            branch=branch,
            do_update=do_update,
            clear=clear,
        )

    # create common docker network (if it does not exist yet)
    if test:
        cmd = subprocess.Popen(["make", "run_testing"], cwd="patched_skyportal")
        cmd.communicate()
    else:
        cmd = subprocess.Popen(["make", "run"], cwd="patched_skyportal")
        cmd.communicate()
