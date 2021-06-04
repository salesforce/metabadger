""" Additional utils """
import csv
import click
import json
import boto3
import pandas as pd
from colorama import Fore, Back
from tabulate import tabulate

OK_GREEN = "\033[92m"
GREY = "\33[90m"
END = "\033[0m"


def metamodify(ec2_client: boto3.Session.client, action: str, httptoken: str, status: str, instance_id: str):
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
