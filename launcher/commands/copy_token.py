import pathlib
import subprocess
import yaml


def copy_token():
    try:
        # open .tokens.yaml file from patched_skyportal
        with open("patched_skyportal/.tokens.yaml", "r") as stream:
            try:
                skyportal_token = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        # open config.yaml of skyportal-fink-client
        with open("extensions/skyportal-fink-client/config.yaml", "r") as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        # update config.yaml with tokens
        config["skyportal_token"] = skyportal_token["INITIAL_ADMIN"]
        # write config.yaml to skyportal-fink-client
        with open("extensions/skyportal-fink-client/config.yaml", "w") as stream:
            try:
                yaml.dump(config, stream)
            except yaml.YAMLError as exc:
                print(exc)
    except Exception as e:
        print(e)
        print("\nFailed to copy token")
