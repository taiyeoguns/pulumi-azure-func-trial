# Pulumi Azure Functions Trial

Trial on deploying simple Azure Functions Python application with Pulumi on Azure.

### Requirements

- Python 3.8
- [Azure Functions Core Tools](https://github.com/Azure/azure-functions-core-tools)
- [Pulumi](https://www.pulumi.com/docs/get-started/install/)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)

### Installation

Install `Pulumi` and `Azure CLI` from links above.

### Clone Project

```sh
git clone https://github.com/taiyeoguns/pulumi-azure-func-trial.git
```

and then change to directory

```sh
cd pulumi-azure-func-trial
```

### Create and activate virtual environment

```sh
python -m venv venv
```

```sh
source venv/bin/activate
```


### Set up Azure

If Azure credentials/SSO not already set up, open a command prompt, enter:

```sh
az login
```

and follow the instructions.

### Install Requirements

```sh
pip install -r requirements.txt
```

### Run locally

```sh
cd application
func host start
```

Server should be started at `http://localhost:7071`

### Azure Deployment

To spin up resources, enter:

```sh
cd infrastructure
pulumi up
```

If successful, deployed application url should be available from the `function_url` output in the console, e.g. `funcappb5dfe6e5.azurewebsites.net/api`

Endpoint can be tested with `funcappb5dfe6e5.azurewebsites.net/api/http_trigger?name=foo`

To tear down resources, use:

```sh
cd infrastructure
pulumi destroy
```

###  Project layout

This project structure combines a Pulumi application and a Azure Functions application. These correspond to the `infrastructure` and `application` directories respectively.  To run any Pulumi commands, ensure you're in the `infrastructure` directory, and to run any Azure Functions core tools commands ensure you're in the `application` directory.

### Further Information

- [https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- [https://www.pulumi.com/docs/intro/languages/python/](https://www.pulumi.com/docs/intro/languages/python/)
- [https://www.pulumi.com/registry/packages/azure-native/](https://www.pulumi.com/registry/packages/azure-native/)
- [https://github.com/pulumi/examples/tree/master/azure-ts-functions-many](https://github.com/pulumi/examples/tree/master/azure-ts-functions-many)
- [https://github.com/pulumi/examples](https://github.com/pulumi/examples)
