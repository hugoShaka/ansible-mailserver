#!/usr/bin/env python3

import smtplib
import pytest
import ssl

##### Helpers


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


##### Tests

### Reception


@pytest.mark.parametrize(
    "recipient", [("sidious@sith.local"), ("vader@sith.local"), ("obiwan@jedi.local")]
)
def test_legit_users(recipient, primary):
    assert send_mail(recipient, server=primary) == dict()


def test_wrong_domain(primary):
    """What happens if the domain is not handled.
    should be error 554 5.7.1 Relay access denied"""
    assert smtp_error_code("obiwan@gryffindor.local", server=primary) == 554


def test_wrong_user(primary):
    """What happens if the user is unknown
    should be error 550 5.1.1 Recipient address rejected: User unknown in
    virtual mailbox table"""
    assert smtp_error_code("snore@sith.local", server=primary) == 550


def test_domain_user_mismatch(primary):
    """A user from a domain should not recieve mail from the others"""
    assert smtp_error_code("sidious@jedi.local", server=primary) == 550


@pytest.mark.skip()
def test_external_alias(primary):
    assert send_mail("anakin@jedi.local", server=primary) == dict()


@pytest.mark.skip()
def test_internal_alias(primary):
    assert send_mail("luke@jedi.local", server=primary) == dict()


def test_invalid_sender(primary):
    assert smtp_error_code("obiwan@jedi.local", sender="vader@none", server=primary) == 504


def test_non_existant_sender_domain(primary):
    """Should be 450 4.1.8 Sender address rejected: Domain not found"""
    assert smtp_error_code("obiwan@jedi.local", sender="vader@poudlard.local", server=primary) == 450


def test_impostor_relay(primary):
    assert smtp_error_code("obiwan@jedi.not.local", sender="vader@sith.local", server=primary) == 554


@pytest.mark.parametrize(
    "sender",
    [
        ("vader@sith.local"),  # existing user
        ("vadoooooor@sith.local"),  # non-existing user
    ],
)
def test_impostor_local(sender, primary):
    """Sending mail to local as local user, not logged in
    should be 553 5.7.1 Sender address rejected: not logged in"""
    assert smtp_error_code("obiwan@jedi.local", sender=sender, server=primary) == 553


##### Outgoing email


@pytest.mark.parametrize(
    "user, submission",
    [
        ("sidious@sith.local", False),
        ("obiwan@jedi.local", True),
        ("vader@sith.local", True),
    ],
)
def test_login(user, submission, primary):
    """We check if legitimate users can log in"""
    assert login(user, submission=submission, server=primary)[0] == 235


@pytest.mark.parametrize(
    "user,password", [("kirby", "nom-nom"), ("sidious", "jedi-ftw")]
)
def test_wrong_login(user, password, primary):
    """Client should not be able to login with wrong credentials"""
    assert login_error_code(user, password=password, server=primary) == 535


@pytest.mark.parametrize(
    "recipient",
    [
        ("pikachu@mail.not.local"),  # non-local user
        ("sidious@sith.local"),    # local user
    ],
)
def test_auth_relay(recipient, primary):
    """Send email to another domain from an authenticated account"""
    sender = "obiwan@jedi.local"
    state, conn = login(sender, "test", submission=True, server=primary)
    result = send_mail(recipient, sender=sender, conn=conn, server=primary)
    assert result == dict()

@pytest.mark.parametrize(
    "victim",
    [
        ("pikachu@mail.not.local"),  # non-local user
        ("sidious@sith.local"),    # local user
    ],
)
def test_auth_relay_mismatch(victim, primary):
    """Login as a user and send an email as another user.
    Should be error 553 5.7.1 Sender access reject: not owned by user"""
    state, conn = login("obiwan@jedi.local", "test", submission=True, server=primary)
    result = smtp_error_code("sidious@sith.local", sender=victim, conn=conn, server=primary)
    assert result == 553
