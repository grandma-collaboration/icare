import time
import os

from baselayer.log import make_log
from baselayer.app.models import init_db
from baselayer.app.env import load_env

import importlib

skyportalfinkclient = importlib.import_module(
    "skyportal-fink-client.skyportal_fink_client.skyportal_fink_client"
)
files = importlib.import_module(
    "skyportal-fink-client.skyportal_fink_client.utils.files"
)
skyportalapi = importlib.import_module(
    "skyportal-fink-client.skyportal_fink_client.utils.skyportal_api"
)

from skyportal.models import DBSession, Instrument

env, cfg = load_env()

init_db(**cfg["database"])
log = make_log("fink")


def skyportal_fink_client():
    instruments = ["CFH12k", "ZTF"]
    skyportal_url = "http://localhost:5000"
    started = False
    skyportal_token = None
    skyportal_instruments = {}
    fink_config = cfg["fink"]
    if any(
        fink_config[key] is None and key not in ["fink_password", "skyportal_token"]
        for key in fink_config
    ):
        log("Fink configuration is incomplete. Please check your config file.")
        return
    while not started or not any(
        [instrument in skyportal_instruments.keys() for instrument in instruments]
    ):
        # open yaml config file
        try:
            token = files.yaml_to_dict(
                os.path.abspath(os.path.join(os.path.dirname(__file__)))
                + "/../../.tokens.yaml"
            )
            skyportal_token = token["INITIAL_ADMIN"]
        except Exception as e:
            log("Can't retrieve skyportal token")
            skyportal_token = ""
            time.sleep(15)
            # get all instruments from skyportalapi

        status, skyportal_instruments = skyportalapi.get_all_instruments(
            skyportal_url, skyportal_token
        )
        if status is not 200 and status is not 400:
            log("App not started yet. Waiting for skyportal to start...")
            time.sleep(15)
        elif status is 400:
            started = True
            fink_config["skyportal_token"] = skyportal_token
            log(
                "Can't retrieve instruments from skyportal using initial admin token. Retrying..."
            )
            time.sleep(15)
        elif status is 200 and not any(
            [instrument in skyportal_instruments.keys() for instrument in instruments]
        ):
            started = True
            fink_config["skyportal_token"] = skyportal_token
            log(f"Waiting for instruments to be added to skyportal")
            time.sleep(15)
        else:
            started = True
            fink_config["skyportal_token"] = skyportal_token
            # set the skyportal token in skyportal fink client config file
            log("App started and the right instruments have been added to skyportal")

    skyportalfinkclient.poll_alerts(**fink_config, log=log)


if __name__ == "__main__":
    skyportal_fink_client()
