import pathlib
import subprocess

from skyportal.model_util import make_super_user

def elevate(
    username: str,
):
    if username:
        make_super_user(username)
        print("Elevated user {} to superuser".format(username))
    else:
        print("No username provided")
    