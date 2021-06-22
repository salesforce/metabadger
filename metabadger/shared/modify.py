import boto3
import logging
from metabadger.shared.utils import convert_red, convert_green, convert_yellow


def metamodify(
    ec2_client: boto3.Session.client,
    action: str,
    httptoken: str,
    status: str,
    instance_id: str,
    dry_run: bool,
):
    """Helper function to change instance metadata status"""
    logging.basicConfig(filename='metabadger.log', format='%(asctime)s,%(message)s', level=logging.INFO, datefmt="%Y-%m-%dT%H:%M:%S")
    if dry_run:
        status_color = convert_yellow("SUCCESS")
        status_text = "SUCCESS"
        print(f"IMDS updated (Dry run mode) : {action} for {instance_id:<80} {status_color:>20}")
        logging.info(f"imds_updated_dry_run,{action},{instance_id},{status_text}")
    else:
        try:
            response = ec2_client.modify_instance_metadata_options(
                InstanceId=instance_id,
                HttpTokens=httptoken,
                HttpEndpoint=status,
            )
            status_color = convert_green("SUCCESS")
            status_text = "SUCCESS"
        except:
            status_color = convert_red("FAILED")
            status_text = "FAILED"
        print(f"IMDS updated : {action} for {instance_id:<80} {status_color:>20}")
        logging.info(f"imds_updated,{action},{instance_id},{status_text}")
