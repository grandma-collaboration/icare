import subprocess
import os
import fire

os.environ["PYTHONPATH"] = "."


@fire.decorators.SetParseFn(str)
def set_user_role(
    list: bool = False,
    username: str = None,
    role: str = None,
):
    command = ["python", "tools/set_user_role.py"]

    if list:
        command.append("--list")
    if username:
        command.append(f"--username={username}")
    if role:
        command.append(f"--role={role.replace('_', ' ')}")

    print(command)

    p = subprocess.run(
        command,
        cwd="patched_skyportal",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(p.stdout.decode("utf-8"))
