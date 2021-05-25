"""Discover EC2 Instance Metadata usage in your AWS account"""
import click
from collections import Counter
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
    instance_tracker = []
    total_instances = 0
    if not instance_list:
        utils.print_yellow(f"No instances found in region: {region}")
    else:
        for instance in instance_list:
            total_instances += 1
            instance = ec2_resource.Instance(instance)
            metadata_options = instance.metadata_options
            instance_tracker.append(metadata_options.get("HttpEndpoint"))
            instance_tracker.append(metadata_options.get("HttpTokens"))
        instance_options = Counter(instance_tracker)
        instance_options["instances"] = total_instances
        enforcement = float(instance_options["required"] / total_instances) * 100
        if not json:
            instance_options["percent_enforcement_v2"] = utils.convert_green(
                f"{enforcement:.2f}%"
            )
            return utils.pretty_metadata_summary([dict(instance_options)])
        elif json:
            instance_options["percent_enforcement_v2"] = enforcement
            print(utils.pretty_json_summary(instance_options))
