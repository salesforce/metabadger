""" Additional utils """
import csv
import click
import json
import pandas as pd
from colorama import Fore, Back
from tabulate import tabulate

OK_GREEN = "\033[92m"
GREY = "\33[90m"
END = "\033[0m"


def discover_instances(ec2: object):
    """Get a list of instances, both running and stopped"""
    instances = ec2.instances.filter(
        Filters=[{"Name": "instance-state-name", "Values": ["running", "stopped"]}]
    )
    instance_list = []
    for instance in instances:
        instance_list.append(instance.id)
    return instance_list


def metamodify(ec2_client, action: str, httptoken: str, status: str, instance_id: str):
    """Helper function to change instance metadata status"""
    try:
        response = ec2_client.modify_instance_metadata_options(
            InstanceId=instance_id,
            HttpTokens=httptoken,
            HttpEndpoint=status,
        )
        status = convert_green("SUCCESS")
    except:
        status = convert_red("FAILED")
    print(f"IMDS updated : {action} for {instance_id:<80} {status:>20}")


def discover_roles(ec2_client: object):
    """Get a summary of roles attached to instances"""
    instances = ec2_client.describe_instances()
    role_count = 0
    instance_count = 0
    instance_role_summary = {}
    for ins_id in instances["Reservations"]:
        instance_id = ins_id["Instances"][0]["InstanceId"]
        instance_count += 1
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


def get_instance_tags(ec2_client: object, instance_id: str):
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


def click_validate_tag_alphanumeric(ctx, param, value):
    if value is not None:
        try:
            if value == "":
                return []
            else:
                tag_values_to_check = value.split(",")
                return tag_values_to_check
        except ValueError:
            raise click.BadParameter(
                "Supply the list of tag names to include for hardening in a comma separated string."
            )


def print_yellow(string):
    """Print yellow text"""
    print(f"{Fore.YELLOW}{string}{END}")


def print_green(string):
    """Print green text"""
    print(f"{Fore.GREEN}{string}{END}")


def print_grey(string):
    """Print grey text"""
    print(f"{Fore.GREY}{string}{END}")


def print_red(string):
    """Print red text"""
    print(f"{Fore.RED}{string}{END}")


def convert_red(string):
    """Return red text"""
    return f"{Fore.RED}{string}{END}"


def convert_green(string):
    """Return green text"""
    return f"{Fore.GREEN}{string}{END}"


def convert_yellow(string):
    """Return green text"""
    return f"{Fore.YELLOW}{string}{END}"


def pretty_grid_keys(output: dict):
    """Print grid keys from dictionary"""
    df = pd.DataFrame(output)
    print(tabulate(df.T, headers="keys", tablefmt="grid"))


def read_from_csv(file):
    """Read file from a path and covert the csv into a list"""
    with open(file) as f:
        reader = csv.reader(f)
        data = list(reader)
    return data[0]


def pretty_metadata_summary(instance_options):
    """Format metadata usage breakdown"""
    print(tabulate(instance_options, headers="keys", tablefmt="grid"))


def pretty_json_summary(instance_dict):
    """Format metadata usage summary into JSON"""
    print(json.dumps(instance_dict, indent=4, sort_keys=True))
