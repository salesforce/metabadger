# Metabadger

Prevent SSRF attacks on AWS EC2 via automated upgrades to the more secure Instance Metadata Service v2 (IMDSv2). 

[![continuous-integration](https://github.com/salesforce/metabadger/workflows/continuous-integration/badge.svg?)](https://github.com/salesforce/metabadger/actions?query=workflow%3Acontinuous-integration)
[![Downloads](https://pepy.tech/badge/metabadger)](https://pepy.tech/project/metabadger)


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

# Problem Statement

Engineering teams may have a vast variety of compute infrastructure in AWS that they need to protect from certain vulnerabilities that leverage the metadata service. The metadata service is required to run on instances if any IAM is used or if there is any user data information the instance might need when it boots. Limiting the attack surface of your instances is crucial in preventing the ability to pivot in your environment by stealing information provided by the service itself. Numerous famous attacks in the past have leveraged this particular service to exploit a role that is attached to the instance or dump sensitive data that is accessible via the metadata service. Metabadger can help to identify where and how you are using the instance metadata service while also giving you the ability to reduce any unwanted attack leverage to lower your overall risk posture while operating in EC2. 

# Disclaimer and Rollback

Using this tool may impact your AWS compute infrastructure as not all services and applications may work either without the metadata service or on version 2. Take caution when deploying this in your production environment and have a rollback plan in place incase something seems out of the ordinary. Metabadger comes built in with the ability to roll back to the default version 1 of the service using the -v1 flag, you can use this to quickly roll back your instances to use the default. Ideally, you should run this tool and update your metadata version in non-production environments as a proving grounds before applying it 

<!-- tocstop -->

<!-- steps -->

# Guided Steps for Hardening

**Step 1**

Initially, we want to discover our overall usage of the metadata service in a particular AWS region. Metabadger will evaluate the current status of your usage in the region where your credentials point to in your ```/.aws/credentials``` file or the current role that is assumed. You may also specify the ```--region``` flag when running the ```discover-metadata``` command if you would like to change to another region than what is currently configured. Once you have a good idea of which version your instances are running and if the service is enabled or disabled, you will be able to make a much more defined action plan for hardening the service.

**Step 2**

One of the areas that should be evaluated when making the switch to v2 of the service is the use of IAM roles. Metabadger lets you identify instances in a region that may already be using an IAM role. The ```discover-role-usage``` command will output a list of instances that have roles attached to them. If you have a lot of instances using roles, you should take precaution when updating the service to v2 to ensure the overall functionality of your workloads does not become impacted.

**Step 3**

Upon completion of doing your initial discovery and evaluation, you can now create a staged approach to hardening your compute infrastructure to use either v2 of the metadata service or disable it where it may not be used. The ```harden-metadata``` command allows you to update all instances in a particular region by default. You can also pass instance tags using the ```--tags``` flag or an input file containing a csv of instances that you would like to apply a configuration for. Once you have made the appropriate updates to v2 and disabled the service where it is not used you can re-evaluate using the items in Step 1 to confirm your environment is locked down. If you have certain instances that you don't want to update you can exlude them via the ```--exclusion``` flag by tag or instance id.


<!-- stepsstop -->

<!-- requirements -->

# Requirements

Metabadger requires an IAM role or credentials with the following permission:

**ec2:ModifyInstanceAttribute**\
**ec2:DescribeInstances**

When making changes to the Instance Metadata service, you should be cautious and follow additional guidance from AWS on how to safely upgrade to version 2. Metabadger was designed to assist you with this process to further secure your compute infrastructure in AWS.

[AWS Best Practice Guide on Updating to IMDSv2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html)

<!-- requirementsstop -->


## Usage & Installation

<!-- usage -->
**Install via pip**
```
pip3 install --user metabadger
```

**Install via Github**

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
  -e, --exclusion        The exclusion flag will apply to everything besides what is specified, tags or instances
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
  -e, --exclusion        The exclusion flag will apply to everything besides what is specified, tags or instances
  -d, --dry-run          Dry run of disabling the metadata service
  -i, --input-file PATH  Path of csv file of instances to disable IMDS for
  -t, --tags TEXT        A comma seperated list of tags to apply the hardening setting to
  -r, --region TEXT      Specify which AWS region you will perform this command in
  -p, --profile TEXT     Specify the AWS IAM profile.
```
<!-- commandstop -->

## Logging

<!-- logging -->

All changes made by Metabadger will be logged to a file saved in the working directory called ```metabadger.log```. The file will include the following for every action that the tool takes when it changes the metadata service:

* The time and date stamp for when a change was made
* Change that occured (disabled, hardened, or updated)
* The instance ID where the change was made
* Dry run information
* A status on if the change was successful or not

<!-- loggingstop -->

