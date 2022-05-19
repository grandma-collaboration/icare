# SkyPortal for Grandma

## What is it ?
SkyPortal for Grandma is a custom "layer" of both frontend and backend, added on top of [SkyPortal](https://skyportal.io/) to provide the features required only by Grandma.

Besides from building on top of SkyPortal, it also provides 2 extensions:

- [SkyPortal-Fink-Client](https://github.com/skyportal-contrib/skyportal-fink-client): A tool to pull alerts from Fink and add them to SkyPortal.

- [Grandma data](https://github.com/grandma-collaboration/grandma_data): a set of data needed by Grandma to populate SkyPortal's database, such as telescopes data, instruments data, etc.

## Authentification
For now, users can login to SkyPortal for Grandma using either their Google account or their EduGAIN account. The service used for authentification is called IAM. Essentially, you will need to create an IAM account that will be used to login to SkyPortal. But don't worry, you won't need to really create an account from A to Z and remember a password, it will be created automatically using your Google or EduGAIN account. You only need to specify your firstname, lastname, email of choice (that will be added to your skyportal profile, and can be different than the google or edugain email), as well as your affiliation (not implemented yet).


## How to create your IAM account.
To create your account, simply head to [SkyPortal for Grandma](https://grandma-v2.ijclab.in2p3.fr/) and click on the "Sign in with IAM" button.
There, you will be asked to create an IAM account using Google or EduGain. Then, you will be asked to provide firstname, lastname, email and affiliation. You will be asked to choose a firstname, lastname, email, and affiliation. After submitting it, your account will need to be verified by an administrator. Once it is verified, you will receive an email to inform you about that.

#### Important : Do not try to connect to SkyPortal until your account is verified. If you still did that, you will need to delete your cache/cookies before logging in.

Now that your account has been created and verified, you can login to [SkyPortal for Grandma](https://grandma-v2.ijclab.in2p3.fr/) using your IAM account by clicking [here](https://grandma-v2.ijclab.in2p3.fr/). A username will be automatically created, which you can change on your profile page (on the top right hand corner, you can click on your profile).


## First steps to follow after login in for the first time

First, you will need to head to the `Groups` page. There, you can request to be added to the groups you are interested in.
Exemple: You are a member of GRANDMA, you can ask to be added to the group `GRANDMA`. You are also interested in seeing alerts from Fink, you can ask to be added to the group `Fink`.

An administrator of the group will be notified of your request. After accepting it, you will receive a notification (you can see it on the top right hand corner of the screen, it is a bell icon) to tell you that you have been added to the group.

Now, you can explore the rest of the platform.



## User permissions and roles

As a new user of SkyPortal, you won't be able to do much at first. Users can have different roles, that come with a predeterminated set of permissions. A user can also be granted a permission without a specific role.
To use certain (most) features of the platform, you will need certain permissions.
Exemple: You can see the list of telescopes, but you can't add a new one. You can see the shifts, but you can't add or join one.
To access those different features, administrators of the platform can provide it to you. You can ask them, but they should take care of it for every user without having to ask them. If you need additional permissions (like the permission to add a source, ...), you can always ask them.
At first, you will be granted the `Manage shift` permission, which allows you to interact with shifts.

## User Guide

You will find a more in depth guide to use SkyPortal for Grandma on the [User Guide](./user_guide/index.md) page.
