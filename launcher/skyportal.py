import subprocess
import json
from distutils.dir_util import copy_tree


def patch():
    """Make grandma-specific file modifications to SkyPortal."""
    print("Applying grandma-specific patches to SkyPortal")

    # add grandma-specific SP extensions
    copy_tree("extensions/skyportal/", "skyportal/")

    # add grandma-specific dependencies for SP
    # js
    with open("extensions/skyportal/package.grandma.json", "r") as f:
        grandma_pkg = json.load(f)
    with open("skyportal/package.json", "r") as f:
        skyportal_pkg = json.load(f)

    skyportal_pkg["dependencies"] = {
        **skyportal_pkg["dependencies"],
        **grandma_pkg["dependencies"],
    }
    with open("skyportal/package.json", "w") as f:
        json.dump(skyportal_pkg, f, indent=2)

    # python
    with open(".requirements/ext.txt", "r") as f:
        ext_req = f.readlines()
    with open("skyportal/requirements.txt", "r") as f:
        skyportal_req = f.readlines()
    with open("skyportal/requirements.txt", "w") as f:
        f.writelines(skyportal_req)
        for line in ext_req:
            if line not in skyportal_req:
                f.write(line)