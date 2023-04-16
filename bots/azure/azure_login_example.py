import json
import requests
import urllib.request
from azure.cli.core import get_default_cli

azureUser = "azureUser"
azurePass = "azurePass"
subscriptionId = "subscriptionId"

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

params = {
    "subscriptionId": subscriptionId,
    "NsgsDetails": [{"rgname": "test", "nsgsnames": ["test-storage-name"]},
                    {"rgname": "test2", "nsgsnames": ["test2-storage-name"]}
                    ]
}

# azure client creation:
azure_cli = get_default_cli()

# azure login
azure_cli.invoke(['login','-u', azureUser,'-p', azurePass])

result = azure_cli.result.result['properties']['outputs']['storagesAccountKeys']['value']

print(result)
