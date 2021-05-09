"""Disable IMDS service on instances"""
import click
from tabulate import tabulate
from metabadger.shared import utils, aws_auth

ec2_resource = aws_auth.get_boto3_resource("ec2")
ec2_client = aws_auth.get_boto3_client("ec2")
instance_list = utils.discover_instances(ec2_resource)


@click.command(short_help="Disable the IMDS service on EC2 instances")
@click.option(
    "--dry-run",
    "-d",
    is_flag=True,
    default=False,
    help="Dry run of disabling the metadata service",
)
@click.option(
    "--input-file",
    "-i",
    type=click.Path(exists=True),
    required=False,
    help="Path of csv file of instances to disable IMDS for",
)
def disable_metadata(dry_run: bool, input_file):
    if utils.discover_roles(ec2_client)[1]["Role_Count"] > 0:
        click.confirm(
            utils.convert_red(
                f"Warning: One or more of the instances in {ec2_client.meta.region_name} is currently using IMDS, do you want to continue?"
            ),
            abort=True,
        )
    if input_file:
        data = utils.read_from_csv(input_file)
        print(f"Reading instances from input csv file\n{data}")
        for instance in data:
            utils.metamodify(ec2_client, "disabled", "optional", "disabled", instance)
    elif dry_run:
        utils.print_yellow(
            "Running in dry run mode, this will NOT make any changes to your metadata service"
        )
        for instance in instance_list:
            status = utils.convert_yellow("SUCCESS")
            print(f"IMDS Disabled for {instance:<80} {status:>22}")
    else:
        for instance in instance_list:
            utils.metamodify(ec2_client, "disabled", "optional", "disabled", instance)
