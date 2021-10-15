import boto3
from metabadger.shared.utils import convert_red, convert_green, convert_yellow
from metabadger.shared.discover import discover_instances


class Instances:
    def __init__(self, ec2_client: boto3.Session.client):
        # self.ec2_resource = ec2_resource
        self.ec2_client = ec2_client
        self.ec2_resource = boto3.resource('ec2')
        self.http_tokens = None
        self.http_endpoint = None
        self.instances = self._set_instance_data()

    def instance_ids(self):
        return discover_instances(ec2_client=self.ec2_client)

    def _set_instance_data(self):
        instance_list = []
        for instance_id in self.instance_ids():
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#instance
            some_instance = self.ec2_resource.Instance(instance_id)

            if isinstance(some_instance.iam_instance_profile, type(None)):
                instance_profile = None
            else:
                instance_profile = some_instance.iam_instance_profile.get("Arn")
            if isinstance(some_instance.metadata_options, type(None)):
                http_tokens = "optional"
                http_endpoint = "disabled"
            else:
                http_tokens = some_instance.metadata_options.get("HttpTokens")
                http_endpoint = some_instance.metadata_options.get("HttpEndpoint")

            instance = Instance(
                ec2_client=self.ec2_client, instance_id=some_instance.id,
                http_tokens=http_tokens,
                http_endpoint=http_endpoint,
                instance_profile=instance_profile
            )
            instance_list.append(instance)
        return instance_list

    def __getitem__(self, number: int):
        return self.instances[number]

    def set_endpoint_optional(self):
        self.http_tokens = "optional"

    def set_endpoint_required(self):
        self.http_tokens = "required"

    def enable_endpoint(self):
        self.http_endpoint = "enabled"

    def disable_endpoint(self):
        self.http_endpoint = "disabled"

    def apply(self, dry_run: bool = False):
        # TODO: Handle tags case
        if not self.http_tokens or not self.http_endpoint:
            raise Exception("Make sure you set the http_tokens to optional/required and the http_endpoint to enabled/disabled")
        for instance in self.instances:
            instance.http_endpoint = self.http_endpoint
            instance.http_tokens = self.http_tokens
            instance.apply(dry_run=dry_run)

    def instances_v2_endpoint_enabled(self):
        results = []
        for instance in self.instances:
            if instance.http_endpoint == "enabled":
                results.append(instance)
        return results

    def instances_v2_endpoint_required(self):
        results = []
        for instance in self.instances:
            if instance.http_endpoint == "required":
                results.append(instance)
        return results

    # def instances_with_tags(self, tags: str):



class Instance:
    def __init__(self, ec2_client: boto3.Session.client, instance_id: str, http_tokens: str, http_endpoint: str, instance_profile: str = None):
        self.ec2_client = ec2_client
        self.instance_id = instance_id
        if http_endpoint not in ["enabled", "disabled"]:
            raise Exception("http_endpoint must be one of: 'enabled', 'disabled'")
        if http_tokens not in ["optional", "required"]:
            raise Exception("http_tokens must be one of: 'optional', 'required'")

        self.http_tokens = http_tokens
        self.http_endpoint = http_endpoint
        self.instance_profile = instance_profile

    def get_instance_tags(self, ec2_client: boto3.Session.client):
        tag_values = []
        tags = ec2_client.describe_tags(
            Filters=[
                {
                    "Name": "resource-id",
                    "Values": [
                        self.instance_id,
                    ],
                },
            ],
        )["Tags"]
        for tag in tags:
            tag_values.append(tag["Value"])
        return tag_values

    def has_instance_tag(self, ec2_client: boto3.Session.client, tags: str):
        if any(
                value in self.get_instance_tags(ec2_client=ec2_client) for value in tags
        ):
            return True
        else:
            return False

    def set_endpoint_optional(self):
        self.http_tokens = "optional"

    def set_endpoint_required(self):
        self.http_tokens = "required"

    def enable_endpoint(self):
        self.http_endpoint = "enabled"

    def disable_endpoint(self):
        self.http_endpoint = "disabled"

    @property
    def message(self):
        if self.http_tokens == "optional":
            return "V1 Enforced"
        elif self.http_tokens == "required":
            return "V2 Enforced"

    def apply(self, dry_run: bool = False):
        if dry_run:
            status = convert_yellow("SUCCESS")
            print(f"IMDS updated: {self.message} for {self.instance_id:<80} {status:>20}")
        else:
            try:
                response = self.ec2_client.modify_instance_metadata_options(
                    InstanceId=self.instance_id,
                    HttpTokens=self.http_tokens,
                    HttpEndpoint=self.http_endpoint,
                )
                status = convert_green("SUCCESS")
            except:
                status = convert_red("FAILED")
            print(f"IMDS updated: {self.message} for {self.instance_id:<80} {status:>20}")

