# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
"""Discover EC2 Instance Metadata usage in your AWS account"""
import click
import time
from collections import Counter
from tabulate import tabulate
from metabadger.shared import utils, aws_auth, discover


@click.command(short_help="Discover summary of IMDS service usage within EC2")
@click.option(
    "--all-region",
    "-a",
    is_flag=True,
    default=False,
    help="Provide a metadata summary for all available regions in the AWS account",
)
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
def discover_metadata(json, profile: str, region: str, all_region):
    ec2_resource = aws_auth.get_boto3_resource(
        region=region, profile=profile, service="ec2"
    )
    ec2_client = aws_auth.get_boto3_client(
        region=region, profile=profile, service="ec2"
    )
    all_regions = aws_auth.get_available_regions("ec2")
    if all_region:
        instance_total_options = []
        utils.print_green(
            f"All region scan initiated: Iterating through each of the following regions {utils.convert_yellow(all_regions)}"
        )
        for each_region in all_regions:
            try:
                instance_total_options.append(
                    discover.get_summary(
                        aws_auth.get_boto3_client(
                            region=each_region, profile=profile, service="ec2"
                        )
                    )
                )
            except Exception as e:
                utils.print_yellow(f"No instance information for {each_region}")
        instance_all_region_total = sum(instance_total_options, Counter())
        if instance_all_region_total["instances"] == 0:
            utils.print_red(f"No instances found in your AWS account")
        else:
            enforcement = (
                float(
                    instance_all_region_total["required"]
                    / instance_all_region_total["instances"]
                )
                * 100
            )
            if not json:
                instance_all_region_total[
                    "percent_enforcement_v2"
                ] = utils.convert_green(f"{enforcement:.2f}%")
                return utils.pretty_metadata_summary([dict(instance_all_region_total)])
            elif json:
                instance_all_region_total["percent_enforcement_v2"] = enforcement
                print(utils.pretty_json_summary(instance_all_region_total))
    else:
        instance_list = discover.discover_instances(ec2_client)
        if not instance_list:
            utils.print_yellow(f"No instances found in region: {region}")
        else:
            print(f"Gathering EC2 metrics for {region}...")
            instance_options = discover.get_summary(ec2_client)
            enforcement = (
                float(instance_options["required"] / instance_options["instances"])
                * 100
            )
            if not json:
                instance_options["percent_enforcement_v2"] = utils.convert_green(
                    f"{enforcement:.2f}%"
                )
                return utils.pretty_metadata_summary([dict(instance_options)])
            elif json:
                instance_options["percent_enforcement_v2"] = enforcement
                print(utils.pretty_json_summary(instance_options))
