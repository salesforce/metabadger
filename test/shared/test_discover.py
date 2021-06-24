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


def quick_instance_creation(region: str = "us-east-1"):
    conn_ec2 = boto3.resource("ec2", region)
    test_instance = conn_ec2.create_instances(
        ImageId=EXAMPLE_AMI_ID, MinCount=1, MaxCount=1
    )
    # We only need instance id for this tests
    return test_instance[0].id


def quick_instance_profile_creation(name: str, region: str = "us-east-1"):
    conn_iam = boto3.resource("iam", region)
    test_instance_profile = conn_iam.create_instance_profile(
        InstanceProfileName=name, Path="/"
    )
    return test_instance_profile.arn, test_instance_profile.name


def quick_associate_instance_profile(instance_profile_arn: str, instance_profile_name: str, instance_ids: list, region: str = "us-east-1"):
    client = boto3.client("ec2", region_name="us-east-1")
    for instance_id in instance_ids:
        client.associate_iam_instance_profile(
            IamInstanceProfile={
                "Arn": instance_profile_arn,
                "Name": instance_profile_name,
            },
            InstanceId=instance_id,
        )
    associations = client.describe_iam_instance_profile_associations()
    return associations


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
        ec2_resource = aws_auth.get_boto3_resource(
            region="us-east-1", profile=None, service="ec2"
        )
        results = discover_instances(ec2_resource)
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
