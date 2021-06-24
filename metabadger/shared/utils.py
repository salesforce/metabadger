# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
""" Additional utils """
import csv
import json
import pandas as pd
from colorama import Fore, Back
from tabulate import tabulate

OK_GREEN = "\033[92m"
GREY = "\33[90m"
END = "\033[0m"


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
