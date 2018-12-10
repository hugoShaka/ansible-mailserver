import dns.resolver
import os

# pytest configuration file


def pytest_addoption(parser):
    parser.addoption("--server", action="store", default="north.mail.local")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".

    if "MOLECULE_INVENTORY_FILE" in os.environ:
        import testinfra.utils.ansible_runner
        inventory = testinfra.utils.ansible_runner.AnsibleRunner(
            os.environ["MOLECULE_INVENTORY_FILE"]
        )
        dns_facts = inventory.run("ns", "setup")
        dns_ip = dns_facts["ansible_facts"]["ansible_default_ipv4"]["address"]

        test_resolver = dns.resolver.Resolver()
        test_resolver.nameservers = [dns_ip]
        answers = test_resolver.query("north.mail.local", "A")

        north_ip = answers[0].address
        metafunc.parametrize("server_address", [north_ip], scope="session")

    else:
        option_value = metafunc.config.option.server
        if "server" in metafunc.fixturenames and option_value is not None:
            metafunc.parametrize("server_address", [option_value], scope="session")
