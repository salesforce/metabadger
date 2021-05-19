import json
import unittest
import warnings
from moto import mock_ec2, mock_sts
from click.testing import CliRunner
from metabadger.command.harden_metadata import harden_metadata


class HardenMetadataClickUnitTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            self.mock = mock_ec2()
            self.mock.start()
            self.mock_sts = mock_sts()
            self.mock_sts.start()

    def test_harden_metadata_help(self):
        """ harden metadata will exit 0 """
        result = self.runner.invoke(harden_metadata, ["--help"])
        self.assertTrue(result.exit_code == 0)

    def test_harden_metadata_dry_run(self):
        """ command.harden_metadata: dry run"""
        dry_run_result = self.runner.invoke(harden_metadata, ["--dry-run"], input="y\n")
        print(dry_run_result.output)
        self.assertTrue(dry_run_result.exit_code == 0)

    def test_harden_metadata_ec2(self):
        """ command.harden_metadata: no flags"""
        normal_result = self.runner.invoke(harden_metadata, input="y\n")
        print(normal_result.output)
        self.assertTrue(normal_result.exit_code == 0)
