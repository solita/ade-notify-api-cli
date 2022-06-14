import click
import http.client
import os
import json
from utils import util
from commands import config
from commands import manifests


@click.group()
@click.option('--tenant', envvar='ADE_TENANT', help="Tenant name used for calls")
@click.option('--installation', envvar='ADE_INSTALLATION', default='datahub')
@click.option('--environment', envvar='ADE_ENVIRONMENT', help="Installation name used for calls")
@click.option('--debug', is_flag=True, default=False, help="Enables debugging for http requests")
@click.option('--out', help="Output file name where response is written")
@click.option('--dir', help="Name of the folder where output is saved")
@click.pass_context
def adenf(ctx, tenant, environment, installation, debug, out, dir):
    """Agile Data Engine Notify API CLI tool.

    This tool is can be used to make requests to ADE Notify API. 
    It was created to provide to show example usage of the API and
    to help get started with more complex use scenarios.

    Usage requires setting up environment credentials using config
    command. Each call requires the user to specify which tenant and 
    environment should be used in the request. These can be specified 
    using options --tenant and --installation. Optionally you can specify
    them using environment variables:

    \b
    export ADE_TENANT=
    export ADE_INSTALLATION=
    export ADE_ENVIRONMENT=

    """

    click.get_app_dir(app_name='ade', roaming=False, force_posix=True)
    if not os.path.exists(click.get_app_dir(app_name='ade', roaming=False, force_posix=True)):
        os.makedirs(click.get_app_dir(app_name='ade', roaming=False, force_posix=True))

    config_path = f"{click.get_app_dir(app_name='ade', roaming=False, force_posix=True)}/ade-notify-api-cli-config.json"
    ctx.ensure_object(dict)
    ctx.obj['CONFIG_PATH'] = config_path
    if click.get_current_context().invoked_subcommand != 'config':
        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                config = json.loads(file.read())
        else:
            click.echo(
                f"Configure credential using 'adenf config' to before using the tool")
            exit(1)

        if tenant == None or installation == None or environment == None:
            click.echo(f"Error: Missing parameters --tenant or --installation or --environment")
            exit(1)

        env = {}
        if tenant in config['tenants'] and installation in config['tenants'][tenant]['installations']:
            env = config['tenants'][tenant]['installations'][installation]['environments'][environment]
        
        if not env:
            click.echo(
                f"Configure design environment for tenant {tenant} and installation {installation}")
            exit(1)

        if debug:
            http.client.HTTPConnection.debuglevel = 1

        ctx.obj['ENVIRONMENT'] = env
        ctx.obj['TENANT'] = tenant
        ctx.obj['INSTALLATION'] = installation
        ctx.obj['CONFIG'] = config

        ctx.obj['OUT'] = out
        ctx.obj['DIR'] = dir


adenf.add_command(config.config)
adenf.add_command(manifests.manifests)
