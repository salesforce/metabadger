"""Discover IAM role usage which may conflict with altering IMDS"""
import click
from metabadger.shared import utils, aws_auth

ec2_client = aws_auth.get_boto3_client("ec2")


@click.command(short_help="Discover summary of IAM role usage for EC2")
def discover_role_usage():
    instance_role_summary = utils.discover_roles(ec2_client)[0]
    return utils.pretty_grid_keys(instance_role_summary)
