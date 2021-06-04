import boto3
from metabadger.shared.utils import convert_red, convert_green


def metamodify(ec2_client: boto3.Session.client, action: str, httptoken: str, status: str, instance_id: str):
    """Helper function to change instance metadata status"""
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
