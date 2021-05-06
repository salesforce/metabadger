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

**discover-metadata**

A summary of your overall instance metadata service usage including which version and an overall enforcement percentage. Using these numbers will help you understand the overall posture of how hardened your metadata usage is and where you're enforcing v2 vs v1.

**discover-role-usage**

A summary of instances and the roles that they are using, this will give you a good idea of the caution you must take when making updates to the metadata service itself.

**harden-metadata**

The ability to modify the instances to use either metadata v1 or v2 and to get an understanding of how many instances would be modified by running a dry run mode.

Options:
--input-file : Provide a csv formatted file containing a list of instances that you'd like to harden the metadata service on, to v2 
--dry-run : Setting this option will let you see 
--v1 : If you need to, you can supply this flag to revert instances to keep HttpTokens as optional letting you use v1

**disable-metadata**

Use this command to completely disable the metadata servie on instances.

Options:
--input-file : Provide a csv formatted file containing a list of instances that you'd like to disable the metadata service on
--dry-run : Setting this option will let you see 


