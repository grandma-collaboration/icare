import subprocess

from launcher.commands.build import build
from launcher.config import check_config_exists


def load_grandma_data():
    """🚀 Load Grandma data in SkyPortal"""
    cmd = subprocess.Popen(["make", "load_grandma_data"], cwd="patched_skyportal")
    cmd.communicate()
