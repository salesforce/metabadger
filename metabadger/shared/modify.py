import boto3
from metabadger.shared.utils import convert_red, convert_green, convert_yellow


def metamodify(
    ec2_client,
    action: str,
    httptoken: str,
    status: str,
    instance_id: str,
    dry_run: bool,
):
    """Helper function to change instance metadata status"""
    if dry_run:
        status = convert_yellow("SUCCESS")
        print(f"IMDS updated : {action} for {instance_id:<80} {status:>20}")
    else:
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

