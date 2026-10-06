import subprocess
from pathlib import Path
from typing import Optional

from launcher.commands.diff import diff


def update(
    repo: Optional[str] = None,
    branch: Optional[str] = None,
    commit: Optional[str] = None,
):
    """Update Icare
    :param repo: Remote repository to pull from
    :param branch: Branch on the remote repository
    :param commit: Specific SkyPortal commit hash to pin to (overrides branch tip)
    """

    p = subprocess.run(["git", "submodule", "update", "--init", "--recursive"])
    if p.returncode != 0:
        raise RuntimeError("Failed to update all submodules recursively")
    skyportal_update, extensions_update, skyportal_start, exists_in_extensions = diff(
        commit=commit
    )
    if extensions_update:
        previous_skyportal_dir = Path("previous_skyportal")
        if not previous_skyportal_dir.exists():
            previous_skyportal_dir.mkdir()
        subprocess.run(["cp", "-r", "skyportal", "previous_skyportal"])
        # update submodules
    if skyportal_update:
        if commit is not None:
            p = subprocess.run(["git", "fetch"], cwd="skyportal")
            if p.returncode != 0:
                raise RuntimeError("Failed to fetch skyportal")
            p = subprocess.run(["git", "checkout", commit], cwd="skyportal")
            if p.returncode != 0:
                raise RuntimeError(f"Failed to checkout skyportal commit {commit}")
            p = subprocess.run(
                ["git", "submodule", "update", "--init", "--recursive"], cwd="skyportal"
            )
            if p.returncode != 0:
                raise RuntimeError("Failed to update all submodules recursively")
        elif repo is not None and branch is not None:
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
            ext_file = Path("extensions/skyportal/" + file)
            if ext_file.exists() and "<<<<<<< " in ext_file.read_text():
                print(
                    f"Skipping {file}: already has unresolved conflict markers. Please resolve conflicts first."
                )
                continue
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
