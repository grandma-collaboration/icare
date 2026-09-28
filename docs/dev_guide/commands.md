# Commands

## System Commands

Now that we've explored the architecture of icare, let's see how do we actually add the extensions to SkyPortal, update Skyportal and said extensions, and much more.

In icare, you'll find a launcher directory, containing different commands. The launcher directory follows the same patterns established in Fritz, for consistency sake.

Here are the different commands, all prefixed with `./icare.sh`:

| Command | Description |
|---|---|
| `run` | Main entry point. Builds and starts the app. Accepts flags: `--init` (initialize DB), `--clear` (drop and recreate DB), `--do_update` (pull and update SkyPortal), `--update_prod` (production update with migration stamping), `--production` (build with rspack for production) |
| `build` | Copies `skyportal/` to `patched_skyportal/` and applies the `extensions/skyportal/` overlay. Called automatically by `run` |
| `update` | Pulls the latest SkyPortal from the remote and updates submodules recursively |
| `diff` | Shows which SkyPortal files have changed upstream and overlap with files in `extensions/skyportal/`. Used to detect merge conflicts before updating |
| `clear` | Drops and recreates the SkyPortal database (`make db_clear`) |
| `apply_config` | Merges `icare.yaml` on top of SkyPortal's default config and writes the result to `patched_skyportal/config.yaml.defaults` |
| `copy_token` | Copies the SkyPortal admin token from `patched_skyportal/.tokens.yaml` into the skyportal-fink-client `config.yaml` so Fink can authenticate |
| `set_user_role` | Sets or lists user roles. Usage: `./icare.sh set_user_role --username=<user> --role=<role>` or `--list` |
| `load_grandma_data` | Loads GRANDMA telescope and instrument data into SkyPortal (`make load_grandma_data`) |

For example: `./icare.sh run --clear --init` drops the database, recreates it, and starts the app.

### Configuration: icare.yaml

Before running the app, you need to create an `icare.yaml` file at the root of the repository. Copy the defaults as a starting point:

```
cp icare.yaml.defaults icare.yaml
```

The key fields to configure before starting are:

| Field | Description |
|---|---|
| `server.host` | Public hostname or IP of the server |
| `server.protocol` | `http` for dev, `https` for production |
| `server.port` | App port (default: 5000) |
| `server.auth.debug_login` | Set to `True` for local dev (no real auth), `False` in production |
| `server.auth.backends[].key` | IAM OAuth2 client key |
| `server.auth.backends[].secret` | IAM OAuth2 client secret |
| `fink.fink_username` | Fink broker username |
| `fink.fink_password` | Fink broker password |
| `fink.fink_group_id` | Kafka consumer group ID |
| `fink.fink_servers` | Kafka broker addresses |

The `apply_config` command merges your `icare.yaml` into SkyPortal's config. It is called automatically when you run `./icare.sh run`.

### Starting the app for the first time

First, you need to install the dependencies required to use the commands mentioned in the previous section. Install them from `pyproject.toml` using `pip` or `uv`:

```
pip install -e .
```
or
```
uv sync
```

To run the app for the first time, we can use the `run` command as such:
```
./icare.sh run --clear --init
```

This will install all the required dependencies, clear the database if it exists, create the database, and run the app.

### Updating SkyPortal and the extensions (development)

