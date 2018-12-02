import imapclient
import ssl
import pytest
import uuid
import psycopg2


@pytest.fixture(scope="session")
def populate_db(server):
    """Add fixtures into the database before teesting"""

    sql_domain = """INSERT INTO virtual_domains VALUES (%s, %s)
                    ON CONFLICT DO NOTHING;"""
    sql_user = """INSERT INTO virtual_users (domain_id, password, email)
                  VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;"""
    domains = [(1, 'sith.local'), (2, 'jedi.local')]
    users = [
            (2, "{PLAIN}test", "padme"),
            (2, "{PLAIN}test", "obiwan"),
            (1, "{PLAIN}test", "maul"),
            ]

    # TODO(shaka) gather password using testinfra and ansible info
    conn = psycopg2.connect(
        host=server, dbname="mailserver", user="pgadmin", password="ChangeMeAlso"
    )
    cur = conn.cursor()
    for domain in domains:
        cur.execute(sql_domain, domain)
        conn.commit()

    for user in users:
        cur.execute(sql_user, user)
        conn.commit()
    cur.close()


@pytest.fixture(scope="session")
def populate_mailbox(server, populate_db):
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
def test_login(user, server, populate_db):
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
def test_invalid_credentials(user, password, server, populate_db):
    """Users with invalid credentials should not be able to log in"""
    assert (
        login_error_code(user, password=password, server=server)
        == "AUTHENTICATIONFAILED"
    )


def test_no_tls(server, populate_db):
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
