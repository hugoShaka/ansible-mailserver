from typing import List
import psycopg2

ADD_DOMAIN_QUERY = """INSERT INTO virtual_domains
                      VALUES (%s, %s)
                      ON CONFLICT DO NOTHING;"""

ADD_USER_QUERY = """INSERT INTO virtual_users (domain_id, password, email)
                    VALUES (%s, %s, %s)
                    ON CONFLICT DO NOTHING;"""


def insert_virtual_domains(server_address: str, domains: List):
    """Add domain fixtures into the database."""

    do_query(server_address, ADD_DOMAIN_QUERY, domains)


def insert_virtual_users(server_address: str, users: List):
    """Add users fixtures into the database."""

    do_query(server_address, ADD_USER_QUERY, users)


def do_query(server_address: str, query: str, items: List):
    """Opens a connection and executes a database query."""

    # TODO(shaka) gather password using testinfra and ansible info
    conn = psycopg2.connect(
        host=server_address,
        dbname="mailserver",
        user="pgadmin",
        password="ChangeMeAlso",
    )

    cur = conn.cursor()
    for item in items:
        cur.execute(query, item)
        conn.commit()
    cur.close()
