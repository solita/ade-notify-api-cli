import click
import json
from utils import util
from adenotifier import notifier
from adenotifier import manifest as _manifest
import ast


@click.group()
def manifests():
    """
    Functionality related to manifests.
    """
    pass

@manifests.command()
@click.pass_context
@click.option('--source-system', '--s', required=True)
@click.option('--source-entity', '--e', required=True)
@click.option('--state', type=click.Choice(['archived', 'failed', 'notified', 'open']), help='Manifest state')
def search_manifests(ctx, source_system, source_entity, state):
    """
    Gets all manifests by source system and source entity.
    """

    state_param = ""
    if state:
        state_param = state

    response = notifier.search_manifests(
        source_system, 
        source_entity, 
        f"{ctx.obj['ENVIRONMENT']['notify_api_url']}",
        f"{ctx.obj['ENVIRONMENT']['apikey_id']}", 
        f"{ctx.obj['ENVIRONMENT']['apikey_secret']}",
        state_param
        )

    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


class PythonLiteralOption(click.Option):
    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)

@manifests.command()
@click.pass_context
@click.option('--source-system', '--s', required=True)
@click.option('--source-entity', '--e', required=True)
@click.option('--manifest-id', '--id', required=True)
def get_manifest(ctx, source_system, source_entity, manifest_id):
    """
    Get single manifest by ID.
    """

    # Initialize a manifest object with mandatory attributes.
    manifest = _manifest.Manifest(
        base_url = f"{ctx.obj['ENVIRONMENT']['notify_api_url']}",
        source_system_name = source_system,
        source_entity_name = source_entity,
        format = "unknown",
        notify_api_key = f"{ctx.obj['ENVIRONMENT']['apikey_id']}",
        notify_api_key_secret = f"{ctx.obj['ENVIRONMENT']['apikey_secret']}"
    )

    manifest.fetch_manifest(manifest_id)
    response = manifest.latest_response.json()

    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


class PythonLiteralOption(click.Option):
    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)

@manifests.command()
@click.pass_context
@click.option('--source-system', '--s', required=True)
@click.option('--source-entity', '--e', required=True)
@click.option('--format', required=True, type=click.Choice(['csv', 'json', 'xml', 'unknown']))
@click.option('--batch', type=int)
@click.option('--columns', cls=PythonLiteralOption, default='[]', help="""Format "['column1', 'column2']" """)
@click.option('--compression', type=click.Choice(['bzip2', 'gzip', 'lzop']))
@click.option('--delim', type=click.Choice(['comma', 'hash', 'pipe', 'semicolon', 'tab']))
@click.option('--fullscanned', type=click.Choice(['false', 'true']))
@click.option('--skiph', type=int)
def create_manifest(ctx, source_system, source_entity, format, batch, columns, compression, delim, fullscanned, skiph):
    """
    Creates a new manifest.
    """

    # Initialize a manifest object with mandatory attributes.
    manifest = _manifest.Manifest(
        base_url = f"{ctx.obj['ENVIRONMENT']['notify_api_url']}",
        source_system_name = source_system,
        source_entity_name = source_entity,
        format = format.upper(),
        notify_api_key = f"{ctx.obj['ENVIRONMENT']['apikey_id']}",
        notify_api_key_secret = f"{ctx.obj['ENVIRONMENT']['apikey_secret']}"
    )

    # Set optional manifest attributes if configured in data source.
    if columns:
        manifest.columns = columns
    if batch:
        manifest.batch = batch
    if compression:
        manifest.compression = compression.upper()
    if delim:
        manifest.delim = delim.upper()
    if fullscanned:
        manifest.fullscanned = fullscanned
    if skiph:
        manifest.skiph = skiph

    manifest.create()

    response = manifest.id

    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@manifests.command()
@click.pass_context
@click.option('--source-system', '--s', required=True)
@click.option('--source-entity', '--e', required=True)
@click.option('--manifest-id', '--id', required=True)
def notify(ctx, source_system, source_entity, manifest_id):
    """
    Notify manifest.
    """

    # Initialize a manifest object with mandatory attributes.
    manifest = _manifest.Manifest(
        base_url = f"{ctx.obj['ENVIRONMENT']['notify_api_url']}",
        source_system_name = source_system,
        source_entity_name = source_entity,
        format="unknown",
        notify_api_key = f"{ctx.obj['ENVIRONMENT']['apikey_id']}",
        notify_api_key_secret = f"{ctx.obj['ENVIRONMENT']['apikey_secret']}"
    )

    manifest.fetch_manifest(manifest_id)

    manifest.notify()

    if manifest.latest_response.status_code == 200:
        response = f"Manifest {manifest.id} notified"
    else:
        response = manifest.latest_response.json()

    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@manifests.command()
