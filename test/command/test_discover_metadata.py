# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
import json
import unittest
import warnings
from moto import mock_ec2, mock_sts
from click.testing import CliRunner
from metabadger.command.discover_metadata import discover_metadata


class DiscoverMetadataClickUnitTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            self.mock = mock_ec2()
            self.mock.start()
            self.mock_sts = mock_sts()
            self.mock_sts.start()

    def test_discover_metadata_help(self):
        """ discover metadata will exit 0 """
        result = self.runner.invoke(discover_metadata, ["--help"])
        self.assertTrue(result.exit_code == 0)

    def test_discover_metadata_ec2(self):
        """ command.discover_metadata: no flags"""
        normal_result = self.runner.invoke(discover_metadata)
        print(normal_result.output)
        self.assertTrue(normal_result.exit_code == 0)
