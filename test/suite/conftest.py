# pytest configuration file


def pytest_addoption(parser):
    parser.addoption("--server", action="store", default="north.mail.local")
