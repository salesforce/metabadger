"""Discover EC2 Instance Metadata usage in your AWS account"""
import click
from tabulate import tabulate
from metabadger.shared import utils, aws_auth


@click.command(short_help="Discover summary of IMDS service usage within EC2")
@click.option(
    "--json",
    "-j",
    is_flag=True,
    default=False,
    help="Get metadata summary in JSON format",
)
@click.option(
    "--region",
    "-r",
    "region",
    type=str,
    required=False,
    default="us-west-2",
    help="Specify which AWS region you will perform this command in",
)
@click.option(
    "--profile", "-p", type=str, required=False, help="Specify the AWS IAM profile."
)
def discover_metadata(json, profile: str, region: str):
    ec2_resource = aws_auth.get_boto3_resource(
        region=region, profile=profile, service="ec2"
    )
    ec2_client = aws_auth.get_boto3_client(
        region=region, profile=profile, service="ec2"
    )
    instance_list = utils.discover_instances(ec2_resource)
    imds_enabled = 0
    imds_disabled = 0
    v1_available = 0
    v2_required = 0
    total_instances = 0
    if not instance_list:
        utils.print_yellow(f"No instances found in region: {region}")
    else:
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
        percent_enforcement_v2 = f"{enforcement:.2f}%"
        if not json:
            return utils.pretty_metadata_summary(
                imds_enabled,
                imds_disabled,
                v1_available,
                v2_required,
                total_instances,
                percent_enforcement_v2,
            )
        elif json:
            return utils.pretty_metadata_json(
                imds_enabled,
                imds_disabled,
                v1_available,
                v2_required,
                total_instances,
                percent_enforcement_v2,
            )
