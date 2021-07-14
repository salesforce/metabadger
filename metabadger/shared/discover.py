# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
import boto3
import click
from typing import Tuple


def discover_instances(ec2_client: boto3.Session.client) -> list:
    """Get a list of instances, both running and stopped"""
    paginator = ec2_client.get_paginator("describe_instances")
    instances = paginator.paginate().build_full_result()
    instance_list = []
    with click.progressbar(
            instances["Reservations"], label="Calculating all instances..."
        ) as all_instances:
            for each_reservation in all_instances:
                for each_instance in each_reservation["Instances"]:
                    instance_list.append(each_instance['InstanceId'])
    return instance_list


def discover_roles(ec2_client: boto3.Session.client) -> Tuple[dict, dict]:
    """Get a summary of roles attached to instances"""
    instances = ec2_client.describe_instances()
    role_count = 0
    instance_count = 0
    instance_role_summary = {}
    for ins_id in instances["Reservations"]:
        instance_id = ins_id["Instances"][0]["InstanceId"]
        instance_count += 1
        instance_name = None
        try:
            for tag in ins_id["Instances"][0]["Tags"]:
                if tag["Key"] == "Name":
                    instance_name = tag["Value"]
        except:
            instance_name = "N/A"
        try:
            role_name = ins_id["Instances"][0]["IamInstanceProfile"]["Arn"]
            role_count += 1
        except:
            role_name = "N/A"
        if role_name != "N/A":
            instance_role_summary[instance_id] = {
                "instance_name": instance_name,
                "instance_role": role_name,
            }
    short_summary = {"role_count": role_count, "instance_count": instance_count}
    return instance_role_summary, short_summary


def get_instance_tags(ec2_client: boto3.Session.client, instance_id: str):
    """Get instance tags to parse through for selective hardening"""
    tag_values = []
    tags = ec2_client.describe_tags(
        Filters=[
            {
                "Name": "resource-id",
                "Values": [
                    instance_id,
                ],
            },
        ],
    )["Tags"]
    for tag in tags:
        tag_values.append(tag["Value"])
    return tag_values
