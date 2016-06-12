# Uniq Sample code
Uniq is a python3 client library for APIC-EM.

### Download
Clone this repository:

``` bash
git clone https://github.com/CiscoDevNet/uniq.git
```

### Install a virtualenv
This optional step will create a virtual environement for uniq

``` bash
pyvenv env
source env/bin/activate
```

### Install
Then install the package locally.

``` bash
cd uniq
python3 setup.py install
```

### Use
Import the package and make an API call.

``` python
from uniq.apis.nb.client_manager import NbClientManager

client = NbClientManager(
    server="1.1.1.1",
    username="username",
    password="password",
    connect=True)

# NorthBound API call to get all users
user_list_result = client.user.getUsers()

# Serialize the model object to a python dictionary
users = client.serialize(user_list_result)

print(users)
```
