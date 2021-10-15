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
