Testing process
===============

Quickstart
----------
- Vagrant
- ansible > 2.4

Testing envionment
------------------

Mocking DNS
^^^^^^^^^^^

Pytest client
^^^^^^^^^^^^^

Tests
-----

SMTP
^^^^

IMAP
^^^^

Replication
^^^^^^^^^^^

End to End
^^^^^^^^^^^

Continuous integration
----------------------
The continuous interation process is composed of two parts which are Azure
Pipelines and Travis-CI.

Azure pipeline handles the molecule testing of the role by providing a virtual
machine per molecule senario. Azure pipelines are managed via the
``azure-pipelines.yml`` file.

Travis-CI handles all the other builds like documentation, docker images,
releases, ... Travis-CI is configured via the ``.travis-ci.yml`` file.

Molecule
--------
