import subprocess
import json
from distutils.dir_util import copy_tree
from .commands.apply_config import apply_config


def patch(source="extensions/skyportal/", destination="patched_skyportal/"):
    """Make grandma-specific file modifications to SkyPortal."""
    print("\n Applying grandma-specific patches to SkyPortal")

    # add grandma-specific SP extensions
    copy_tree(source, destination)

    # add grandma-specific dependencies for SP
    # js
    with open(source + "package.grandma.json", "r") as f:
        grandma_pkg = json.load(f)
    with open(destination + "package.json", "r") as f:
        skyportal_pkg = json.load(f)

    skyportal_pkg["dependencies"] = {
        **skyportal_pkg["dependencies"],
        **grandma_pkg["dependencies"],
    }
    with open(destination + "package.json", "w") as f:
        json.dump(skyportal_pkg, f, indent=2)

    # python
    with open(".requirements/ext.txt", "r") as f:
        ext_req = f.readlines()
    with open(
        source + "services/fink/skyportal-fink-client/requirements.txt", "r"
    ) as f:
        fink_req = f.readlines()
    with open(destination + "requirements.txt", "r") as f:
        skyportal_req = f.readlines()
    with open(destination + "requirements.txt", "w") as f:
        f.writelines(skyportal_req)
        for line in ext_req:
            if line not in skyportal_req:
                f.write(line)
        for line in fink_req:
            if line not in skyportal_req:
                f.write(line)

    apply_config()
