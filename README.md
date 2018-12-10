# ISPmail Ansible Playbook #

This repository contains a playbook and roles that you can use to set up your
own Debian-based mail server. Behind the scene, it makes use of postfix,
 dovecot, postgresql.

This is a modified version of the original repo :
(https://git.workaround.org/chaas/ansible-ispmail-jessie/)

Modifications include:
* use of postgres
* rewrite in ansible-style
* tests and CI
* webmail removed

# Development

## Dependencies

* vagrant
* ansible 2.6
* python 3
* virtualbox (other virts may work too)
* molecule
* docker

## Setting up

* Clone the repository
* `cd ansible-mailserver`
* *If you want to use a virtual environment make sure it is activated here*

You can use vagrant :

* `vagrant up` will create 3 VMs : the mailservers (north and south) and the tester

Or you can use molecule dans docker :

* molecule converge

## Running tests

### With molecule

* `molecule test` or `molecule test -s single` will run the full test suite

### With vagrant

Tests are  manually started :
* `vagrant ssh tester`
* `cd suite`
* `pytest`

Test suites `test_imap.py` and `test_dmtp.py` hits by default
`north.mail.local`. The target can be configured with the flag `--server`.

# Credits and copyrights #

The original code was written by Christoph "Signum" Haas © for
(http://www.workaround.org) and is licensed under MIT.
Please take a look at his article about mailservers, it's one of the best you
could find on the Internet.

Contributors :
- Christopher Haas (original code : ansible-ispmail-jessie)
- hugoShaka
- dric0

# License

According to the original license everything in this repository can be freely
used under the terms of the MIT license.
