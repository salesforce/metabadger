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
    print (f"Gathering EC2 metrics for {region}...")
    instance_list = discover.discover_instances(ec2_client)
    instance_tracker = []
    total_instances = 0
    if not instance_list:
        utils.print_yellow(f"No instances found in region: {region}")
    else:
        paginator = ec2_client.get_paginator("describe_instances")
        instances = paginator.paginate(PaginationConfig={"PageSize" : 1000}).build_full_result()
        with click.progressbar(
            instances["Reservations"], label=utils.convert_green("Calculating instance metadata summary...")
        ) as all_instances:
            for each_reservation in all_instances:
                time.sleep(.001)
                for each_instance in each_reservation["Instances"]:
                    instance_tracker.append((each_instance["MetadataOptions"]["State"]))
                    instance_tracker.append(
                        (each_instance["MetadataOptions"]["HttpTokens"])
                    )
                    instance_tracker.append(
                        (each_instance["MetadataOptions"]["HttpEndpoint"])
                    )
                    total_instances += 1
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