To update the version of SkyPortal that is pinned in the repo, first create a new branch (if you are working on a fork, which is preferable, don't forget to merge the changes coming from upstream in your main branch first) and use
```
git checkout <new-branch-name>
```
to switch to the new branch. Then, to be sure that the submodules are all at the right version pinned to the branch (they might be on an older or newer version if you made some modifications earlier, even on another branch. Submodules usually don't automatically checkout to the pinned version after you checkout to a branch), use:
```
git pull
git submodule update --init --recursive
```

Last but not least, remove the `patched_skyportal` and `previous_skyportal` directories if they exist:
```
sudo rm -rf patched_skyportal
sudo rm -rf previous_skyportal
```

Now, you can use the `do_update` command as such:
```
./icare.sh run --do_update
```

This will update the version of SkyPortal that is pinned in the app. When doing so, we are basically running a `git diff` to see which files have been modified. If some of those files are also the files we have copied and modified in the extensions folder, we need to merge new changes in the extensions folder too. If we don't do this, when replacing skyportal's files by the files in the extensions folder, we'll lose new changes. And besides from missing on new features, it is very likely to break the app. Which is why, when we detect that some changes coming from skyportal are made on same files we have in the extensions folder, we give the user 3 choices:

- **Option 1 — Fix conflicts first (recommended)**: the launcher exits without starting. Go to `extensions/skyportal/` and manually update the conflicting files to incorporate the upstream changes. Use `git diff skyportal/path/to/file` (from the repo root) to see what changed in SkyPortal. Edit the corresponding file in `extensions/skyportal/path/to/file`, then rerun `./icare.sh run --do_update`.
- **Option 2 — Force update**: runs with the upstream changes, overwriting your extension files. Will likely break the app.
- **Option 3 — Cancel update**: keeps the current SkyPortal version and starts normally.

After resolving conflicts and verifying the app starts correctly, rerun the app with:
```
./icare.sh run
```

If everything seems to be working fine, commit your changes to your branch (don't forget to `git add` all the modified files, including skyportal itself using `git add skyportal`), open a PR and wait for the GitHUb actions to finish running. If everything is green, ask for a review and merge the changes to the main branch **ONLY** when all reviewers approved your changes.

### Updating icare (production)

The commands mentioned above are meant to update the version of skyportal that is pinned in the repo, along with the extensions. Once that is done, the developer has to commit new changes to the branch that is used in production.

On your local environment:
```
# 1. Update your repo
git pull
git submodule update --init --recursive
./icare.sh run --do_update

# 2. Push to icare the last modifications
git add skyportal
git commit -m "Bump to skyportal <commit_hash>"
git push
```

Then, on the production machine :

1. Reboot the machine to stop icare and connect you as root (`sudo su`)

2. Go to `/htdocs/skyportal/deployment/grandma_skyportal/`

3. Update to the last version of icare and its submodule :

```
git pull
git submodule update --init --recursive
```

4. Run this command:
```
./icare_prod.sh run --update_prod
```

It will stamp the current database state using alembic. This is done so that when updating the app, if the models of some tables has been modified, or if new tables have been added, alembic is able to apply the changes to the database. Then skyportal will be updated, and changes from the extensions directory will be applied.
When the app runs, as the database's state has been stamped, a migration server should start automatically and update the database.

5. If everything is ok in the last step, run the following command :
```
./icare_prod.sh run --production
```

#### Troubleshooting

##### `./icare_prod.sh run --update_prod` failed

Make sure that postgres and nginx are running and restart them if their process are dead.
```
systemctl status postgresql
systemctl status nginx
```
If needed, run :
```
systemctl restart postgresql
systemctl restart nginx
```

##### Error 502 after an icare update

If after a icare update you go to icare portal and you have an error message with a 502 error code, then perform the following steps:

1. Press Ctrl Z and run `bg` to put icare in the background without stopping the process.

2. Run `setenforce 0` to set the enforcement mode of the SELinux to permissive.

### Loading data from the grandma_data repo

To load data from the grandma_data repo, we can use the `load_grandma_data` command as such:
```
./icare.sh load_grandma_data
```

### Set user roles

In SkyPortal, there is a script that an admin can use to set user roles manually from the terminal in production for example.
Here, we just added a command to call that script with the same syntax as other command from grandma_skyportal.
You can use it as such:
```
./icare.sh set_user_role --user=<user_name> --role=<role_with_underscores_instead_of_spaces>
```

To see the list of user and roles, run:
```
./icare.sh set_user_role --list
```

## Access the Production VM (at IJCLAB)

We deployed icare on a VM at IJCLAB/CNRS, which is accessible remotely via SSH. However, for security reasons, we don't want to expose an SSH connection to the public internet. Which is why you will need an IJCLAB account, so you can first connect to a public VM of IJCLAB, and then connect to the private VM dedicated to icare.

- Connect to the public VM of IJCLAB:
```
ssh <your_user_name>@lx3.lal.in2p3.fr
```

- Connect to the private VM running icare (to be able to do so, you first need to ask someone at the "Service d'exploitation", or someone that already has access to the VM to add your SSH key to the grandmadmin user):
```
ssh grandmadmin@grandma-v2.ijclab.in2p3.fr
```

Now that you are connected, you can use the following commands:

- to elevate your privileges, run
```
sudo -i
```

- activate your virtual environment with all the dependencies needed to run the app

- then go to the `icare` folder and run the following command:
```
cd /pdisk/htdocs/skyportal/deployment/icare
```

- to run the app, run
```
./icare.sh run
```

We advise you to open a second terminal, go to the `patched_skyportal` folder and run:
```
make log
```
so you can see the logs of the app in real time, and verify that everything is running correctly.

When the app is fully started, and if you haven't encountered any bugs/errors, you can use the following command to make the app available to the public:
```
setenforce 0
```

!!! tip
    If any command fails, make sure that every time you open a new terminal you reconnect via SSH and elevate your privileges with `sudo -i`.

For now, starting the app is not done automatically when the VM reboots. You can do it manually by running the commands mentioned above.

After starting the app remotely from your computer, you will very likely close the SSH connection, effectively closing the terminal in which you ran the app. This is fine, and won't close the app. However, if you want to stop the app, you won't be able to go back to that terminal to close it using the `Ctrl+C` key as you would normally do. Instead, you need to reboot the VM, connect to it, and repeat the steps detailed above.

If you have trouble starting or accessing the app, maybe that Nginx or PostgreSQL did not start correctly. First stop the app, and use `systemctl` to see the status of a service (they should be named `nginx` and `postgresql-17`):
```
systemctl status <service_name>
```

If it is not displayed as active and loaded, try restarting it using:
```
systemctl restart <service_name>
```

Verify their status once more, and if everything seems to be working you should be able to start the app again.
