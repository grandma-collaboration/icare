import subprocess

def clear():
    cmd = subprocess.Popen(
        ["make", "db_clear"],
        cwd="patched_skyportal"
    )
    cmd.communicate()
    print("Cleared database")