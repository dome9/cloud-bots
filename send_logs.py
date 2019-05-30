import json
from botocore.vendored import requests
import os
import time
from time import gmtime, strftime

SUMO_HTTP_ENDPOINT = 'https://endpoint4.collection.us2.sumologic.com/receiver/v1/http/ZaVnC4dhaV3N-lPxodY4J3xadi2by444XVaSboLlcbfMeGhqAnZn4PIVuJw_h3EzhhCv4jEFLfhHO3nbvfVgVSiRrB2X1hedSvXwyKB31hF3zdmR7j7mrQ=='


def getTimeStamp():
    timeStamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    timeStamp += "Z"
    return timeStamp


def send_logs(message, start_time, vendor):
    account_mode = os.getenv('ACCOUNT_MODE', '')
    cross_account_role_name = os.getenv('CROSS_ACCOUNT_ROLE_NAME', '')
    output_type = os.getenv('OUTPUT_TYPE', '')
    execution_time = time.time() - start_time
    session = requests.Session()
    headers = {"Content-Type": "application/json", "Accept": "application/json", "X-Sumo-Name": message.get('Account id'), "X-Sumo-Category": vendor}
    data = {'timestamp': getTimeStamp(),
            'msg': message,
            'account_mode': account_mode,
            'cross_account_role_name': cross_account_role_name,
            'output_type': output_type,
            'execution_time': execution_time}
    r = session.post(SUMO_HTTP_ENDPOINT, headers=headers, data=json.dumps(data))
    print(f'{__file__} - status code from dome9 logs: {r.status_code}')
    return
