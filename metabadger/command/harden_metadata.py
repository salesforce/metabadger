# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
"""Harden the AWS metadata service to your liking by upgrading to IMDSv2"""
import click
from tabulate import tabulate
from metabadger.shared import utils, aws_auth, validate, discover, modify
from metabadger.command import discover_role_usage


@click.command(short_help="Harden the AWS instance metadata service from v1 to v2")
@click.option(
    "--all-region",
    "-a",
    is_flag=True,
    default=False,
    help="Update IMDS on all available regions in the AWS account",
)
@click.option(
    "--exclusion",
    "-e",
    is_flag=True,
    default=False,
    help="The exclusion flag will apply to everything besides what is specified, tags or instances",
)
@click.option(
    "--dry-run",
    "-d",
    is_flag=True,
    default=False,
    help="Dry run of hardening metadata changes",
)
@click.option(
    "--v1",
    "-v1",
    is_flag=True,
    default=False,
    help="Enforces v1 of the metadata service",
)
@click.option(
    "--input-file",
    "-i",
    type=click.Path(exists=True),
    required=False,
    help="Path of csv file of instances to harden IMDS for",
)
@click.option(
    "--tags",
    "-t",
    "tags",
    type=str,
    default="",
    help="A comma separated list of tags to apply the hardening setting to",
    callback=validate.click_validate_tag_alphanumeric,
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
def harden_metadata(
    dry_run: bool,
    v1: bool,
    input_file: str,
    tags: str,
    profile: str,
    region: str,
    exclusion: bool,
    all_region: bool,
):
    ec2_resource = aws_auth.get_boto3_resource(
        region=region, profile=profile, service="ec2"
    )
    ec2_client = aws_auth.get_boto3_client(
        region=region, profile=profile, service="ec2"
    )
    all_regions = aws_auth.get_available_regions("ec2")
    instance_list = discover.discover_instances(ec2_client)
    if discover.discover_roles(ec2_client)[1]["role_count"] > 0:
        click.confirm(
            utils.convert_red(
                f"Warning: One or more of the instances in {ec2_client.meta.region_name} you want to upgrade has a role attached, do you want to continue?"
            ),
            abort=True,
        )
    if discover.discover_roles(ec2_client)[1]["instance_count"] <= 0:
        utils.print_yellow(f"No EC2 instances found in region: {region}")
    if dry_run:
        utils.print_yellow(
            "Running in dry run mode, this will NOT make any changes to your metadata service"
        )
    if v1:
        message_default = "V1 Enforced"
        http_option = "optional"
    else:
        message_default = "V2 Enforced"
        http_option = "required"
    if exclusion and input_file:
        utils.print_yellow("Excluding instances specified in your configuration file")
        data = utils.read_from_csv(input_file)
        print(f"Reading instances from input csv file\n{data}")
        delta = [instance for instance in instance_list if instance not in data]
        for instance in delta:
            modify.metamodify(
                ec2_client,
                message_default,
                http_option,
                "enabled",
                instance,
                dry_run,
                region,
            )
    elif all_region and tags and exclusion:
        tag_apply_count = 0
        utils.print_yellow("All region IMDS hardening initiated")
        for region_iterate in all_regions:
            try:
                region_client = aws_auth.get_boto3_client(
                    region=region_iterate, profile=profile, service="ec2"
                )
                region_instance_list = discover.discover_instances(region_client)
                for instance in region_instance_list:
                    if not any(
                        value in discover.get_instance_tags(region_client, instance)
                        for value in tags
                    ):
                        modify.metamodify(
                            region_client,
                            message_default,
                            http_option,
                            "enabled",
                            instance,
                            dry_run,
                            region_iterate,
                        )
            except Exception as e:
                utils.print_yellow(f"No instance information for {region_iterate}")
            if tag_apply_count < 1:
                print(f"No instances with this tag found, no changes were made")
    elif exclusion and tags:
        utils.print_yellow("Excluding instances specified by tags")
        print(f"Tags: {tags}")
        for instance in instance_list:
            if not any(
                value in discover.get_instance_tags(ec2_client, instance)
                for value in tags
            ):
                modify.metamodify(
                    ec2_client,
                    message_default,
                    http_option,
                    "enabled",
                    instance,
                    dry_run,
                    region,
                )
    elif exclusion:
        utils.print_yellow("An exclusion requires either tags or instance list")
        raise click.Abort()
    elif input_file:
        data = utils.read_from_csv(input_file)
        print(f"Reading instances from input csv file\n{data}")
        for instance in data:
            modify.metamodify(
                ec2_client,
                message_default,
                http_option,
                "enabled",
                instance,
                dry_run,
                region,
            )
    elif all_region and tags:
        tag_apply_count = 0
        utils.print_yellow("All region IMDS hardening initiated")
        for region_iterate in all_regions:
            try:
                region_client = aws_auth.get_boto3_client(
                    region=region_iterate, profile=profile, service="ec2"
                )
                region_instance_list = discover.discover_instances(region_client)
                for instance in region_instance_list:
                    if any(
                        value in discover.get_instance_tags(region_client, instance)
                        for value in tags
                    ):
                        modify.metamodify(
                            region_client,
                            message_default,
                            http_option,
                            "enabled",
                            instance,
                            dry_run,
                            region_iterate,
                        )
            except Exception as e:
                utils.print_yellow(f"No instance information for {region_iterate}")
            if tag_apply_count < 1:
                print(f"No instances with this tag found, no changes were made")
    elif all_region:
        utils.print_yellow("All region IMDS hardening initiated")
        for region_iterate in all_regions:
            try:
                region_client = aws_auth.get_boto3_client(
                    region=region_iterate, profile=profile, service="ec2"
                )
                region_instance_list = discover.discover_instances(region_client)
                for instance in region_instance_list:
                    modify.metamodify(
                        region_client,
                        message_default,
                        http_option,
                        "enabled",
                        instance,
                        dry_run,
                        region_iterate,
                    )
            except Exception as e:
                utils.print_yellow(f"No instance information for {region_iterate}")
    elif tags:
        tag_apply_count = 0
        utils.print_yellow("Only applying hardening to the following tagged instances")
        print(f"Tags: {tags}")
        for instance in instance_list:
            if any(
                value in discover.get_instance_tags(ec2_client, instance)
                for value in tags
            ):
                tag_apply_count += 1
                modify.metamodify(
                    ec2_client,
                    message_default,
                    http_option,
                    "enabled",
                    instance,
                    dry_run,
                    region,
                )
        if tag_apply_count < 1:
            print(f"No instances with this tag found, no changes were made")
    else:
        for instance in instance_list:
            modify.metamodify(
                ec2_client,
                message_default,
                http_option,
                "enabled",
                instance,
                dry_run,
                region,
            )
