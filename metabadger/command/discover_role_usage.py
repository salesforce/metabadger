"""Discover IAM role usage which may conflict with altering IMDS"""
import click
from metabadger.shared import utils, aws_auth


@click.option(
    "--profile", "-p", type=str, required=False, help="Specify the AWS IAM profile."
)
@click.command(short_help="Discover summary of IAM role usage for EC2")
def discover_role_usage(profile: str):
    ec2_client = aws_auth.get_boto3_client(profile=profile, service="ec2")
    instance_role_summary = utils.discover_roles(ec2_client)[0]
    return utils.pretty_grid_keys(instance_role_summary)
