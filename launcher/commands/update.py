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
    git_pull_command = ["git", "pull"]
    if repo is not None and branch is not None:
        git_pull_command.extend([repo, branch])
    p = subprocess.run(git_pull_command)
    if p.returncode != 0:
        raise RuntimeError("Failed to git pull grandma")
    # auto stash SP
    p = subprocess.run(["git", "stash"], cwd="skyportal")
    if p.returncode != 0:
        raise RuntimeError("SkyPortal autostash failed")

    # show diff between patched skyportal and skyportal
    if diff():
        # update submodules
        p = subprocess.run(["git", "checkout", "master"], cwd="skyportal")
        if p.returncode != 0:
            raise RuntimeError("Failed to update grandma's submodules")
        return True
    else:
        return False