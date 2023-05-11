import shutil
import subprocess
import sys
from pathlib import Path

from launcher.commands import (build, clear, diff, load_grandma_data,
                               poll_from_fink, run, set_user_role, update)
from tools.check_environment import dependencies_ok
from tools.status import status

sys.path.insert(0, "skyportal")

required_services = [["postgresql", "postgresql-14"], ["nginx"]]


def check_services():
    # using systemctl to check if services are running
    print("Checking that necessary services are running:")
    missing_services = []
    for services in required_services:
        with status(services[0]):
            try:
                if not any(
                    # check that the output of systemctl is-active is "active"
                    subprocess.run(
                        ["systemctl", "is-active", service],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                    )
                    .stdout.decode("utf-8")
                    .strip()
                    == "active"
                    for service in services
                ):
                    raise RuntimeError(f"Service {services} is not running")
            except Exception as e:
                missing_services.append(services[0])

    print("-" * 20)

    if len(missing_services) == 0:
        return True
    else:
        print(
            f'The following systemctl services are not running: {", ".join(missing_services)}'
        )
        return False


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
        # with status("Initializing submodules"):
        #     initialize_submodules()

        env_ok = dependencies_ok()
        if not env_ok:
            print("\nHalting because of unsatisfied dependencies.")
            sys.exit(-1)
        if "--skip_services_check" in sys.argv:
            print("\nSkipping services check")
        else:
            if not check_services():
                print("Halting because some services are not running")
                sys.exit(-1)

    # if the patched_skyportal folder exists, we need to remove the node_modules and package-lock.json
    # files to avoid conflicts with the skyportal package
    # if Path("patched_skyportal").exists():
    #     if Path("patched_skyportal", "node_modules").exists():
    #         shutil.rmtree("patched_skyportal", "node_modules")
    #     if Path("patched_skyportal", "package-lock.json").exists():
    #         Path("patched_skyportal", "package-lock.json").unlink()

    # if previous_skyportal directory exists, we need to remove the entire directory and subdirectories
    if Path("previous_skyportal").exists():
        shutil.rmtree("previous_skyportal")

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
