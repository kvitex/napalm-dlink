"""Test fixtures."""
from builtins import super

import pytest
from napalm.base.test import conftest as parent_conftest

from napalm.base.test.double import BaseTestDouble

from napalm_dlink import dlink


@pytest.fixture(scope='class')
def set_device_parameters(request):
    """Set up the class."""
    def fin():
        request.cls.device.close()
    request.addfinalizer(fin)

    request.cls.driver = dlink.DlinkDriver
    request.cls.patched_driver = PatchedDlinkDriver
    request.cls.vendor = 'dlink'
    parent_conftest.set_device_parameters(request)


def pytest_generate_tests(metafunc):
    """Generate test cases dynamically."""
    parent_conftest.pytest_generate_tests(metafunc, __file__)


class PatchedDlinkDriver(dlink.DlinkDriver):
    """Patched Dlink Driver."""

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """Patched Dlink Driver constructor."""
        super().__init__(hostname, username, password, timeout, optional_args)

        self.patched_attrs = ['device']
        self.device = FakeDlinkDevice()


class FakeDlinkDevice(BaseTestDouble):
    """Dlink device test double."""

    def run_commands(self, command_list, encoding='json'):
        """Fake run_commands."""
        result = list()

        for command in command_list:
            filename = '{}.{}'.format(self.sanitize_text(command), encoding)
            full_path = self.find_file(filename)

            if encoding == 'json':
                result.append(self.read_json_file(full_path))
            else:
                result.append({'output': self.read_txt_file(full_path)})

        return result
