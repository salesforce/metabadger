# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
import json
import unittest
import warnings
from moto import mock_ec2, mock_sts, mock_iam
from click.testing import CliRunner
from metabadger.shared.discover import discover_roles, discover_instances, get_instance_tags
from metabadger.shared.aws_auth import get_boto3_resource
from metabadger.shared import aws_auth
import boto3
from test import EXAMPLE_AMI_ID
from test.helpers import quick_instance_creation, quick_instance_profile_creation, quick_associate_instance_profile


class DiscoverUtilsUnitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_sts = mock_sts()
        self.mock_iam = mock_iam()
        self.mock_ec2 = mock_ec2()
        self.mock_iam.start()
        self.mock_ec2.start()
        self.mock_sts.start()
        # Create instances
        self.instance_ids = []
        for _ in range(3):
            self.instance_ids.append(quick_instance_creation())
        print(self.instance_ids)
        self.instance_profile_arn, self.instance_profile_name = quick_instance_profile_creation(
            name="ExampleInstanceProfile", region="us-east-1"
        )
        print(self.instance_profile_arn)
        print(self.instance_profile_name)
        self.ec2_client = aws_auth.get_boto3_client(service="ec2", region="us-east-1", profile=None)

    def test_discover_instances(self):
        ec2_client = aws_auth.get_boto3_client(
            region="us-east-1", profile=None, service="ec2"
        )
        results = discover_instances(ec2_client)
        print(results)
        self.assertListEqual(results, self.instance_ids)

    def test_discover_role_usage(self):
        # instance_role_summary, short_summary = discover_roles(ec2_client=self.ec2_client)
        # self.assertEqual(short_summary["role_count"], 0)
        # self.assertEqual(short_summary["instance_count"], 3)
        # self.assertDictEqual(instance_role_summary, {})
        associations = quick_associate_instance_profile(
            instance_profile_arn=self.instance_profile_arn, instance_ids=self.instance_ids, instance_profile_name=self.instance_profile_name
        )
        print(json.dumps(associations, indent=4))
        instance_role_summary, short_summary = discover_roles(ec2_client=self.ec2_client)
        print(short_summary)
