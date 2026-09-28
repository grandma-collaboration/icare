# ICARE

**Interface and Communication for Addicts of the Rapid follow-up in multi-messenger Era**

## What is ICARE?

ICARE is a platform designed for the coordination and follow-up of multi-messenger astronomical events: gravitational wave alerts, gamma-ray bursts, and other transient phenomena requiring rapid telescope scheduling and data sharing.

Development started in 2020 as a custom layer built on top of [SkyPortal](https://skyportal.io/), originally created for the [GRANDMA](https://grandma.ijclab.in2p3.fr/) collaboration. GRANDMA (Global Rapid Advanced Network Devoted to the Multi-messenger Addicts) is an international network of telescopes founded in 2018 by Sarah Antier that coordinates observations of transient events, in particular kilonovae associated with gravitational wave sources detected by LIGO/Virgo/KAGRA.

In 2025, thanks to the [ACME](https://www.acme-astro.eu/) funding, ICARE opened its doors to the broader European astronomical community, becoming a shared infrastructure accessible to any research group interested in multi-messenger follow-up.

## How does it work?

ICARE is a custom frontend and backend layer added on top of [SkyPortal](https://skyportal.io/), and provides 2 extensions:

- [SkyPortal-Fink-Client](https://github.com/skyportal-contrib/skyportal-fink-client): a tool to pull alerts from the Fink broker and add them to SkyPortal.
- [GRANDMA data](https://github.com/grandma-collaboration/grandma_data): a set of data needed by GRANDMA to populate SkyPortal's database, such as telescopes and instruments.

## Authentication

##### Full Account Creation Tutorial: [User Guide](./user_guide/index.md)

Users can login to ICARE using either their Slack account (for GRANDMA people), ORCID or eduGAIN account. The service used for
authentication is called IAM. One benefit of this service is that you will be able to use your
standard account, without the need to remember a username and a password specific to ICARE.
Also you will be able to use any of the authentication methods proposed and still remain the same user in ICARE.

Your IAM account will be automatically created the first time you connect to
[ICARE](https://skyportal-icare.ijclab.in2p3.fr).

!!! warning
    Do not try to connect to ICARE until your account is verified. If you already did, delete your browser cache/cookies before logging in again.

## First steps after logging in

First, head to the `Groups` page. There, you can request to be added to the groups you are interested in.
Example: if you are a member of GRANDMA, you can ask to be added to the `GRANDMA` group. If you are interested
in seeing alerts from Fink, you can ask to be added to the `Fink` group.

An administrator of the group will be notified of your request. After accepting it, you will receive
a notification (bell icon, top right corner) confirming you have been added.

Now, you can explore the rest of the platform.

## User permissions and roles

Users can have different roles that come with a predetermined set of permissions. A user can also be granted individual permissions without a specific role.

By default, new users receive the `Full user` role, which gives access to most features: creating sources, groups, leaving comments, and more. Some actions require additional permissions that an administrator can grant. If you need access to a specific feature, reach out to an administrator.

## User Guide

You will find a more in depth guide to use ICARE on the [User Guide](./user_guide/index.md) page.

## Contact

For any question about ICARE, you can reach out to:

- **Camille Douzet** — [camille.douzet@ijclab.in2p3.fr](mailto:camille.douzet@ijclab.in2p3.fr)
- **Sarah Antier** — [antier@ijclab.in2p3.fr](mailto:antier@ijclab.in2p3.fr)
