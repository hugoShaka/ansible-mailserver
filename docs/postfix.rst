Postfix
=======

**Role Variables:**

.. include:: ../roles/ispmail-postfix/defaults/main.yml
   :literal:

Postscreen
----------

Milters
-------

Virtual Mapping
---------------

Domain Alias
^^^^^^^^^^^^
Domain aliasing allows to redirect all the mail for a domain to another without
creating an alias per user. Domain alias are defined in the
``virtual_alias_domains`` database table.
Domain-wide aliasing is done in 2 steps :

1. Declaring that the server is this domain's final destination and that
   the mail will be handled by aliases, redirecting to a local or remote
   domain. This is done by using the ``virtual_alias_domains`` parameter. The
   postgresql query is described in ``pgsql-virtual-alias-domains.cf``.

2. Creating the domain-wide alias. This is done by the ``virtual_alias_maps``
   parameter. As specified in the `Virtual Mapping`_ section three lookups are
   made. We're relying on the third one (``@domain``) and will return the
   destination domain. The postgresql request is described in
   ``pgsql-virtual-alias-domains-maps.cf``.

LMTP
----

IPv6
----
