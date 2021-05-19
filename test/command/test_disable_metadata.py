import json
import unittest
import warnings
from moto import mock_ec2, mock_sts
from click.testing import CliRunner
from metabadger.command.disable_metadata import disable_metadata


class DisableMetadataClickUnitTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            self.mock = mock_ec2()
            self.mock.start()
            self.mock_sts = mock_sts()
            self.mock_sts.start()

    def test_disable_metadata_help(self):
        """ disable metadata will exit 0 """
        result = self.runner.invoke(disable_metadata, ["--help"])
        self.assertTrue(result.exit_code == 0)

    def test_disable_metadata_dry_run(self):
        """ command.disable_metadata: dry run"""
        dry_run_result = self.runner.invoke(
            disable_metadata, ["--dry-run"], input="y\n"
        )
        print(dry_run_result.output)
        self.assertTrue(dry_run_result.exit_code == 0)

    def test_disable_metadata_ec2(self):
        """ command.disable_metadata: no flags"""
        normal_result = self.runner.invoke(disable_metadata, input="y\n")
        print(normal_result.output)
        self.assertTrue(normal_result.exit_code == 0)
