# Metabadger

An AWS Security tool created to let you see your Instance Metadata usage and harden it to version 2 to prevent against known attack vectors that may leverage version 1.

<!-- toc -->

# Metabadger

Purpose and functionality
* Diagnose and evaluate your current usage of the AWS Instance Metadata Service along with understanding how the service works
* Prepare you to upgrade to v2 of the Instance Metadata service to safeguard against v1 attack vectors
* Give you the ability to specifically update your instances to only use IMDSv2
* Give you the ability to disable the Instance Metadata service where you do not need it as a way to reduce attack surface

<!-- tocstop -->

## Usage

<!-- usage -->
```sh-session
$ git clone https://github.com/salesforce/metabadger
$ cd metabadger
$ pip install -e .

$ metabadger
Usage: metabadger [OPTIONS] COMMAND [ARGS]...

  Metabadger is an AWS Security Tool used for discovering and hardening the
  Instance Metadata service.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  disable-metadata     Disable the IMDS service on EC2 instances
  discover-metadata    Discover summary of IMDS service usage within EC2
  discover-role-usage  Discover summary of IAM role usage for EC2
  harden-metadata      Harden the AWS instance metadata service from v1 to v2
```
<!-- usagestop -->
## Commands
<!-- commands -->

TO DO