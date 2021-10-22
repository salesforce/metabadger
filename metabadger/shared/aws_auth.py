# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
""" AWS auth functions from https://github.com/salesforce/cloudsplaining/blob/master/cloudsplaining/shared/aws_login.py """
import os
import logging
import boto3
import sys
from botocore.config import Config
from metabadger.shared import utils

logger = logging.getLogger(__name__)


def get_boto3_client(
    service: str, profile: str = None, region: str = "us-west-2"
) -> boto3.Session.client:
    """Get a boto3 client for a given service"""
    logging.getLogger("botocore").setLevel(logging.CRITICAL)
    session_data = {"region_name": region}
    if profile:
        session_data["profile_name"] = profile
    session = boto3.Session(**session_data)
    if region not in get_available_regions(service):
        utils.print_red(f"The service {service} is not available in this region!")
        sys.exit()
    config = Config(read_timeout=5, connect_timeout=5, retries={"max_attempts": 10})
    if os.environ.get("LOCALSTACK_ENDPOINT_URL"):
        client = session.client(
            service,
            config=config,
            endpoint_url=os.environ.get("LOCALSTACK_ENDPOINT_URL"),
        )
    else:
        client = session.client(service, config=config)
    # Uncomment if you are having trouble with authing across a particular region :)
    # utils.print_green(f"Authentication to {service} in {region} was successful!")
    logger.debug(
        f"{client.meta.endpoint_url} in {client.meta.region_name}: boto3 client login successful"
    )
    return client


def get_boto3_resource(
    service: str, profile: str = None, region: str = "us-west-2"
) -> boto3.Session.resource:
    """Get a boto3 resource for a given service"""
    logging.getLogger("botocore").setLevel(logging.CRITICAL)
    session_data = {"region_name": region}
    if profile:
        session_data["profile_name"] = profile
    session = boto3.Session(**session_data)

    resource = session.resource(service)
    return resource


def get_current_account_id(sts_client: boto3.Session.client) -> str:
    """Get the current account ID"""
    response = sts_client.get_caller_identity()
    current_account_id = response.get("Account")
    return current_account_id


def get_available_regions(service: str):
    """AWS exposes their list of regions as an API. Gather the list."""
    regions = boto3.session.Session().get_available_regions(service)
    logger.debug(
        "The service %s does not have available regions. Returning us-west-2 as default"
    )
    if not regions:
        regions = ["us-west-2"]
    return regions
