__all__ = [
    "check_config_exists",
    "check_config",
]


from pathlib import Path
import subprocess

import yaml


def check_config_exists(cfg="icare.defaults.yaml", yes=False):
    c = cfg.replace(".defaults", "")
    if not Path(c).exists():
        cd = (
            input(
                f"{c} does not exist, do you want to use default settings from {cfg}? [y/N] "
            )
            if not yes
            else "y"
        )
        if cd.lower() == "y":
            subprocess.run(["cp", f"{cfg}", f"{c}"], check=True)
        else:
            raise IOError(f"{c} does not exist, aborting")


def check_config(cfg="icare.defaults.yaml", yes=False):
    """
    Check if config exists, generate a K token for SP, adjust cfg and distribute to K and SP
    """
    c = cfg.replace(".defaults", "")
    check_config_exists(cfg=cfg, yes=yes)
