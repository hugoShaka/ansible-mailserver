# Mailserver Ansible Playbook

This repository contains a playbook and roles that you can use to set up your
own Debian-based mail server. Behind the scenes, it makes use of postfix,
dovecot, postgresql or sqlite.

This is a modified version of the original repo:
(https://git.workaround.org/chaas/ansible-ispmail-jessie/)

Modifications include:
* use of postgres/sqlite
* rewrite most of the code to be ansible-ish
* tests and CI
* webmail removed
* antispam using rspamd
* active-active replication

# Development

## Dependencies

* ansible
* python 3
* molecule
* docker

## Setting up

* molecule converge

## Running tests

### With molecule

* `molecule test` or `molecule test -s single` will run the full test suite with postgres
* `molecule test -s sqlite` or `molecule test -s sqlite-double` will run the full test suite with postgres


### With vagrant

Tests are  manually started:
* `vagrant ssh tester`
* `cd suite`
* `pytest`

Test suites `test_imap.py` and `test_smtp.py` hit by default
`north.mail.local`. The target can be configured with the flag `--server`.

# Credits and copyrights

The original code was written by Christoph "Signum" Haas © for
(http://www.workaround.org) and is licensed under MIT.
Please take a look at his article about mailservers, it's one of the best you
can find on the Internet.

Contributors:
- Christopher Haas (original code: ansible-ispmail-jessie)
- hugoShaka
- dric0

# License

According to the original license everything in this repository can be freely
used under the terms of the MIT license.
