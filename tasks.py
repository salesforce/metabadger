#!/usr/bin/env python
import sys
import os
import logging
from invoke import task, Collection

BIN = os.path.abspath(os.path.join(os.path.dirname(__file__), "metabadger", "bin", "cli.py"))
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.path.pardir, "metabadger")
    )
)

# Create the necessary collections (namespaces)
ns = Collection()

test = Collection("test")
ns.add_collection(test)

@task
def disable_metadata(c):
    c.run(f"echo 'Disabling the metadata on instances'")
    c.run(f"{BIN} disable-metadata", pty=True)

@task
def discover_metadata(c):
    c.run(f"echo 'Discovering metadata of instances'")
    c.run(f"{BIN} discover-metadata", pty=True)

@task
def discover_role_usage(c):
    c.run(f"echo 'Discovering roles of instances'")
    c.run(f"{BIN} discover-role-usage", pty=True)

@task
def harden_metadata(c):
    c.run(f"echo 'Discovering roles of instances'")
    c.run(f"{BIN} harden-metadata", pty=True)

test.add_task(disable_metadata, "disable-metadata")
test.add_task(discover_metadata, "discover-metadata")
test.add_task(discover_role_usage, "discover-role-usage")
test.add_task(harden_metadata, "harden-metadata")
