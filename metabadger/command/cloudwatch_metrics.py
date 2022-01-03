# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
"""Pull CloudWatch metrics for MetadataNoToken usage"""
import click
import time
from collections import Counter
from datetime import date, datetime, timedelta
from tabulate import tabulate
from metabadger.shared import utils, aws_auth, discover


@click.command(short_help="Pull CloudWatch Metrics for MetadataNoToken usage")
@click.option(
    "--all-region",
    "-a",
    is_flag=True,
    default=False,
    help="Pull CloudWatch metrics across all available regions",
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
    "--time-period",
    "-t",
    type=int,
    required=False,
    default="3600",
    help="The CloudWatch time period in seconds used to track the IMDS v1 metric",
)
@click.option(
    "--profile", "-p", type=str, required=False, help="Specify the AWS IAM profile."
)
def cloudwatch_metrics(profile: str, region: str, all_region: bool, time_period: int):
    last_hour_date_time = (datetime.utcnow() - timedelta(seconds=time_period))
    current_time = datetime.utcnow()
    cloudwatch_resource = aws_auth.get_boto3_resource(
        region=region, profile=profile, service="cloudwatch"
    )
    cloudwatch_client = aws_auth.get_boto3_client(
        region=region, profile=profile, service="cloudwatch"
    )
    ec2_client = aws_auth.get_boto3_client(
        region=region, profile=profile, service="ec2"
    )
    all_regions = aws_auth.get_available_regions("ec2")
    metric = cloudwatch_resource.Metric("AWS/EC2", "MetadataNoToken")
    metrics_summary = {}
    if all_region:
        utils.print_yellow("All region CloudWatch IMDS metrics being gathered")
        for region_iterate in all_regions:
            try:
                region_client = aws_auth.get_boto3_client(
                    region=region_iterate, profile=profile, service="ec2"
                )
                instances = discover.discover_instances(region_client)
                for instance in instances:
                    stats = metric.get_statistics(Dimensions=[
                        {
                            "Name": "InstanceId",
                            "Value": instance
                        }
                    ],
                    StartTime=last_hour_date_time, EndTime=current_time, Period=time_period, Statistics=["Sum"])
                    if stats["Datapoints"]:
                        if stats["Datapoints"][0]["Sum"] > 0:
                            api_count = (stats["Datapoints"][0]["Sum"])
                            instance_tags = discover.get_instance_tags(ec2_client, instance)
                            metrics_summary[instance] = {"instance_id": instance, "imdsv1_usage_count_last_hour":api_count, "instance_tags":instance_tags}
                if metrics_summary:
                    utils.pretty_grid_keys(metrics_summary)
            except Exception as e:
                utils.print_yellow(f"No IMDS metric information for {region_iterate}")
    else:
        instances = discover.discover_instances(ec2_client)
        for instance in instances:
            stats = metric.get_statistics(Dimensions=[
                {
                    "Name": "InstanceId",
                    "Value": instance
                }
            ],
            StartTime=last_hour_date_time, EndTime=current_time, Period=time_period, Statistics=["Sum"])
            try:
                if stats["Datapoints"]:
                    if stats["Datapoints"][0]["Sum"] > 0:
                        api_count = (stats["Datapoints"][0]["Sum"])
                        instance_tags = discover.get_instance_tags(ec2_client, instance)
                        metrics_summary[instance] = {"instance_id": instance, "imdsv1_usage_count_last_hour":api_count, "instance_tags":instance_tags}
            except:
                utils.print_red("No metrics available yet!")
        utils.pretty_grid_keys(metrics_summary)