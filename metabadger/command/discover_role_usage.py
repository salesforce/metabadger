# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
"""Discover IAM role usage which may conflict with altering IMDS"""
import click
from metabadger.shared import utils, aws_auth, discover


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
    instance_role_summary = discover.discover_roles(ec2_client)[0]
    if not instance_role_summary:
        utils.print_yellow(f"No attached EC2 IAM roles found in region: {region}")
    else:
        return utils.pretty_grid_keys(instance_role_summary)
