import os
import subprocess

from launcher.commands.build import build


def run(
    init: bool = False,
    repo: str = "origin",
    branch: str = "main",
    do_update: bool = False,
    test: bool = False,
    clear: bool = False,
    update_prod: bool = False,
    production: bool = False,
    skip_services_check: bool = False,  # not used here
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
        elif production:
            # we want to run all of the following:
            # export NPM_CONFIG_LEGACY_PEER_DEPS=true && make system_setup && ./node_modules/.bin/webpack --mode=production && make run_production
            # but we need to run them in the patched_skyportal directory
            env = os.environ.copy()
            env["NPM_CONFIG_LEGACY_PEER_DEPS"] = "true"
            cmd = subprocess.Popen(
                ["make", "system_setup"],
                cwd="patched_skyportal",
                env=env,
            )
            cmd.communicate()
            print("\nBuilding webpack, this may take a while...")
            cmd = subprocess.Popen(
                ["./node_modules/.bin/webpack", "--mode=production"],
                cwd="patched_skyportal",
                env=env,
            )
            cmd.communicate()
            cmd = subprocess.Popen(
                ["make", "run_production"],
                cwd="patched_skyportal",
                env=env,
            )
            cmd.communicate()
        else:
            # we just run make run
            env = os.environ.copy()
            env["NPM_CONFIG_LEGACY_PEER_DEPS"] = "true"
            cmd = subprocess.Popen(["make", "run"], cwd="patched_skyportal", env=env)
            cmd.communicate()
    else:
        print("App will not start as the extensions need to be updated")
