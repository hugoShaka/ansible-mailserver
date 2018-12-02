# pytest configuration file

def pytest_addoption(parser):
    parser.addoption("--server", action="store", default="north.mail.local")

def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.server
    if 'server' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("server", [option_value], scope='session')
