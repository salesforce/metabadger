# Metabadger

An AWS Security tool created to let you see your Instance Metadata usage and harden it to version 2 to prevent against known attack vectors that may leverage version 1.

[![continuous-integration](https://github.com/salesforce/metabadger/workflows/continuous-integration/badge.svg?)](https://github.com/salesforce/metabadger/actions?query=workflow%3Acontinuous-integration)

<p align="center">
  <img src="docs/images/metabadger.gif">
</p>

<!-- toc -->

# Metabadger

Purpose and functionality
* Diagnose and evaluate your current usage of the AWS Instance Metadata Service along with understanding how the service works
* Prepare you to upgrade to v2 of the Instance Metadata service to safeguard against v1 attack vectors
* Give you the ability to specifically update your instances to only use IMDSv2
* Give you the ability to disable the Instance Metadata service where you do not need it as a way to reduce attack surface

# What is the AWS Instance Metadata Service?

* The AWS metadata service essentially gives you access to all the things within an instance, including the instance role credential & session token
* Known XSRF vulnerabilities that exploit and use this attack as a pivot into your environment
* The famous attacks you have heard about, some of which involved this method of gaining access via a vulnerable web app with access to the instance metadata service
* Attacker could take said credentials from metadata service and use them outside of that particular instance 

# IMDSv2 and why it should be used

* Ensuring that instances are using V2 of the metadata service at all times by making it a requirement within it’s configuration
* Enabling session tokens with a PUT request with a mandatory request header to the AWS metadata API, IMDSv1 does not check for this making it easier for attackers to exploit the service
* X-Forwarded-For header is not allowed in IMDSv2 ensuring that no proxy based traffic is allowed to communicate with the metadata service

<!-- tocstop -->

<!-- requirements -->

# Requirements

Metabadger requires an IAM role or credentials with the following permission:

**ec2:ModifyInstanceAttribute**\
**ec2:DescribeInstances**

When making changes to the Instance Metadata service, you should be cautious and follow additional guidance from AWS on how to safely upgrade to version 2. Metabadger was designed to assist you with this process to further secure your compute infrastructure in AWS.

[AWS Best Practice Guide on Updating to IMDSv2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)


<!-- requirementsstop -->


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

```
Options:
  -j, --json          Get metadata summary in JSON format
  -r, --region TEXT   Specify which AWS region you will perform this command in
  -p, --profile TEXT  Specify the AWS IAM profile.
```

**discover-role-usage**

A summary of instances and the roles that they are using, this will give you a good idea of the caution you must take when making updates to the metadata service itself.

```
Options:
  -p, --profile TEXT  Specify the AWS IAM profile.
  -r, --region TEXT   Specify which AWS region you will perform this command in
```
**harden-metadata**

The ability to modify the instances to use either metadata v1 or v2 and to get an understanding of how many instances would be modified by running a dry run mode.

```
Options:
  -d, --dry-run          Dry run of hardening metadata changes
  -v1, --v1              Enforces v1 of the metadata service
  -i, --input-file PATH  Path of csv file of instances to harden IMDS for
  -t, --tags TEXT        A comma seperated list of tags to apply the hardening setting to
  -r, --region TEXT      Specify which AWS region you will perform this command in
  -p, --profile TEXT     Specify the AWS IAM profile.
```

**disable-metadata**

Use this command to completely disable the metadata servie on instances.

```
Options:
  -d, --dry-run          Dry run of disabling the metadata service
  -i, --input-file PATH  Path of csv file of instances to disable IMDS for
  -t, --tags TEXT        A comma seperated list of tags to apply the hardening setting to
  -r, --region TEXT      Specify which AWS region you will perform this command in
  -p, --profile TEXT     Specify the AWS IAM profile.
```
<!-- commandstop -->

