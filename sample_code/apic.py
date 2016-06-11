import requests
import json
import time
import logging
from apic_config import APIC, APIC_USER, APIC_PASSWORD
requests.packages.urllib3.disable_warnings()

# -------------------------------------------------------------------
# Custom exception definitions
# -------------------------------------------------------------------
class TaskTimeoutError(Exception):
    pass

class TaskError(Exception):
    pass

# API ENDPOINTS
ENDPOINT_TICKET = "ticket"
ENDPOINT_TASK_SUMMARY ="task/%s"
RETRY_INTERVAL=2

# -------------------------------------------------------------------
# Helper functions
# -------------------------------------------------------------------
def create_url(path, controller_ip=APIC):
    """ Helper function to create a APIC-EM API endpoint URL
    """

    return "https://%s/api/v1/%s" % (controller_ip, path)


def get_auth_token(controller_ip=APIC, username=APIC_USER, password=APIC_PASSWORD):
    """ Authenticates with controller and returns a token to be used in subsequent API invocations
    """

    login_url = create_url(ENDPOINT_TICKET, controller_ip,)

    data = {
        "username": username,
        "password": password
    }
    headers={"Content-Type" : "application/json"}
    result = requests.post(url=login_url, data=json.dumps(data), headers=headers, verify=False)
    result.raise_for_status()

    token = result.json()["response"]["serviceTicket"]
    return {
        "controller_ip": controller_ip,
        "token": token
    }

def wait_on_task(task_id, token, timeout=(3*RETRY_INTERVAL), retry_interval=RETRY_INTERVAL):
    """ Waits for the specified task to complete
    """

    task_url = create_url(ENDPOINT_TASK_SUMMARY % task_id, token["controller_ip"])

    headers = {
        "x-auth-token": token["token"]
    }
    start_time = time.time()

    while True:
        result = requests.get(url=task_url, headers=headers, verify=False)
        result.raise_for_status()

        response = result.json()["response"]
        #print json.dumps(response)
        if "endTime" in response:
            return response
        else:
            if timeout and (start_time + timeout < time.time()):
                raise TaskTimeoutError("Task %s did not complete within the specified timeout "
                                       "(%s seconds)" % (task_id, timeout))

            print("Task=%s has not completed yet. Sleeping %s seconds..." %(task_id, retry_interval))
            time.sleep(retry_interval)

        if response['isError'] == True:
            raise TaskError("Task %s had error %s" % (task_id, response['progress']))

    return response