# ade-notify-api-cli

Example client application for Agile Data Engine's Notify API. Similar client application is provided for External API: https://github.com/solita/ade-external-api-cli 

## Installation

Install tool using the following command

```pip install .```

Usage requires configuring Notify API credentials for the tool. Configuration can be done using configuration command

```adenf config add --tenant {tenant} --installation {installation} --environment {environment} --notify-api-url {notify-api-url} --apikey-id {apikey_id} --apikey-secret {apikey_secret}```

The tool requires at least one runtime environment to be configured.

You can find your tenant, installation and environment from your Notify API URL. Usually in format ```https://external-api.{environment}.{installation}.{tenant}.saas.agiledataengine.com/notify-api```

Tenant, installation, environment and Notify API URL are all required as parameters, since they can deviate in different installations.

Access keys are saved under ```~/.ade```

## Usage
Use tool with command 
```bash
adenf [OPTIONS] COMMAND [ARGS]
```

To get more information about all the commands available, use ```--help``` parameter with all commands and subcommands. It will give more information about the command and display all available parameters and subcommands.

Use environment variables or parameters to change environments:
```bash
# Environment variables
export ADE_TENANT={tenant}
export ADE_INSTALLATION={installation}
export ADE_ENVIRONMENT={environment}

# Or use --environment flag, for example, to switch between different environments in same tenant
adenf --environment dev manifests search-manifests --s system --e test

adenf --environment prod manifests search-manifests --s system --e test
```


## Troubleshooting

if you get this error

```ModuleNotFoundError: No module named 'utils'```

install the tool using

```pip install --editable .```

### Script not in PATH
Export PATH (in Linux/WSL for example):
```export PATH=$PATH:/home/{username}/.local/bin```