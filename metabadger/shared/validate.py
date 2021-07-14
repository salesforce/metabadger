# Copyright (c) 2021, salesforce.com, inc.
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root
# or https://opensource.org/licenses/BSD-3-Clause
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
