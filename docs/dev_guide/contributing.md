# Contributing

## CI/CD

Three GitHub Actions workflows run automatically on every push and pull request:

| Workflow | Trigger | What it checks |
|---|---|---|
| `pre-commit-linting.yml` | push / PR | Runs `black` (Python formatting), YAML validity, trailing whitespace |
| `test_icare_extensions.yaml` | push / PR | Builds the patched SkyPortal, initializes the DB, and runs `skyportal/tests/frontend/test_patch_grandma.py` with headless Firefox |
| `add_labels.yaml` | PR | Automatically adds labels based on changed files |

Both checks must pass before merging to `main`. To run the linter locally before pushing:

```
pip install pre-commit
pre-commit run --all-files
```

## Deploy on a new VM

Follow these steps to deploy ICARE on a fresh AlmaLinux VM:

1. Clone the repository and initialize submodules:
```
git clone https://github.com/grandma-collaboration/icare
cd icare
git submodule update --init --recursive
```

2. Install system dependencies (nginx, supervisor, postgresql, bun: see the [Installation](installation.md) page for details).

3. Install Python dependencies:
```
uv sync
```

4. Create and configure `icare.yaml` (see [Configuration](commands.md#configuration-icareyaml)):
```
cp icare.yaml.defaults icare.yaml
# edit icare.yaml with production values
```

5. Run the app for the first time:
```
./icare.sh run --clear --init
```

If you encounter issues, check that nginx, supervisor, and postgresql are running (`systemctl status <service>`) and refer to the Common issues section below.

## Common issues

### VM full restart (production)

The production VM runs **AlmaLinux 9.6**. The OS is installed on a temporary disk while the app and database live on a permanent disk. When the VM is fully restarted (e.g. by the "Service d'exploitation"), the OS is reinstalled completely but the app on the permanent disk is preserved.

After a full restart, services that are not configured to start automatically will need to be restarted manually. Make sure nginx, supervisor, and postgresql are running before starting the app:

```
systemctl status nginx
systemctl status supervisor
systemctl status postgresql
```

If any are not active, restart them:
```
systemctl restart <service_name>
```

### Installing Python dependencies

Dependencies are managed via `pyproject.toml`. Install them with `pip install -e .` or `uv sync`.

## Contributing

### Workflow

1. Fork the repository and create a branch from `main`:
```
git checkout -b my-feature
```

2. Make your changes in `extensions/skyportal/` (never in `patched_skyportal/`).

3. Run the linter locally before pushing:
```
pip install pre-commit
pre-commit run --all-files
```

4. Push your branch and open a pull request against `main`. GitHub Actions will automatically run:
    - `pre-commit` linting (black, YAML validity, trailing whitespace)
    - The ICARE extension test suite (headless Firefox)

5. Both checks must be green before merging. Request a review and merge only after approval.

### Automatic PR labels

PRs are automatically labelled based on the files changed:

| Label | Triggered by |
|---|---|
| `config-change` | Changes to `icare.yaml.defaults` or SkyPortal config files |
| `dependencies` | Changes to dependency files |
| `documentation` | Changes to doc directories |
| `migration` | New Alembic migration files |
| `needs-migration?` | Changes to model files without a new migration |
| `skyportal_updates` | Changes to the `skyportal/` submodule |
| `workflows` | Changes to `.github/` |

### Commit message style

[Commitizen](https://commitizen-tools.github.io/commitizen/) format is encouraged. The structure is:

```
<type>: <short description>
```

Common types:

| Type | When to use |
|---|---|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change that is neither a fix nor a feature |
| `chore` | Build, deps, CI changes |

Examples:
```
feat: add leave confirmation dialog
fix: handle missing skyportal token
docs: update installation steps
chore: bump skyportal to 999a955
```

Good luck!
