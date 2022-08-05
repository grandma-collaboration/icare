# Icare

## What is it ?
Icare is a custom "layer" of both frontend and backend, added on top of [SkyPortal](https://skyportal.io/) to provide the features required only by Grandma.

Besides from building on top of SkyPortal, it also provides 2 extensions:

- [SkyPortal-Fink-Client](https://github.com/skyportal-contrib/skyportal-fink-client): A tool to pull alerts from Fink and add them to SkyPortal.

- [Grandma data](https://github.com/grandma-collaboration/grandma_data): a set of data needed by Grandma to populate SkyPortal's database, such as telescopes data, instruments data, etc.

## Authentication

##### Full Account Creation Tutorial: [User Guide](./user_guide/index.md)

Users can login to Icare using either their Slack account or their eduGAIN account. The service used for
authentication is called IAM. One benefit of this service is that you will be able to use your
standard account, without the need to remember a username and a password specific to Icare.
Also you will be able to use any of the authentication methods proposed and still remain the same user in Icare.

Your IAM account will be automatically created the first time you connect to
[Icare](https://grandma-v2.ijclab.in2p3.fr/) but we recommend that you follow
the steps below to create it before attempting to connect to Icare.

**Important : Do not try to connect to SkyPortal until your account is verified. If you still did that,
you will need to delete your cache/cookies before logging in.**

## How to create and configure your IAM account.

It is recommended to create your IAM account before connecting to Icare by
connecting directly to the [IAM service](https://iam-grandma.ijclab.in2p3.fr/login).
You will have to enter some information required to create your account. Note that the that
the firstname, lastname, email you enter will be used to initialize your Skyportal
profile. The email you specifiy don't need to be the same as the email associated with the
Slack or eduGAIN account you used to authenticate and will be used as your Icare
identifier (username).

**Note: one of the mandatory information to create your IAM account is the `Note` field: we request you to put your
affiliation in this note, as well as other information you may find useful.**

Once your account has been created and verified, you can login again to
[Icare](https://grandma-v2.ijclab.in2p3.fr/) using your IAM account
A Icare username will be automatically created. You can edit it your profile information
by clicking on the button on the top-right corner of the Icare window.

If you want to be able to authenticate using several methods, once your IAM account has been
created and validated, connect again to the [IAM service](https://iam-grandma.ijclab.in2p3.fr/login),
use the same authentication method as for the account creation (or any that you already configured)
and click on button `Link external account`. Then choose the appropriate method and enter your
credentials. If you are familiar with certificates, you can also configure a certificate that
you can use to authenticate using the `Link certificate` button.

## First steps to follow after login in for the first time

First, you will need to head to the `Groups` page. There, you can request to be added to the groups you are interested in.
Exemple: You are a member of GRANDMA, you can ask to be added to the group `GRANDMA`. You are also interested
in seeing alerts from Fink, you can ask to be added to the group `Fink`.

An administrator of the group will be notified of your request. After accepting it, you will receive
a notification (you can see it on the top right hand corner of the screen, it is a bell icon) to tell
you that you have been added to the group.

Now, you can explore the rest of the platform.

## User permissions and roles

As a new user of SkyPortal, you won't be able to do much at first. Users can have different roles,
that come with a predeterminated set of permissions. A user can also be granted a permission without a specific role.
To use certain (most) features of the platform, you will need certain permissions.
Exemple: You can see the list of telescopes, but you can't add a new one. You can see the shifts, but you can't add or join one.
To access those different features, administrators of the platform can provide it to you. You can ask
them, but they should take care of it for every user without having to ask them. If you need additional
permissions (like the permission to add a source, ...), you can always ask them.
At first, you will be granted the `Manage shift` permission, which allows you to interact with shifts.

## User Guide

You will find a more in depth guide to use Icare on the [User Guide](./user_guide/index.md) page.
