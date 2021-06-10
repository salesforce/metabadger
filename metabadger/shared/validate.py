import click


def click_validate_tag_alphanumeric(ctx, param, value):
    if value is not None:
        try:
            if value == "":
                return []
            else:
                tag_values_to_check = value.split(",")
                return tag_values_to_check
        except ValueError:
            raise click.BadParameter(
                "Supply the list of tag names to include for hardening in a comma separated string."
            )
