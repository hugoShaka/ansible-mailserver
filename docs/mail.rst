Email basics
============

The big picture
---------------
Sending email involves lots of components.

.. image:: https://res.cloudinary.com/shaka/image/upload/v1545332352/ansible_mailserver/simple_mail_1.png

Components
----------

Mail Transfer Agent
^^^^^^^^^^^^^^^^^^^
Within Internet message handling services (MHS), a message transfer agent or
mail transfer agent (MTA) or mail relay is software that transfers electronic
mail messages from one computer to another using a client–server application
architecture. An MTA implements both the client (sending) and server (receiving)
portions of the Simple Mail Transfer Protocol.

The terms mail server, mail exchanger, and MX host may also refer to a computer
performing the MTA function. The Domain Name System (DNS) associates a mail
server to a domain with an MX record containing the domain name of the host(s)
providing MTA services. [Wikipedia_MTA]_

Mail Delivery Agent
^^^^^^^^^^^^^^^^^^^

A mail delivery agent or message delivery agent (MDA) is a computer software
component that is responsible for the delivery of e-mail messages to a local
recipient's mailbox. It is also called a local delivery agent (LDA).

Within the Internet mail architecture, local message delivery is achieved
through a process of handling messages from the message transfer agent, and
storing mail into the recipient's environment (typically a mailbox).
[Wikipedia_MDA]_

Mail User Agent
^^^^^^^^^^^^^^^
In Internet, an email client, email reader or more formally mail user agent
(MUA) is a computer program in the category of groupware environments used to
access and manage a user's email.

Client is meant to be a role. For example, a web application which provides
message management, composition, and reception functions may internally act as
an email client; as a whole, it is commonly referred to as webmail. Likewise,
email client may refer to a piece of computer hardware or software whose
primary or most visible role is to work as an email client.  [Wikipedia_MUA]_

Protocols
---------

SMTP
^^^^

LMTP
^^^^

IMAP
^^^^

POP
^^^

Sieve
^^^^^

SPF
^^^

DKIM
^^^^

DMARC
^^^^^


.. [Wikipedia_MTA] Message transfer agent,
  https://en.wikipedia.org/w/index.php?title=Message_transfer_agent&oldid=863112371
  (last visited Nov. 13, 2018). 

.. [Wikipedia_MDA] Mail delivery agent,
  https://en.wikipedia.org/w/index.php?title=Mail_delivery_agent&oldid=860431679
  (last visited Nov. 13, 2018). 

.. [Wikipedia_MUA] Email client,
  https://en.wikipedia.org/w/index.php?title=Email_client&oldid=869783973 
  (last visited Dec. 2, 2018).
