import imapclient
import ssl
import pytest
import uuid

FOLDER = "folder-%s" % uuid.uuid4()
FLAG = "May the force be with you %s" % uuid.uuid4()

@pytest.fixture(scope='session')
def populate_mailbox():
    _, conn = login("padme@jedi.local")
    conn.create_folder(FOLDER)
    conn.append(FOLDER, FLAG)
    conn.append(FOLDER, FLAG)
    conn.append(FOLDER, FLAG)

def login(user, password="test", *, conn=None):
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    if conn is None:
        conn = imapclient.IMAPClient("mail.shaka.local", 993, ssl_context=ssl_context)
    result = conn.login(user, password)
    return result.decode("utf-8"), conn

def login_error_code(user, **kwargs):
    with pytest.raises(Exception) as excinfo:
        _, _ = login(user, **kwargs)
    print(excinfo)
    print(excinfo.value)
    return excinfo.value.args[0].split(' ')[0][3:-1]

@pytest.mark.parametrize(
    "user",
    [
        ("sidious@sith.local"),
        ("obiwan@jedi.local"),
        ("vader@sith.local"),
    ],
)
def test_login(user):
    """We check if legitimate users can log in"""
    assert login(user)[0] == 'Logged in'

@pytest.mark.parametrize(
    "user, password",
    [
        ("sidious@sith.local", "wrongpassword"),
        ("bowser@jedi.local", "test"),
        ("sidious@pokemon.local", "test"),
    ],
)
def test_invalid_credentials(user, password):
    """Users with invalid credentials should not be able to log in"""
    assert login_error_code(user, password=password) == 'AUTHENTICATIONFAILED'

def test_no_tls():
    """No login should be possible over non-TLS"""
    conn = imapclient.IMAPClient("mail.shaka.local", 143, ssl=False)
    assert login_error_code("obiwan@jedi.local", conn=conn) == 'PRIVACYREQUIRED'

def test_read_email(populate_mailbox):
    """Reads fixture emails and recover content"""
    _, conn = login("padme@jedi.local")
    conn.select_folder(FOLDER)
    messages_ids = conn.search('ALL')
    assert len(messages_ids) == 3
    messages = conn.fetch(messages_ids, 'RFC822')
    message_content = messages[messages_ids[0]][b'RFC822'].decode('utf-8')
    assert message_content == FLAG
