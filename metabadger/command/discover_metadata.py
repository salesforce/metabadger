"""Discover EC2 Instance Metadata usage in your AWS account"""
import click
from tabulate import tabulate
from metabadger.shared import utils, aws_auth

ec2_resource = aws_auth.get_boto3_resource("ec2")
instance_list = utils.discover_instances(ec2_resource)


@click.command(short_help="Discover summary of IMDS service usage within EC2")
def discover_metadata():
    imds_enabled = 0
    imds_disabled = 0
    v1_available = 0
    v2_required = 0
    total_instances = 0
    for instance in instance_list:
        total_instances += 1
        instance = ec2_resource.Instance(instance)
        metadata_options = instance.metadata_options
        if metadata_options.get("HttpEndpoint") == "enabled":
            imds_enabled += 1
        if metadata_options.get("HttpEndpoint") == "disabled":
            imds_disabled += 1
        if metadata_options.get("HttpTokens") == "optional":
            v1_available += 1
        if metadata_options.get("HttpTokens") == "required":
            v2_required += 1
    enforcement = float(v2_required / total_instances) * 100
    percent_enforcement_v2 = f"{enforcement:.2f}"
    return utils.pretty_metadata_summary(
        imds_enabled,
        imds_disabled,
        v1_available,
        v2_required,
        total_instances,
        percent_enforcement_v2,
    )


# @click.option("--discover-metadata", "-dm", default=False, is_flag=True, help="Get metdata summary of all instances in condensed format")
