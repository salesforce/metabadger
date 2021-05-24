"""Discover IAM role usage which may conflict with altering IMDS"""
import click
from metabadger.shared import utils, aws_auth


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
@click.command(short_help="Discover summary of IAM role usage for EC2")
def discover_role_usage(profile: str, region: str):
    ec2_client = aws_auth.get_boto3_client(
        region=region, profile=profile, service="ec2"
    )
    instance_role_summary = utils.discover_roles(ec2_client)[0]
    if not instance_role_summary:
        utils.print_yellow(f"No attached EC2 IAM roles found in region: {region}")
    else:
        return utils.pretty_grid_keys(instance_role_summary)
