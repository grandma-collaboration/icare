from pathlib import Path
import subprocess
import sys

from launcher.commands import (
    build,
    run,
    update,
    diff,
    clear,
    set_user_role,
    poll_from_fink,
    load_grandma_data,
)

from tools.check_environment import dependencies_ok
from tools.status import status

sys.path.insert(0, "skyportal")


def initialize_submodules():
    """Initialize submodules if either submodule directory is empty"""
    if len(list(Path("skyportal").glob("*"))) == 0:
        p = subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print(p.stdout.decode("utf-8"))
    if len(list(Path("extensions/services/fink/skyportal-fink-client").glob("*"))) == 0:
        p = subprocess.run(
            ["git", "submodule", "update", "--init"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print(p.stdout.decode("utf-8"))
        if p.returncode != 0:
            raise RuntimeError("Failed to initialize icare's submodules")


if __name__ == "__main__":
    try:
        import fire
    except ImportError:
        print("\nThis tool depends on `fire`.  Please install it using:")
        print("\n  pip install fire")
        sys.exit(-1)

    # Monkey-patch away fire's paging
    fire.core.Display = lambda lines, out: print(*lines, file=out)

    # Prevent fire from printing annoying extra debugging information
    # when the user specifies `--help` instead of `-- --help`
    if sys.argv[-1] == "--help" and sys.argv[-2] != "":
        sys.argv.insert(-1, "--")

    # No need to install whole environment if the user just
    # wants/needs some help
    if (
        sys.argv[-1] != "--help"
        and len(sys.argv) != 1
        and "diff" not in sys.argv
        and "set_user_role" not in sys.argv
    ):
        # check environment
        with status("Initializing submodules"):
            initialize_submodules()

        env_ok = dependencies_ok()
        if not env_ok:
            print("\nHalting because of unsatisfied dependencies.")
            sys.exit(-1)

    fire.Fire(
        {
            "build": build,
            "run": run,
            "update": update,
            "diff": diff,
            "clear": clear,
            "set_user_role": set_user_role,
            "poll_from_fink": poll_from_fink,
            "load_grandma_data": load_grandma_data,
        },
        name="icare",
    )
