import json
import click
import os
import requests
from uuid import UUID


def write_to_file(dir, file_name, content):
    path = ""

    if dir:
        click.echo("asd")
        path = f"{dir}/"

    if path != "" and not os.path.exists(path):
        os.makedirs(path)

    
    location = f"{path}{file_name}"

    with open(location, "w") as file:
        click.echo(pretty_json(content), file=file)


def pretty_json(content):
    return json.dumps(content, indent=4)


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def get_environment_config_from_context(ctx, environment_name):
    config = ctx.obj['CONFIG']
    if environment_name.lower() in config['tenants'][ctx.obj['TENANT']]['installations'][ctx.obj['INSTALLATION']]['environments']:
        return config['tenants'][ctx.obj['TENANT']]['installations'][ctx.obj['INSTALLATION']]['environments'][environment_name.lower()]
    else:
        click.echo(
            f"Configure {environment_name.lower()} environment for tenant {ctx.obj['TENANT']} and installation {ctx.obj['INSTALLATION']}")
        exit(1)
