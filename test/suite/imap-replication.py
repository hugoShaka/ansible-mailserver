import imapclient
import ssl
import pytest
import uuid
import time


@pytest.fixture()
def populate_mailbox(primary):
    _, conn = login("padme@jedi.local", server=primary)
    folder = "folder-%s" % uuid.uuid4()
    flag = "May the force be with you %s" % uuid.uuid4()
    conn.create_folder(folder)
    conn.append(folder, flag)
    conn.append(folder, flag)
    conn.append(folder, flag)
    return (folder, flag)


def login(user, password="test", *, conn=None, server=None):
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    if conn is None:
        conn = imapclient.IMAPClient(server, 993, ssl_context=ssl_context)
    result = conn.login(user, password)
    return result.decode("utf-8"), conn


def login_error_code(user, **kwargs):
    with pytest.raises(Exception) as excinfo:
        _, _ = login(user, **kwargs)
    print(excinfo)
    print(excinfo.value)
    return excinfo.value.args[0].split(" ")[0][3:-1]


def check_messages(conn, folder, flag):
    """Checks if there are 3 messages in the fodler and that they contain the
    flag."""
    conn.select_folder(folder)
    messages_ids = conn.search("ALL")
    assert len(messages_ids) == 3
    messages = conn.fetch(messages_ids, "RFC822")
    message_content = messages[messages_ids[0]][b"RFC822"].decode("utf-8")
    assert message_content == flag


def test_read_email(populate_mailbox, primary, secondary):
    """Reads fixture emails and recover content"""
    _, conn1 = login("padme@jedi.local", server=primary)
    _, conn2 = login("padme@jedi.local", server=secondary)
    folder, flag = populate_mailbox
    # We wait or the server to do the sync
    time.sleep(5)
    check_messages(conn1, folder, flag)
    check_messages(conn2, folder, flag)
