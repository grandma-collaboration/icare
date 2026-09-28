# Installation

## System Dependencies

### Dependencies

SkyPortal requires the following software to be installed.  We show
how to install them on MacOS and Debian-based systems below.

- Python (v>=3.12, <3.13)
- Supervisor (v>=3.0b2)
- NGINX (v>=1.7)
- PostgreSQL (v>=17)
- Node.JS (v>=24) / bun (v>=1.3.14)

When installing SkyPortal on Debian-based systems, 2 additional packages are required to be able to install pycurl later on:

- libcurl4-gnutls-dev
- libgnutls28-dev

### Source download, Python environment

Clone the [ICARE repository](https://github.com/grandma-collaboration/icare) and install dependencies.

With `uv` (recommended):
```
git clone https://github.com/grandma-collaboration/icare
cd icare/
uv sync
```

With `pip`:
```
git clone https://github.com/grandma-collaboration/icare
cd icare/
pip install -e .
```

If you are using Windows Subsystem for Linux (WSL) be sure you clone the repository onto a location on the virtual machine, not the mounted Windows drive. Additionally, we recommend that you use WSL 2, and not WSL 1, in order to avoid complications in interfacing with the Linux image's `localhost` network.

### Installation: Debian-based Linux and WSL

1. Install nginx, python and bun

Run the following commands to install the dependencies:
```
sudo apt install nginx supervisor libpq-dev python3-pip libcurl4-gnutls-dev libgnutls28-dev
curl -fsSL https://bun.sh/install | bash
```

2. Installing PostgreSQL

The version of PostgreSQL that is shipped with most Debian-based Linux distributions is not up to date. If you already have an older version installed, you first need to remove it:
```
sudo systemctl stop postgresql
sudo pg_dropcluster --stop <older_version> main
sudo apt-get --purge remove postgresql postgresql-*
sudo rm -r /var/lib/postgresql/<older_version>
sudo rm -r /etc/postgresql/<older_version>
```
Here are the steps to install version 17:
```
sudo apt update && sudo apt upgrade
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt -y update
sudo apt -y install postgresql-17
```

To verify if the installation was successful, run the following command:
```
systemctl status postgresql
```
It should be displayed as "Loaded" and "Active".

You can also run:
```
sudo -u postgres psql -c "SELECT version();"
```
to verify that the version is the right one.

Sometimes, if you removed an older version of postgresql before installing a newer one, a cluster won't be automaticcally created for the newer version. You can create a cluster manually by running the following command:
```
sudo pg_createcluster <new_version> main --start
sudo systemctl restart postgresql
```

Then, run the same commands mentionned above to verify that the installation was successful.

3. Verify node.js and bun

Bun was already installed in step 1. Open a new terminal and run:
```
node --version
bun --version
```
to verify the installations. Node.js must be version 24 or higher.

2. Configure your database permissions.

In `pg_hba.conf` (typically located in
`/etc/postgresql/<postgres-version>/main`), insert the following lines
*before* any other `host` lines:

```
host skyportal skyportal 127.0.0.1/32 trust
host skyportal_test skyportal 127.0.0.1/32 trust
host all postgres 127.0.0.1/32 trust
```

If you are deploying SkyPortal using IPv6 rather than IPv4, you should add the following lines instead:

```
host skyportal skyportal ::1/128 trust
host skyportal_test skyportal ::1/128 trust
host all postgres ::1/128 trust
```

In some PostgreSQL installations, the default TCP port may be different from the 5432 value assumed in our default configuration file values. To remedy this, you can either edit your config.yaml file to reflect your system's PostgreSQL default port, or update your system-wide config to use port 5432 by editing /etc/postgresql/12/main/postgresql.conf (replace "12" with your installed version number) and changing the line `port = XXXX` (where "XXXX" is whatever the system default was) to `port = 5432`.

Restart PostgreSQL:

```
sudo service postgresql restart
```

3. To run the frontend test suite locally, you'll need geckodriver and Firefox:

```
sudo apt install firefox-geckodriver
```

Set `FRONTEND_TEST_HEADLESS=1` to run headless (as CI does):
```
FRONTEND_TEST_HEADLESS=1 cd patched_skyportal && python baselayer/tools/test_frontend.py skyportal/tests/frontend/test_patch_grandma.py
```
