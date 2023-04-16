import json
import requests
import urllib.request
from azure.cli.core import get_default_cli

# install requests (pip install requests)
# install azure cli (pip install azure-cli)

dome9ApiKey = "dome9ApiKey"
dome9ApiSecret = "dome9ApiSecret"
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

# get json url arm
arm_url = requests.post('https://api.dome9.com/v2/view/magellan/magellan-azure-flowlogs-onboarding-with-arm',
                        json=params, headers=headers, auth=(dome9ApiKey, dome9ApiSecret))

valid_url = json.loads(arm_url.content)
if valid_url:
    # get arm content
    with urllib.request.urlopen(valid_url) as url:
        with open('data.json', 'w') as f:
            json.dump(json.loads(url.read().decode("utf-8")), f, indent=4)

    # azure running command:
    azure_cli = get_default_cli()

    # azure login
    azure_cli.invoke(['login','-u', azureUser,'-p', azurePass])
    # azure run arm
    azure_cli.invoke(['deployment', 'sub', 'create', '--location', 'eastus', '--template-file', 'data.json'])
    # get storage keys
    keys = azure_cli.result.result['properties']['outputs']['storagesAccountKeys']['value']


    params = {
        "StorageDetails": keys,
        "SubscriptionId": subscriptionId
    }
    storage_key_respond = requests.post('https://api.dome9.com/v2/view/magellan/provide-azure-storage-details', json=params,
                                        headers=headers, auth=(dome9ApiKey, dome9ApiSecret))

    print(storage_key_respond)
