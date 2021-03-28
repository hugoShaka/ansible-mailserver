import imapclient
import ssl
import pytest
import uuid
import time
import os

import tools
from tools import database  # noqa: F401

class HackyHost():
    """
    This is a hacky reimplementation of what testinfra `host` does. I want to
    be able to instanciate a `database` and need something with a `run_expect`
    method to do so.
    """
    def __init__(self, inventory, db_host):
        self.inventory = inventory
        self.host = db_host

    def run_expect(self, expected, command):
        out = self.inventory.run_module(self.host, "shell", module_args=command, check=False)
        assert out["rc"] in expected, "Unexpected exit code {} for {}".format(out.rc, out)
        return out

@pytest.fixture(scope="module")
def servers(dbtype):
    import testinfra.utils.ansible_runner

    domains = [(1, "sith.local"), (2, "jedi.local")]
    users = [
        (2, "{PLAIN}test", "rey"),
    ]


    inventory = testinfra.utils.ansible_runner.AnsibleRunner(
        os.environ["MOLECULE_INVENTORY_FILE"]
    )
    db_hosts = inventory.get_hosts("db")

    # we cannot use the database fixture as it is host-scoped
    # we're breaking the testinfra abstraction by loading the ansible inventory
    # and looking up the db and mda IPs.
    for db_host in db_hosts:
        host = HackyHost(inventory, db_host)
        database = tools.get_database(host, dbtype)
        database.insert_virtual_domains(domains)
        database.insert_virtual_users(users)

    mda_hosts = inventory.get_hosts("mda")
    if len(mda_hosts) != 2:
        raise ValuerError("Too many mda hosts")

    mda_ips = []
    for mda_host in mda_hosts:
        mda_facts = inventory.run_module(mda_host, "setup", [])
        mda_ip = mda_facts["ansible_facts"]["ansible_default_ipv4"]["address"]
        mda_ips.append(mda_ip)

    return mda_ips


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
    time.sleep(20)
    check_messages(conn1, folder, flag)
    check_messages(conn2, folder, flag)
