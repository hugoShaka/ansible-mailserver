# ISPmail Ansible Playbook #

This repository contains a playbook and roles that you can use to set up your
own Debian-based mail server. Behind the scene, it makes use of postfix,
 dovecot, postgresql.

This is a modified version of the original repo :
(https://git.workaround.org/chaas/ansible-ispmail-jessie/)

Please follow the instructions at https://workaround.org/ispmail/jessie/ansible
DO NOT APPLY IF YOU ARE NOT CONFIDENT WITH WHAT THE PLAYBOOK DOES.

# Development

## Dependencies

* vagrant
* ansible 2.6
* python 3
* virtualbox (other virts may work too)

## Setting up

* Clone the repository
* `cd ansible-mailserver`
* *If you've installed ansible in a venv make sure it is activated here*
* `vagrant up` will create 3 VMs : the mailservers (north and south) and the tester

## Running tests

Tests are still manually started.
* `vagrant ssh tester`
* `cd suite`
* `pytest <yourtestfile.py> [--server south.mail.local]`

Test suites `imap.py` and `incoming-email.py` hits by default
`north.mail.local`. The target can be configured with the flag `--server`.

# Credits and copyrights #

The original code was written by Christoph "Signum" Haas © for
(http://www.workaround.org).
Please take a look at his article about mailservers, it's one of the best you
could find on the Internet.

Contributors :
- Christopher Haas (original code : ansible-ispmail-jessie)
- hugoShaka

# License

Everything in this repository can be freely used under the terms of the MIT license.

