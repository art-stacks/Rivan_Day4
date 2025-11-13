import netmiko
from netmiko import ConnectHandler
import json

## READ DATA
with open('device.json') as file:
    device = json.load(file)

## PARSE 
ph_info = device['VPN_PH']['device_info']
ph_configs = device['VPN_PH']['configs']

jp_info = device['VPN_JP']['device_info']
jp_configs = device['VPN_JP']['configs']


## CONNECT
def config_devices(device_info, device_configs):
    access_cli = ConnectHandler(**device_info)
    output = access_cli.send_config_set(device_configs)
    access_cli.disconnect()

    return output

if __name__ == '__main__':
    order_of_config = [
        'VPN_PH', 
        'VPN_JP'
    ]

    for device in order_of_config:
        if device == 'VPN_PH':
            output = config_devices(ph_info, ph_configs)
        elif device == 'VPN_JP':
            output = config_devices(jp_info, jp_configs)
        
        print(f'''
########################
Configuring {device}
########################

{output}



              ''')
        

