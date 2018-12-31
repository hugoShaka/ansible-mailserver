CREATE TABLE IF NOT EXISTS virtual_domains (
  id SERIAL,
  name varchar(50) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS virtual_alias_domains (
  id SERIAL,
  source varchar(50) NOT NULL,
  destination varchar(50) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (source)
);

CREATE TABLE IF NOT EXISTS virtual_users (
  id SERIAL,
  domain_id integer NOT NULL,
  password varchar(150) NOT NULL,
  email varchar(100) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (email),
  FOREIGN KEY (domain_id) REFERENCES virtual_domains(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS virtual_aliases (
  id SERIAL,
  domain_id integer NOT NULL,
  source varchar(100) NOT NULL,
  destination varchar(100) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (domain_id) REFERENCES virtual_domains(id) ON DELETE CASCADE
);
