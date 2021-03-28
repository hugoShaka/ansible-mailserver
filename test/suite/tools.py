from typing import List
import psycopg2
import pytest
import os

ADD_DOMAIN_QUERY = """INSERT INTO virtual_domains (id, name)
                      VALUES (%s, %s)
                      ON CONFLICT DO NOTHING;"""

ADD_USER_QUERY = """INSERT INTO virtual_users (domain_id, password, email)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING;"""

ADD_ALIAS_DOMAIN_QUERY = """INSERT INTO virtual_alias_domains (source, destination)
                            VALUES (%s, %s)
                            ON CONFLICT DO NOTHING;"""

ADD_ALIASES_QUERY = """INSERT INTO virtual_aliases (domain_id, source, destination)
                            VALUES (%s, %s, %s)
                            ON CONFLICT DO NOTHING;"""


class Database():
    def insert_virtual_domains(self, domains: List):
        """Add domain fixtures into the database."""

        self.do_query(ADD_DOMAIN_QUERY, domains)


    def insert_virtual_users(self,  users: List):
        """Add users fixtures into the database."""

        self.do_query(ADD_USER_QUERY, users)


    def insert_virtual_alias_domains(self, alias_domains: List):
        """Add alias_domains fixtures into the database"""

        self.do_query(ADD_ALIAS_DOMAIN_QUERY, alias_domains)


    def insert_virtual_aliases(self, aliases: List):
        """Add aliases fixtures into the database"""

        self.do_query(ADD_ALIASES_QUERY, aliases)


class PostgresDatabase(Database):
    def __init__(self, ip, dbname, user, password):
        self.conn = psycopg2.connect(
            host=ip,
            dbname=dbname,
            user=user,
            password=password,
        )

    def do_query(self, query, items):
        cur = self.conn.cursor()
        for item in items:
            cur.execute(query, item)
            self.conn.commit()
        cur.close()


class SqliteDatabase(Database):
    def __init__(self, host):
        self.host = host

    def do_query(self, query, items):
        for item in items:
            # escape values to be inserted with single quotes
            print(item)
            item_escaped = tuple((f"'{x}'" for x in item))
            print(item_escaped)
            item_query = query % item_escaped
            print(item_query)
            self.host.run_expect([0], f"sqlite3 /etc/maildb.sqlite3 \"{item_query}\"")

@pytest.fixture(scope="module")
def database(host, dbtype):
    return get_database(host, dbtype)

def get_database(host, dbtype):
    """
    Returns a database object we can load fixtures in
    """

    if dbtype == "pgsql":
        import testinfra.utils.ansible_runner
        inventory = testinfra.utils.ansible_runner.AnsibleRunner(
            os.environ["MOLECULE_INVENTORY_FILE"]
        )
        database_hosts = inventory.get_hosts("db")
        if len(database_hosts) != 1:
            raise ValueError("Multiple databases are not correctly suported")
        database_facts = inventory.run_module(database_hosts[0], "setup", [])
        database_ip = database_facts["ansible_facts"]["ansible_default_ipv4"]["address"]
        database = PostgresDatabase(database_ip, "mailserver", "pgadmin", "PGAdmin_Password")

    elif dbtype == "sqlite":
        database = SqliteDatabase(host)

    else:
        raise ValueError("Unkown dbtype")
    return database


@pytest.fixture(scope="module")
def server_address(host):
    """Get server address"""

    return host.interface("eth0").addresses[0]
