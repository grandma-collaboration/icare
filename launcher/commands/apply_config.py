import subprocess
from pathlib import Path
import yaml


class MyDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1 or len(self.indents) == 2:
            super().write_line_break()


def apply_config():
    print("applying config")
    try:
        file = "grandma.yaml"
        if not Path(file).exists():
            file = "grandma.yaml.defaults"

        with open(file, "r") as stream:
            try:
                grandma_config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        with open("patched_skyportal/config.yaml.defaults", "r") as stream:
            try:
                skyportal_config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        # replace keys of skyportal_config with values of grandma_config
        for key in grandma_config:
            print("key", key)
            if key in skyportal_config:
                for subkey in grandma_config[key]:
                    print("subkey", subkey)
                    print(grandma_config[key][subkey])
                    skyportal_config[key][subkey] = grandma_config[key][subkey]
            else:
                skyportal_config[key] = grandma_config[key]

            # # if key is a list, replace values
            # else:
            # skyportal_config[key] = grandma_config[key]
        # write config.yaml to skyportal-fink-client
        with open("patched_skyportal/config.yaml.defaults", "w") as stream:
            try:
                yaml.dump(skyportal_config, stream, Dumper=MyDumper, sort_keys=False)
            except yaml.YAMLError as exc:
                print(exc)
    except Exception as e:
        print(e)
        print("Failed to apply grandma patches to the config")
