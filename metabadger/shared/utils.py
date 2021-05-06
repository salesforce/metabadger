""" Additional utils """
import csv
import pandas as pd
from colorama import Fore, Back
from tabulate import tabulate

OK_GREEN = "\033[92m"
GREY = "\33[90m"
END = "\033[0m"


def discover_instances(ec2: object):
    instances = ec2.instances.filter(
        Filters=[{"Name": "instance-state-name", "Values": ["running", "stopped"]}]
    )
    instance_list = []
    for instance in instances:
        instance_list.append(instance.id)
    return instance_list


def discover_roles(ec2_client: object):
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
        instance_role_summary[instance_id] = {
            "Instance_Name": instance_name,
            "Instance_Role": role_name,
        }
    short_summary = {"Role_Count": role_count, "Instance_Count": instance_count}
    return instance_role_summary, short_summary


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
    with open(file) as f:
        reader = csv.reader(f)
        data = list(reader)
    return data[0]


def pretty_metadata_summary(
    enabled_instances,
    disabled_instances,
    v1_enabled_instances,
    v2_enforced_instances,
    total_instances,
    percent_enforcement_v2,
):
    """Format metadata usage breakdown"""
    print(
        tabulate(
            [
                [
                    enabled_instances,
                    disabled_instances,
                    convert_red(v1_enabled_instances),
                    convert_green(v2_enforced_instances),
                    total_instances,
                    convert_green(percent_enforcement_v2),
                ]
            ],
            headers=[
                "IMDS Enabled",
                "IMDS Disabled",
                convert_red("V1 Available"),
                convert_green("V2 Enforced"),
                "Total Instances",
                convert_green("Enforcement Metric"),
            ],
            tablefmt="grid",
        )
    )
