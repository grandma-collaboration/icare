import subprocess
import json
from distutils.dir_util import copy_tree
from .commands.apply_config import apply_config


def patch(source="extensions/skyportal/", destination="patched_skyportal/"):
    """Make icare-specific file modifications to SkyPortal."""
    print("\n Applying icare-specific patches to SkyPortal")

    # add icare-specific SP extensions
    copy_tree(source, destination)

    # add icare-specific dependencies for SP
    # js
    with open(source + "package.icare.json", "r") as f:
        icare_pkg = json.load(f)
    with open(destination + "package.json", "r") as f:
        skyportal_pkg = json.load(f)

    skyportal_pkg["dependencies"] = {
        **skyportal_pkg["dependencies"],
        **icare_pkg["dependencies"],
    }
    with open(destination + "package.json", "w") as f:
        json.dump(skyportal_pkg, f, indent=2)

    # python
    with open(".requirements/ext.txt", "r") as f:
        ext_req = f.readlines()
    with open(destination + "requirements.txt", "r") as f:
        skyportal_req = f.readlines()
    with open(destination + "requirements.txt", "w") as f:
        f.writelines(skyportal_req)
        for line in ext_req:
            if line not in skyportal_req:
                f.write(line)

    apply_config()
