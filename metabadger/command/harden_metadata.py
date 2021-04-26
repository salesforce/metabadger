"""Harden the AWS metadata service to your liking by upgrading to IMDSv2"""
import click
from tabulate import tabulate
from metabadger.shared import utils, aws_auth
from metabadger.command import discover_role_usage

ec2_client = aws_auth.get_boto3_client("ec2")
ec2_resource = aws_auth.get_boto3_resource("ec2")
instance_list = utils.discover_instances(ec2_resource)


@click.command(short_help="Harden the AWS instance metadata service from v1 to v2")
def harden_metadata():
    if utils.discover_roles(ec2_client)[1]["Role_Count"] > 0:
        click.confirm(
            utils.convert_red(
                f"Warning: One or more of the instances in {ec2_client.meta.region_name} you want to upgrade has a role attached, do you want to continue?"
            ),
            abort=True,
        )
    for instance in instance_list:
        try:
            response = ec2_client.modify_instance_metadata_options(
                InstanceId=instance, HttpTokens="required", HttpEndpoint="enabled"
            )
            status = utils.convert_green("SUCCESS")
        except:
            status = utils.convert_red("FAILED")
        print(f"IMDSv2 Enforced for {instance:<80} {status:>20}")


# @click.option("--imdsv2", "-v2", default=False, is_flag=True, help="Update any instances using IMDSv1 to IMDSv2")
