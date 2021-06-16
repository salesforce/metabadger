from test.helpers import quick_instance_creation, quick_instance_profile_creation, quick_associate_instance_profile
import json
import boto3
import unittest
from moto import mock_ec2, mock_sts, mock_iam
from metabadger.shared.modify import Instance, Instances
from metabadger.shared import aws_auth


class ModifyUnitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_sts = mock_sts()
        self.mock_iam = mock_iam()
        self.mock_ec2 = mock_ec2()
        self.mock_iam.start()
        self.mock_ec2.start()
        self.mock_sts.start()
        # Create instances
        self.instance_ids = []
        region = "us-east-1"
        for _ in range(3):
            self.instance_ids.append(quick_instance_creation())
        print(self.instance_ids)
        self.instance_profile_arn, self.instance_profile_name = quick_instance_profile_creation(
            name="ExampleInstanceProfile", region=region
        )
        print(self.instance_profile_arn)
        print(self.instance_profile_name)
        self.ec2_client = aws_auth.get_boto3_client(service="ec2", region=region, profile=None)
        self.ec2_resource = aws_auth.get_boto3_resource(service="ec2", profile=None, region=region)
        self.instances = Instances(ec2_client=self.ec2_client, ec2_resource=self.ec2_resource)
        self.instance = self.instances[0]

    def test_instance(self):
        """Test method to check which instances have the endpoint enabled."""
        expected_result = self.instance.instance_id
        # We only expect the first instance to have it enabled and required
        self.instance.enable_endpoint()
        self.instance.set_endpoint_required()
        # Apply the changes set above
        self.instance.apply()
        results = self.instances.instances_v2_endpoint_enabled()
        # there should only be one instance in the result
        self.assertTrue(len(results), 1)
        # the instance ID should match
        self.assertEqual(results[0].instance_id, expected_result)

