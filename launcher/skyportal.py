import json
from distutils.dir_util import copy_tree

from .commands.apply_config import apply_config

version_operators = ["==", ">=", "<=", ">", "<", "!="]


def dep_version(line):
    """Return the version and a dependency from a requirements line."""
    if any([op in line for op in version_operators]):
        op = [op for op in version_operators if op in line][0]
        dep = line.split(op)[0]
        version = line.split(op)[1]
    else:
        op = None
        dep = line
        version = None
    return dep, version


def patch(source="extensions/skyportal/", destination="patched_skyportal/"):
    """Make icare-specific file modifications to SkyPortal."""
    print("\n Applying icare-specific patches to SkyPortal")

    # add icare-specific SP extensions
    copy_tree(source, destination)

    # add icare-specific dependencies for SP
    # js
    with open(source + "package.icare.json", "r") as f:
        icare_pkg = json.load(f)
    with open("skyportal/" + "package.json", "r") as f:
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
    with open("skyportal/" + "requirements.txt", "r") as f:
        skyportal_req = f.readlines()
    with open(destination + "requirements.txt", "w") as f:
        for line in ext_req:
            dep, _ = dep_version(line)
            if dep not in [dep_version(r)[0] for r in skyportal_req]:
                skyportal_req.append(line)
            else:
                # replacing existing dependency
                for i, r in enumerate(skyportal_req):
                    if dep_version(r)[0] == dep:
                        print(f"Replacing skyportal: {r}, with icare: {line}")
                        skyportal_req[i] = line
                        break
        f.writelines(skyportal_req)

    apply_config()
