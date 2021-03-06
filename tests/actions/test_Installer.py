import unittest

from os import path
from tests.util.TestingUtils import TestingUtils
from xl_helper.actions.Installer import Installer
from xl_helper.artifacts.Cache import Cache
from xl_helper.artifacts.server.LocalServerDist import LocalServerDist
from xl_helper.artifacts.server.RemoteServerDist import RemoteServerDist
from tests.util.TestWithTempDirs import TestWithTempDirs


class InstallerTest(TestWithTempDirs):

    def setUp(self):
        self.installer = Installer(self.test_config)
        self.temp_dir = self.create_temp_dir()
        self.cache = Cache(self.test_config)

    def test_install_server_from_local_zip(self):
        remote_dist_zip = self.cache.get(RemoteServerDist("4.0.1", self.test_config))
        home = self.installer.server(LocalServerDist(path.join(self.temp_dir, remote_dist_zip)), target=self.temp_dir)
        TestingUtils.assert_valid_server_installation(home)

    def test_install_server_existing_path(self):
        home = self.installer.server(RemoteServerDist('4.0.0', self.test_config), target=self.temp_dir)
        assert home.endswith('xl-deploy-4.0.0-server')
        TestingUtils.assert_valid_server_installation(home)

    def test_install_plugin(self):
        home = self.installer.server(RemoteServerDist('3.9.2', self.test_config), target=self.temp_dir)
        assert not path.isfile(path.join(home, 'plugins/jbossas-plugin-3.9.0.jar'))
        self.installer.plugin(name='jbossas', version='3.9.0', server_location=home)
        assert path.isfile(path.join(home, 'plugins/jbossas-plugin-3.9.0.jar'))

    def test_install_cli(self):
        home = self.installer.cli("3.9.4", self.create_temp_dir())
        TestingUtils.assert_valid_cli_home(home)


if __name__ == '__main__':
    unittest.main()