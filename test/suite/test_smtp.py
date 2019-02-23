#!/usr/bin/env python3

import smtplib
import pytest
import ssl

import tools
from tools import server_address, database_address  # noqa: F401


@pytest.fixture(scope="module")  # noqa: F811
def server(server_address, database_address):
    """Add fixtures into the database before testing"""

    domains = [(1, "sith.local"), (2, "jedi.local")]
    users = [
        (1, "{PLAIN}test", "sidious"),
        (1, "{PLAIN}test", "vader"),
        (2, "{PLAIN}test", "luke"),
        (2, "{PLAIN}test", "leia"),
    ]
    alias_domains = [("good.local", "jedi.local"), ("evil.local", "sith.local")]
    aliases = [(2, "anakin", "vader@sith.local"),  # anakin@jedi.local
               (2, "kenobi", "ben@tatooine.local")]  # kenobi@jedi.local

    tools.insert_virtual_domains(database_address, domains)
    tools.insert_virtual_users(database_address, users)
    tools.insert_virtual_alias_domains(database_address, alias_domains)
    tools.insert_virtual_aliases(database_address, aliases)
    return server_address


def send_mail(recipient, *, sender="tester@mail.not.local", server=None, conn=None):
    if conn is None:
        conn = smtplib.SMTP(server)
        print("New connection established")
    else:
        print("Connection already established")
    return conn.sendmail(sender, recipient, "hello !")


def login(user, password="test", *, server=None, submission=False):
    """Creates a connection and logs in with user & password. sumbission can be
    specified to log in on 587 port (submission) over a TLS connection.
    Returns ( login state , connection object ).
    """
    if submission:
        conn = smtplib.SMTP(server, 587)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        conn.ehlo()
        conn.starttls(context=context)
    else:
        conn = smtplib.SMTP(server)
    print("connection established")
    conn.ehlo("mail.not.local")
    return (conn.login(user, password)[0], conn)


def login_error_code(user, **kwargs):
    with pytest.raises(Exception) as excinfo:
        _, _ = login(user, **kwargs)
    print(excinfo)
    print(excinfo.value)
    return excinfo.value.smtp_code


def smtp_error_code(recipient, **kwargs):
    with pytest.raises(Exception) as excinfo:
        send_mail(recipient, **kwargs)
    print(excinfo.value)
    return excinfo.value.recipients[recipient][0]


# Tests
# Reception


@pytest.mark.parametrize(
    "recipient", [("vader@sith.local"), ("sidious@sith.local"), ("luke@jedi.local")]
)
def test_legit_users(recipient, server):
    assert send_mail(recipient, server=server) == dict()


def test_wrong_domain(server):
    """What happens if the domain is not handled.
    should be error 554 5.7.1 Relay access denied"""
    assert smtp_error_code("luke@gryffindor.local", server=server) == 554


def test_wrong_user(server):
    """What happens if the user is unknown
    should be error 550 5.1.1 Recipient address rejected: User unknown in
    virtual mailbox table"""
    assert smtp_error_code("snore@sith.local", server=server) == 550


def test_domain_user_mismatch(server):
    """A user from a domain should not recieve mail from the others"""
    assert smtp_error_code("sidious@jedi.local", server=server) == 550


def test_external_alias(server):
    assert send_mail("anakin@jedi.local", server=server) == dict()


def test_internal_alias(server):
    assert send_mail("kenobi@jedi.local", server=server) == dict()


@pytest.mark.parametrize("recipient", [("sidious@evil.local"), ("luke@good.local")])
def test_domain_alias(server, recipient):
    """Test whole domain alias feature."""
    assert send_mail(recipient, server=server) == dict()


def test_invalid_sender(server):
    assert smtp_error_code("luke@jedi.local", sender="vader@none", server=server) == 504


def test_non_existant_sender_domain(server):
    """Should be 450 4.1.8 Sender address rejected: Domain not found"""
    assert (
        smtp_error_code("luke@jedi.local", sender="vader@hogwarts.local", server=server)
        == 450
    )


def test_impostor_relay(server):
    assert (
        smtp_error_code(
            "johndoe@mail.not.local", sender="vader@sith.local", server=server
        )
        == 554
    )


@pytest.mark.parametrize(
    "sender",
    [
        ("vader@sith.local"),  # existing user
        ("vadoooooor@sith.local"),  # non-existing user
    ],
)
def test_impostor_local(sender, server):
    """Sending mail to local as local user, not logged in
    should be 553 5.7.1 Sender address rejected: not logged in"""
    assert smtp_error_code("luke@jedi.local", sender=sender, server=server) == 553


# Outgoing email


@pytest.mark.parametrize(
    "user, submission",
    [
        ("sidious@sith.local", False),
        ("luke@jedi.local", True),
        ("vader@sith.local", True),
    ],
)
def test_login(user, submission, server):
    """We check if legitimate users can log in"""
    assert login(user, submission=submission, server=server)[0] == 235


@pytest.mark.parametrize(
    "user,password", [("kirby", "nom-nom"), ("sidious", "jedi-ftw")]
)
def test_wrong_login(user, password, server):
    """Client should not be able to login with wrong credentials"""
    assert login_error_code(user, password=password, server=server) == 535


@pytest.mark.parametrize(
    "recipient",
    [
        ("pikachu@mail.not.local"),  # non-local user
        ("sidious@sith.local"),  # local user
    ],
)
def test_auth_relay(recipient, server):
    """Send email to another domain from an authenticated account"""
    sender = "luke@jedi.local"
    state, conn = login(sender, "test", submission=True, server=server)
    result = send_mail(recipient, sender=sender, conn=conn, server=server)
    assert result == dict()


@pytest.mark.parametrize(
    "victim",
    [
        ("pikachu@mail.not.local"),  # non-local user
        ("sidious@sith.local"),  # local user
    ],
)
def test_auth_relay_mismatch(victim, server):
    """Login as a user and send an email as another user.
    Should be error 553 5.7.1 Sender access reject: not owned by user"""
    state, conn = login("luke@jedi.local", "test", submission=True, server=server)
    result = smtp_error_code(
        "sidious@sith.local", sender=victim, conn=conn, server=server
    )
    assert result == 553
