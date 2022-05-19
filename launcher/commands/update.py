import subprocess
from typing import Optional
from launcher.commands.diff import diff


def update(
    repo: Optional[str] = None,
    branch: Optional[str] = None,
):
    """Update grandma
    :param init: Initialize before updating grandma
    :param repo: Remote repository to pull from
    :param branch: Branch on the remote repository
    """

    # show diff between patched skyportal and skyportal
    if diff():
        # update submodules
        git_pull_command = ["git", "pull"]
        if repo is not None and branch is not None:
            p = subprocess.run(["git", "checkout", branch], cwd="skyportal")
            if p.returncode != 0:
                raise RuntimeError("Failed to update grandma's submodules")
            p = subprocess.run(git_pull_command, cwd="skyportal")
            if p.returncode != 0:
                raise RuntimeError("Failed to git pull grandma")
        return True
    else:
        return False
