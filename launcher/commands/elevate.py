import pathlib
import subprocess

def elevate(
    username: str,
):
    try:
        import patched_skyportal.skyportal.elevate as elevate
        elevate.elevate(username)
    except ImportError:
        print("No patched_skyportal found, initial build required")
        pass
    