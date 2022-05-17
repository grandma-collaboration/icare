from baselayer.app.config import load_config
from baselayer.app.models import init_db
from skyportal.model_util import make_super_user

cfg = load_config()
init_db(**cfg["database"])


def elevate(
    username: str,
):
    if username:
        try:
            user = make_super_user(username)
            print(f"Elevated {username} to superuser")
        except Exception as e:
            print(f"Failed to elevate {username} to superuser: {e}")
            print(
                "Try again with a different username (this one probably does not exist"
            )
    else:
        print("No username provided")
