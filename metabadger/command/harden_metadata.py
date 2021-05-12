"""Harden the AWS metadata service to your liking by upgrading to IMDSv2"""
import click
from tabulate import tabulate
from metabadger.shared import utils, aws_auth
from metabadger.command import discover_role_usage

ec2_client = aws_auth.get_boto3_client("ec2")
ec2_resource = aws_auth.get_boto3_resource("ec2")
instance_list = utils.discover_instances(ec2_resource)


@click.command(short_help="Harden the AWS instance metadata service from v1 to v2")
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
    help="A comma seperated list of tags to apply the hardening setting to",
    callback=utils.click_validate_tag_alphanumeric,
)
def harden_metadata(dry_run: bool, v1: bool, input_file, tags):
    if utils.discover_roles(ec2_client)[1]["Role_Count"] > 0:
        click.confirm(
            utils.convert_red(
                f"Warning: One or more of the instances in {ec2_client.meta.region_name} you want to upgrade has a role attached, do you want to continue?"
            ),
            abort=True,
        )
    if dry_run:
        utils.print_yellow(
            "Running in dry run mode, this will NOT make any changes to your metadata service"
        )
        for instance in instance_list:
            status = utils.convert_yellow("SUCCESS")
            print(f"IMDS hardened to v2 for {instance:<80} {status:>22}")
    elif input_file:
        data = utils.read_from_csv(input_file)
        print(f"Reading instances from input csv file\n{data}")
        for instance in data:
            utils.metamodify(ec2_client, "V2 Enforced", "required", "enabled", instance)
    elif tags:
        tag_apply_count = 0
        utils.print_yellow("Only applying hardening to the following tagged instances")
        print(f"Tags: {tags}")
        for instance in instance_list:
            if any(
                value in utils.get_instance_tags(ec2_client, instance) for value in tags
            ):
                utils.metamodify(
                    ec2_client, "V2 Enforced", "required", "enabled", instance
                )
                tag_apply_count += 1
        if tag_apply_count < 1:
            print(f"No instances with this tag found, no changes were made")
    elif not input_file:
        for instance in instance_list:
            if not v1:
                utils.metamodify(
                    ec2_client, "V2 Enforced", "required", "enabled", instance
                )
            elif v1:
                utils.metamodify(
                    ec2_client, "V1 Default Set", "optional", "enabled", instance
                )
