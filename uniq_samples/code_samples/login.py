'''
login helper module.
'''
import requests.exceptions
from apic_config import APIC, APIC_USER, APIC_PASSWORD
from uniq.apis.nb.client_manager import NbClientManager


def login():
    """ Login to APIC-EM northbound APIs in shell.
    Returns:
        Client (NbClientManager) which is already logged in.
    """


    try:
        client = NbClientManager(
                server=APIC,
                username=APIC_USER,
                password=APIC_PASSWORD,
                connect=True)
        return client
    except requests.exceptions.HTTPError as exc_info:
        if exc_info.response.status_code == 401:
            print('Authentication Failed. Please provide valid username/password.')
        else:
            print('HTTP Status Code {code}. Reason: {reason}'.format(
                    code=exc_info.response.status_code,
                    reason=exc_info.response.reason))
        exit(1)
    except requests.exceptions.ConnectionError:
        print('Connection aborted. Please check if the host {host} is available.'.format(host=APIC))
        exit(1)
