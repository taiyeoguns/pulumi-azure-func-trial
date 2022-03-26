"""An Azure RM Python Pulumi program."""

from pathlib import Path

import pulumi
from pulumi_azure_native import insights, resources, storage, web
from utilities.naming import env_name
from utilities.storage import signed_blob_read_url
from utilities.tagging import register_auto_tags

APPLICATION_PATH = Path(__file__).parents[1] / "application"

register_auto_tags(
    {
        "project": pulumi.get_project(),
        "stack": pulumi.get_stack(),
    }
)


# Create an Azure Resource Group
resource_group = resources.ResourceGroup(env_name("rg"))

# create application insight
application_insight = insights.Component(
    env_name("app-insights"),
    resource_group_name=resource_group.name,
    application_type=insights.ApplicationType.WEB,
    kind=insights.ApplicationType.WEB,
)

# Create an Azure resource (Storage Account)
storage_account = storage.StorageAccount(
    env_name("sa", no_dash=True),
    resource_group_name=resource_group.name,
    sku=storage.SkuArgs(
        name=storage.SkuName.STANDARD_LRS,
    ),
    kind=storage.Kind.STORAGE_V2,
)

app_service_plan = web.AppServicePlan(
    env_name("asp"),
    kind="Linux",
    resource_group_name=resource_group.name,
    sku={"name": "Y1", "tier": "Dynamic"},
    reserved=True,
)

container = storage.BlobContainer(
    env_name("container"),
    account_name=storage_account.name,
    resource_group_name=resource_group.name,
    public_access=storage.PublicAccess.NONE,
)

function_app_blob = storage.Blob(
    env_name("fn-app-blob"),
    resource_group_name=resource_group.name,
    account_name=storage_account.name,
    container_name=container.name,
    source=pulumi.asset.FileArchive(str(APPLICATION_PATH)),
)

function_app_signed_url = signed_blob_read_url(
    blob=function_app_blob,
    container=container,
    account=storage_account,
    resource_group=resource_group,
)

function_app = web.WebApp(
    env_name("funcapp"),
    resource_group_name=resource_group.name,
    server_farm_id=app_service_plan.id,
    kind="FunctionApp",
    site_config=web.SiteConfigArgs(
        app_settings=[
            web.NameValuePairArgs(name="runtime", value="python"),
            web.NameValuePairArgs(name="FUNCTIONS_WORKER_RUNTIME", value="python"),
            web.NameValuePairArgs(
                name="WEBSITE_RUN_FROM_PACKAGE",
                value=function_app_signed_url,
            ),
            web.NameValuePairArgs(name="FUNCTIONS_EXTENSION_VERSION", value="~3"),
            web.NameValuePairArgs(
                name="APPINSIGHTS_INSTRUMENTATIONKEY",
                value=application_insight.instrumentation_key,
            ),
            web.NameValuePairArgs(
                name="APPLICATIONINSIGHTS_CONNECTION_STRING",
                value=application_insight.instrumentation_key.apply(
                    lambda key: "InstrumentationKey=" + key
                ),
            ),
            web.NameValuePairArgs(
                name="ApplicationInsightsAgent_EXTENSION_VERSION", value="~2"
            ),
        ]
    ),
)

function_url = pulumi.Output.all(function_app.default_host_name).apply(
    lambda output: f"https://{output[0]}/api",
)

pulumi.export("function_url", function_url)
