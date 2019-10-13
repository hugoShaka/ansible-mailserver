import imapclient
import ssl
import pytest
import uuid

import tools
from tools import server_address, database_address  # noqa: F401


@pytest.fixture(scope="module")  # noqa: F811
def server(server_address, database_address):  # noqa: F811
    """Add fixtures into the database before teesting"""

    domains = [(1, "sith.local"), (2, "jedi.local")]
    users = [
        (2, "{PLAIN}test", "padme"),
        (2, "{PLAIN}test", "obiwan"),
        (1, "{PLAIN}test", "maul"),
    ]

    tools.insert_virtual_domains(database_address, domains)
    tools.insert_virtual_users(database_address, users)
    return server_address


@pytest.fixture(scope="module")
def populate_mailbox(server):
    _, conn = login("padme@jedi.local", server=server)
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


@pytest.mark.parametrize(
    "user", [("maul@sith.local"), ("obiwan@jedi.local"), ("padme@jedi.local")]
)
def test_login(user, server):
    """We check if legitimate users can log in"""
    assert login(user, server=server)[0] == "Logged in"


@pytest.mark.parametrize(
    "user, password",
    [
        ("sidious@sith.local", "wrongpassword"),
        ("bowser@jedi.local", "test"),
        ("sidious@pokemon.local", "test"),
    ],
)
def test_invalid_credentials(user, password, server):
    """Users with invalid credentials should not be able to log in"""
    assert (
        login_error_code(user, password=password, server=server)
        == "AUTHENTICATIONFAILED"
    )


def test_no_tls(server):
    """No login should be possible over non-TLS"""
    conn = imapclient.IMAPClient(server, 143, ssl=False)
    assert login_error_code("obiwan@jedi.local", conn=conn) == "PRIVACYREQUIRED"


def test_read_email(populate_mailbox, server):
    """Reads fixture emails and recover content"""
    _, conn = login("padme@jedi.local", server=server)
    folder, flag = populate_mailbox
    conn.select_folder(folder)
    messages_ids = conn.search("ALL")
    assert len(messages_ids) == 3
    messages = conn.fetch(messages_ids, "RFC822")
    message_content = messages[messages_ids[0]][b"RFC822"].decode("utf-8")
    assert message_content == flag
