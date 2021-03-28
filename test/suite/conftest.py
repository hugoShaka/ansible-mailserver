def pytest_addoption(parser):
    parser.addoption("--dbtype", action="store", default="pgsql")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.dbtype
    if 'dbtype' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("dbtype", [option_value], scope="session")
