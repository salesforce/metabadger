"""Disable IMDS service on instances"""
import click
from tabulate import tabulate
from metabadger.shared import utils, aws_auth


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
@click.option(
    "--tags",
    "-t",
    "tags",
    type=str,
    default="",
    help="A comma seperated list of tags to apply the hardening setting to",
    callback=utils.click_validate_tag_alphanumeric,
)
@click.option(
    "--profile", "-p", type=str, required=False, help="Specify the AWS IAM profile."
)
def disable_metadata(dry_run: bool, input_file: str, tags: str, profile: str):
    ec2_resource = aws_auth.get_boto3_resource(profile=profile, service="ec2")
    ec2_client = aws_auth.get_boto3_client(profile=profile, service="ec2")
    instance_list = utils.discover_instances(ec2_resource)
    if utils.discover_roles(ec2_client)[1]["Role_Count"] > 0:
        click.confirm(
            utils.convert_red(
                f"Warning: One or more of the instances in {ec2_client.meta.region_name} you want to update has a role attached, do you want to continue?"
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
    elif tags:
        tag_apply_count = 0
        utils.print_yellow("Only applying hardening to the following tagged instances")
        print(f"Tags: {tags}")
        for instance in instance_list:
            if any(
                value in utils.get_instance_tags(ec2_client, instance) for value in tags
            ):
                utils.metamodify(
                    ec2_client, "disabled", "optional", "disabled", instance
                )
                tag_apply_count += 1
        if tag_apply_count < 1:
            print(f"No instances with this tag found, no changes were made")
    else:
        for instance in instance_list:
            utils.metamodify(ec2_client, "disabled", "optional", "disabled", instance)
