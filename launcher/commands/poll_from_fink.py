import pathlib
import subprocess
import yaml
from launcher.commands.copy_token import copy_token


def poll_from_fink(
    testing: bool = False,
):
    # open config.yaml of skyportal-fink-client
    with open("extensions/skyportal-fink-client/config.yaml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    if testing:
        # update config.yaml with tokens
        config["testing"] = True
    else:
        config["testing"] = False
    # write config.yaml to skyportal-fink-client
    print(config)
    with open("extensions/skyportal-fink-client/config.yaml", "w") as stream:
        try:
            yaml.dump(config, stream)
        except yaml.YAMLError as exc:
            print(exc)

    copy_token()

    cmd = subprocess.Popen(
        ["make", "poll_alerts"], cwd="extensions/skyportal-fink-client"
    )
    cmd.communicate()
