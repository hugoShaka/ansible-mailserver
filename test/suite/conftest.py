# pytest configuration file

def pytest_addoption(parser):
    parser.addoption("--primary", action="store", default="north.mail.local")
    parser.addoption("--secondary", action="store", default="south.mail.local")

def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    options = ["primary", "secondary"]
    for option in options:
        option_value = getattr(metafunc.config.option, option)
        if option in metafunc.fixturenames and option_value is not None:
            metafunc.parametrize(option, [option_value])
