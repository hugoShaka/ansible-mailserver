#!/usr/bin/env python3

import pytest
import smtplib

def send_mail(recipient,*, sender="tester@mail.not.local"):
    conn = smtplib.SMTP("mail.shaka.local")
    print("connection established")
    return conn.sendmail(sender,recipient ,"hello !")

@pytest.mark.parametrize("recipient", [
    ("sidious@sith.local"),
    ("vader@sith.local"),
    ("obiwan@jedi.local"),
])
def test_legit_users(recipient):
    assert send_mail(recipient) == dict()

def test_wrong_domain():
    with pytest.raises(Exception) as excinfo:
        send_mail("obiwan@gryffindor.local")
    print(excinfo)
    print(excinfo['obiwan@gryffindor.local'][0])
    assert excinfo['obiwan@gryffindor.local'][0] == 554

def test_wrong_user():
    pass

def test_domain_user_mismatch():
    #("sidious@jedi.local"), # 
    pass

@pytest.mark.skip()
def test_alias():
    assert send_mail("anakin@jedi.local") == dict()

