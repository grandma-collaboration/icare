import subprocess
from typing import Optional
from launcher.commands.diff import diff
from pathlib import Path


def update(
    repo: Optional[str] = None,
    branch: Optional[str] = None,
):
    """Update Icare
    :param init: Initialize before updating Icare
    :param repo: Remote repository to pull from
    :param branch: Branch on the remote repository
    """

    # show diff between patched skyportal and skyportal
    p = subprocess.run(["git", "pull", "origin", "main"], cwd="skyportal")
    if p.returncode != 0:
        raise RuntimeError("Failed to pull new changes")
    p = subprocess.run(["git", "submodule", "update", "--init", "--recursive"])
    if p.returncode != 0:
        raise RuntimeError("Failed to update all submodules recursively")
    skyportal_update, extensions_update, skyportal_start, exists_in_extensions = diff()
    if extensions_update:
        previous_skyportal_dir = Path("previous_skyportal")
        if not previous_skyportal_dir.exists():
            previous_skyportal_dir.mkdir()
        subprocess.run(["cp", "-r", "skyportal", "previous_skyportal"])
        # update submodules
    if skyportal_update:
        if repo is not None and branch is not None:
            p = subprocess.run(["git", "checkout", branch], cwd="skyportal")
            if p.returncode != 0:
                raise RuntimeError("Failed to update icare's submodules")
            p = subprocess.run(["git", "pull"], cwd="skyportal")
            if p.returncode != 0:
                raise RuntimeError("Failed to git pull icare")
            p = subprocess.run(
                ["git", "submodule", "update", "--init", "--recursive"], cwd="skyportal"
            )
            if p.returncode != 0:
                raise RuntimeError("Failed to update all submodules recursively")
    if extensions_update:
        print("\n")
        for file in exists_in_extensions:
            command = [
                "git",
                "merge-file",
                "extensions/skyportal/" + file,
                "previous_skyportal/" + file,
                "skyportal/" + file,
            ]
            subprocess.run(command)
            print("Updated " + file)
        print(
            "\nDone updating extensions. Please go to the extensions folder, solve potential merge conflicts and start the app again with the --init flag instead"
        )
        # replace previous_skyportal with skyportal
        cmd = subprocess.Popen(["cp", "-a", "skyportal/.", "previous_skyportal/"])
        cmd.wait()
    return skyportal_update, skyportal_start
