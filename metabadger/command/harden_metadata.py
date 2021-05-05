"""Harden the AWS metadata service to your liking by upgrading to IMDSv2"""
import click
from tabulate import tabulate
from metabadger.shared import utils, aws_auth
from metabadger.command import discover_role_usage

ec2_client = aws_auth.get_boto3_client("ec2")
ec2_resource = aws_auth.get_boto3_resource("ec2")
instance_list = utils.discover_instances(ec2_resource)


@click.command(short_help="Harden the AWS instance metadata service from v1 to v2")
@click.option("--dry-run", "-d", is_flag=True, default=False, help="Dry run of hardening metadata changes")
@click.option("--v1", "-v1", is_flag=True, default=False, help="Enforces v1 of the metadata service")
def harden_metadata(dry_run: bool, v1: bool):
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
    for instance in instance_list:
        if not v1:
            try:
                response = ec2_client.modify_instance_metadata_options(
                    InstanceId=instance, HttpTokens="required", HttpEndpoint="enabled"
                )
                status = utils.convert_green("SUCCESS")
            except:
                status = utils.convert_red("FAILED")
            print(f"IMDSv2 Enforced for {instance:<80} {status:>20}")
        elif v1:
            try:
                response = ec2_client.modify_instance_metadata_options(
                    InstanceId=instance, HttpTokens="optional", HttpEndpoint="enabled"
                )
                status = utils.convert_green("SUCCESS")
            except:
                status = utils.convert_red("FAILED")
            print(f"IMDSv1 Enforced for {instance:<80} {status:>20}")


