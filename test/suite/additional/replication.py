import imapclient
import ssl
import pytest
import uuid
import time
import os

import tools
from tools import database_address  # noqa: F401

@pytest.fixture(scope="module")
def servers(database_address):
    import testinfra.utils.ansible_runner

    inventory = testinfra.utils.ansible_runner.AnsibleRunner(
        os.environ["MOLECULE_INVENTORY_FILE"]
    )
    mda_hosts = inventory.get_hosts("mda")
    if len(mda_hosts) != 2:
        raise ValuerError("Too many mda hosts")

    server_ips = []
    for mda_host in mda_hosts:
        mda_facts = inventory.run_module(mda_host, "setup", [])
        mda_ip = mda_facts["ansible_facts"]["ansible_default_ipv4"]["address"]
        server_ips.append(mda_ip)

    domains = [(1, "sith.local"), (2, "jedi.local")]
    users = [
        (2, "{PLAIN}test", "rey"),
    ]

    tools.insert_virtual_domains(database_address, domains)
    tools.insert_virtual_users(database_address, users)

    return server_ips


@pytest.fixture()
def populate_mailbox(servers):
    _, conn = login("rey@jedi.local", server=servers[0])
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


def test_read_email(populate_mailbox, servers):
    """Reads fixture emails and recover content"""
    _, conn1 = login("rey@jedi.local", server=servers[0])
    _, conn2 = login("rey@jedi.local", server=servers[1])
    folder, flag = populate_mailbox
    # We wait or the server to do the sync
    time.sleep(5)
    check_messages(conn1, folder, flag)
    check_messages(conn2, folder, flag)