@click.pass_context
@click.option('--source-system', '--s', required=True)
@click.option('--source-entity', '--e', required=True)
@click.option('--manifest-id', '--id', required=True)
@click.option('--source-file', required=True)
@click.option('--batch', type=int)
@click.option('--content-length', type=int)
def add_entry(ctx, source_system, source_entity, manifest_id, source_file, batch, content_length):
    """
    Add entry to manifest.
    """

    # Initialize a manifest object with mandatory attributes.
    manifest = _manifest.Manifest(
        base_url = f"{ctx.obj['ENVIRONMENT']['notify_api_url']}",
        source_system_name = source_system,
        source_entity_name = source_entity,
        format="unknown",
        notify_api_key = f"{ctx.obj['ENVIRONMENT']['apikey_id']}",
        notify_api_key_secret = f"{ctx.obj['ENVIRONMENT']['apikey_secret']}"
    )

    manifest.fetch_manifest(manifest_id)

    if batch and content_length:
        manifest.add_entry(source_file, batch, content_length)
    if batch:
        manifest.add_entry(source_file, batch)
    if content_length:
        manifest.add_entry(source_file, content_length=content_length)
    else:
        manifest.add_entry(source_file)

    if manifest.latest_response.status_code == 200:
        response = f"Manifest entry added to manifest {manifest}"
    else:
        response = manifest.latest_response.json()

    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@manifests.command()
@click.pass_context
@click.option('--source-system', '--s', required=True)
@click.option('--source-entity', '--e', required=True)
@click.option('--manifest-id', '--id', required=True)
@click.option('--entries', cls=PythonLiteralOption, default='[]', 
    help="""Format "[{'sourceFile': 'file1', 'batch': 123}, {'sourceFile': 'file2', 'batch': 123}]" """)
@click.option('--file', help='Local JSON file path')
def add_entries(ctx, source_system, source_entity, manifest_id, entries, file):
    """
    Add or overwrite entries to manifest. You can use either --entries parameter to supply JSON object
    or --file parameter to supply JSON file to be loaded.
    """


    # Initialize a manifest object with mandatory attributes.
    manifest = _manifest.Manifest(
        base_url = f"{ctx.obj['ENVIRONMENT']['notify_api_url']}",
        source_system_name = source_system,
        source_entity_name = source_entity,
        format="unknown",
        notify_api_key = f"{ctx.obj['ENVIRONMENT']['apikey_id']}",
        notify_api_key_secret = f"{ctx.obj['ENVIRONMENT']['apikey_secret']}"
    )

    manifest.fetch_manifest(manifest_id)

    if entries != []:
        manifest.add_entries(entries)
    if file and entries == []:
        f = open(file)
        entries_dict = json.load(f)
        manifest.add_entries(entries_dict)

    if manifest.latest_response.status_code == 200:
        response = f"Manifest entries added to manifest {manifest}"
    else:
        response = manifest.latest_response.json()

    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))


@manifests.command()
@click.pass_context
@click.option('--source-system', '--s', required=True)
@click.option('--source-entity', '--e', required=True)
@click.option('--manifest-id', '--id', required=True)
def get_entries(ctx, source_system, source_entity, manifest_id):
    """
    Get manifest entries.
    """

    # Initialize a manifest object with mandatory attributes.
    manifest = _manifest.Manifest(
        base_url = f"{ctx.obj['ENVIRONMENT']['notify_api_url']}",
        source_system_name = source_system,
        source_entity_name = source_entity,
        format="unknown",
        notify_api_key = f"{ctx.obj['ENVIRONMENT']['apikey_id']}",
        notify_api_key_secret = f"{ctx.obj['ENVIRONMENT']['apikey_secret']}"
    )

    manifest.fetch_manifest(manifest_id)

    manifest.fetch_manifest_entries()
    response = manifest.manifest_entries

    if ctx.obj['OUT']:
        util.write_to_file(ctx.obj['DIR'], f"{ctx.obj['OUT']}", response)
    else:
        click.echo(util.pretty_json(response))