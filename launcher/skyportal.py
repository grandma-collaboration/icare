import json
import tomllib
import tomli_w
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
    with open("skyportal/package.json", "r") as f:
        skyportal_pkg = json.load(f)

    skyportal_pkg["dependencies"] = {
        **skyportal_pkg["dependencies"],
        **icare_pkg["dependencies"],
    }
    if "engines" in icare_pkg:
        skyportal_pkg["engines"] = {
            **skyportal_pkg.get("engines", {}),
            **icare_pkg["engines"],
        }
    with open(destination + "package.json", "w") as f:
        json.dump(skyportal_pkg, f, indent=2)

    # python
    with open("pyproject.toml", "rb") as f:
        icare_pyproject = tomllib.load(f)
    with open("skyportal/pyproject.toml", "rb") as f:
        skyportal_data = tomllib.load(f)

    ext_dependencies = icare_pyproject["dependency-groups"]["ext"]
    skyportal_data["project"]["dependencies"] = list(
        set(skyportal_data["project"]["dependencies"] + ext_dependencies)
    )
    with open(destination + "pyproject.toml", "wb") as f:
        tomli_w.dump(skyportal_data, f)

    apply_config()
