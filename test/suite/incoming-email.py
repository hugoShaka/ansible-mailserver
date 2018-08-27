#!/usr/bin/env python3

import pytest
import smtplib

def send_mail(recipient,* , sender="tester@mail.not.local"):
    conn = smtplib.SMTP("mail.shaka.local")
    print("connection established")
    return conn.sendmail(sender,recipient ,"hello !")

def smtp_error_code(recipient, **kwargs):
    with pytest.raises(Exception) as excinfo:
        send_mail(recipient, **kwargs)
    print(excinfo.value)
    return excinfo.value.recipients[recipient][0]


@pytest.mark.parametrize("recipient", [
    ("sidious@sith.local"),
    ("vader@sith.local"),
    ("obiwan@jedi.local"),
])
def test_legit_users(recipient):
    assert send_mail(recipient) == dict()

def test_wrong_domain():
    """What happens if the domain is not handled.
    should be error 554 5.7.1 Relay access denied"""
    assert smtp_error_code("obiwan@gryffindor.local") == 554

def test_wrong_user():
    """What happens if the user is unknown
    should be error 550 5.1.1 Recipient address rejected: User unknown in
    virtual mailbox table"""
    assert smtp_error_code("snore@sith.local") == 550

def test_domain_user_mismatch():
    """A user from a domain should not recieve mail from the others"""
    assert smtp_error_code("sidious@jedi.local") == 550

@pytest.mark.skip()
def test_external_alias():
    assert send_mail("anakin@jedi.local") == dict()

@pytest.mark.skip()
def test_internal_alias():
    assert send_mail("luke@jedi.local") == dict()

def test_invalid_sender():
    assert smtp_error_code("obiwan@jedi.local", sender='vader@none') == 504

def test_non_existant_sender_domain():
    """Should be 450 4.1.8 Sender address rejected: Domain not found"""
    assert smtp_error_code("obiwan@jedi.local", sender='vader@poudlard.local') == 450

def test_impostor_relay():
    assert smtp_error_code("obiwan@jedi.not.local", sender='vader@sith.local') == 554

@pytest.mark.parametrize("sender", [
    ("vader@sith.local"), #existing user
    ("vadoooooor@sith.local"), #non-existing user
])
def test_impostor_local(sender):
    """Sending mail to local as local user, not logged in
    should be 553 5.7.1 Sender address rejected: not logged in"""
    assert smtp_error_code("obiwan@jedi.local", sender=sender) == 553

