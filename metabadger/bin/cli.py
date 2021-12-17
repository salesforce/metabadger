#! /usr/bin/env python
# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
"""
    Metabadger is an AWS Security Tool used for discovering and hardening the Instance Metadata service.
"""
import click
from metabadger import command
from metabadger.bin.version import __version__


@click.group()
@click.version_option(version=__version__)
def metabadger():
    """
    Metabadger is an AWS Security Tool used for discovering and hardening the Instance Metadata service.
    """


metabadger.add_command(command.disable_metadata.disable_metadata)
metabadger.add_command(command.discover_metadata.discover_metadata)
metabadger.add_command(command.discover_role_usage.discover_role_usage)
metabadger.add_command(command.harden_metadata.harden_metadata)
metabadger.add_command(command.cloudwatch_metrics.cloudwatch_metrics)


def main():
    """ Metabadger is an AWS Security Tool used for discovering and hardening the Instance Metadata service. """
    metabadger()


if __name__ == "__main__":
    metabadger()
