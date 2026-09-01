<h1 align="center">
  <br>
  <img
    src="docs/skyportal_logo.png"
    alt="ICARE Logo"
    width="100px"
  />
  <br>
  ICARE
  <br>
</h1>

<h2 align="center">
Interface and Communication for Addicts of the Rapid follow-up in multi-messenger Era
</h2>

[![Documentation Status](https://readthedocs.org/projects/grandma-skyportal/badge/?version=latest)](https://grandma-skyportal.readthedocs.io)
[![pre-commit](https://github.com/grandma-collaboration/icare/actions/workflows/pre-commit-linting.yml/badge.svg)](https://github.com/grandma-collaboration/icare/actions/workflows/pre-commit-linting.yml)
[![tests](https://github.com/grandma-collaboration/icare/actions/workflows/test_icare_extensions.yaml/badge.svg)](https://github.com/grandma-collaboration/icare/actions/workflows/test_icare_extensions.yaml)

ICARE is a custom instance of [SkyPortal](https://skyportal.io) ([docs](https://skyportal.io/docs/)) tailored for the coordination and follow-up of multi-messenger astronomical events. Originally developed in 2020 for the [GRANDMA](https://grandma.ijclab.in2p3.fr/) collaboration, it is now open to the broader European astronomical community thanks to [ACME](https://www.acme-astro.eu/) funding.

## Links

| | |
|---|---|
| **ICARE Service** | https://skyportal-icare.ijclab.in2p3.fr |
| **Documentation** | https://grandma-skyportal.readthedocs.io |
| **GRANDMA** | https://grandma.ijclab.in2p3.fr |
| **ACME** | https://www.acme-astro.eu |

## Quick install

```bash
git clone https://github.com/grandma-collaboration/icare
cd icare
git submodule update --init --recursive
uv sync
cp icare.yaml.defaults icare.yaml
./icare.sh run --clear --init
```

See the [Developer Guide](https://grandma-skyportal.readthedocs.io/dev_guide/installation/) for full installation instructions.

## Contact

- Camille Douzet — camille.douzet@ijclab.in2p3.fr
- Sarah Antier — antier@ijclab.in2p3.fr

## License

Copyright (C) 2020-2026, the GRANDMA collaboration team. All rights reserved.
