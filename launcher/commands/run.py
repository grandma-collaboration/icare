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
    update_prod: bool = False,
):
    """🚀 Launch Icare"""
    skyportal_start = True
    if init or do_update or update_prod:
        skyportal_start = build(
            init=init,
            repo=repo,
            branch=branch,
            do_update=do_update,
            clear=clear,
            update_prod=update_prod,
        )

    # create common docker network (if it does not exist yet)
    if skyportal_start:
        if test:
            cmd = subprocess.Popen(["make", "run_testing"], cwd="patched_skyportal")
            cmd.communicate()
        else:
            cmd = subprocess.Popen(["make", "run"], cwd="patched_skyportal")
            cmd.communicate()
    else:
        print("App will not start as the extensions need to be updated")
