from typing import List
import psycopg2
import pytest
import os

ADD_DOMAIN_QUERY = """INSERT INTO virtual_domains
                      VALUES (%s, %s)
                      ON CONFLICT DO NOTHING;"""

ADD_USER_QUERY = """INSERT INTO virtual_users (domain_id, password, email)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING;"""

ADD_ALIAS_DOMAIN_QUERY = """INSERT INTO virtual_alias_domains (source, destination)
                            VALUES (%s, %s)
                            ON CONFLICT DO NOTHING;"""


def insert_virtual_domains(database_address: str, domains: List):
    """Add domain fixtures into the database."""

    do_query(database_address, ADD_DOMAIN_QUERY, domains)


def insert_virtual_users(database_address: str, users: List):
    """Add users fixtures into the database."""

    do_query(database_address, ADD_USER_QUERY, users)


def insert_virtual_alias_domains(database_address: str, alias_domains: List):
    """Add alias_domains fixtures into the database"""

    do_query(database_address, ADD_ALIAS_DOMAIN_QUERY, alias_domains)


def do_query(server_address: str, query: str, items: List):
    """Opens a connection and executes a database query."""

    conn = psycopg2.connect(
        host=server_address,
        dbname="mailserver",
        user="pgadmin",
        password="PGAdmin_Password",
    )

    cur = conn.cursor()
    for item in items:
        cur.execute(query, item)
        conn.commit()
    cur.close()


@pytest.fixture(scope="session")
def database_address(request):
    import testinfra.utils.ansible_runner

    inventory = testinfra.utils.ansible_runner.AnsibleRunner(
        os.environ["MOLECULE_INVENTORY_FILE"]
    )
    database_facts = inventory.run("north", "setup")
    database_ip = database_facts["ansible_facts"]["ansible_default_ipv4"]["address"]

    return database_ip


@pytest.fixture(scope="module")
def server_address(request, host):
    """Get server address"""

    return host.interface("eth0").addresses[0]
