Certificates
============

**Role Variables**

.. include:: ../roles/ispmail-certificate/defaults/main.yml
   :literal:

Introduction
------------

A lot of differets certificates are used in this role. We can divide them in
two categories : 

- certificates that will be used by external entities (MXs, MUA, ...)
- certificates that are restricted for internal use (DB connection,
  replication, ...)


Public facing certs
-------------------

Those certs should be trusted by the client (MX or MUA).
For testing setups we're using self-signed certificates, for productions ones
letsencrypt is used.

Depending on what protocol is used to contact the server the client will ask
for a server-specific domain-name or a domain-name shared by both serverA and
serverB.

Example (FQDN stands for Fully Qualified Domain Name):

serverA::
  FQDN : serverA.example.com

ServerB::
  FQDN : serverB.example.com

MX entries::
  MX 50 mail.example.com serverA.example.com
  MX 50 mail.example.com serverB.example.com

Submission DNS entry::
  A submission.example.com <serverA IP>
  A submission.example.com <serverB IP>

Here an MTA will pick an MX entry and access serverA by its FQDN. So serverA
should provide a cert valid for ``serverA.example.com``.
A MUA asking to sumbit new mail through submission will not know there are two
servers and will ask serverA or serverB for ``submission.example.com``. The
same goes for IMAP/POP/Sieve.

Internal PKI
------------

In case of internal communication we don't need our certs to be trusted by the
usual PKIs (Public Key Infrastructures). We only need the cert to be trsuted by
all of our servers.

Each server will generate a CA (Certifiate Authority) and sign its certificates
with its own CA.

Each server will trust the other servers' CA, thus will trust the other servers
certificates.

This is our own internal PKI.

Such certs are used for:
- MDA replication

Those certs will also be used for:
- LMTP in case of distant MDA
- DB connection
