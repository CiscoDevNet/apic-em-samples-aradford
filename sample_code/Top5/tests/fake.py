
from tests.fake_interface_network_device import fake_interface_network_device
from tests.fake_network_device import fake_network_device
from tests.fake_network_device_list import  fake_network_device_list
from tests.fake_host_connected_device import fake_host_connected_device
from tests.fake_licence import fake_licence
from tests.fake_host_wlan import fake_host_wlan
from tests.fake_host_wired import fake_host_wired
from tests.fake_wlc import fake_wlc
from tests.fake_path_trace import fake_path_trace

from tests.fake_path_post import fake_path_post

fake = {
    "network-device" : fake_network_device_list,
    "network-device/ip-address/212.1.10.1" : fake_network_device,
    "interface/network-device/7f794dae-b5fc-4cc4-8140-c088d46c7d51" : fake_interface_network_device,
    "network-device/181bc9ed-fad0-44aa-bc52-b5e1ba06941d" : fake_wlc,
    "host?connectedDeviceIp=212.1.10.1" : fake_host_connected_device,
    "license-info/network-device/7f794dae-b5fc-4cc4-8140-c088d46c7d51" : fake_licence,
    "host?hostMac=00:24:d7:43:59:d8" : fake_host_wlan,
    "host?hostMac=e8:9a:8f:7a:22:99" : fake_host_wired,
    "host?connectedDeviceIp=212.1.10.1" : fake_host_wired,
    "host?hostIp=212.1.10.20" : fake_host_wired,
    "flow-analysis/88dc1fce-34d6-4c6a-83aa-2047a957d835" : fake_path_trace
}

fake_post = {
    "flow-analysis" : fake_path_post
}
