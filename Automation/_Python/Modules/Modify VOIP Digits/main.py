def get_devices():
    prompt = input('Which Monitors to be configured? [ex. 11,12,21]: ')
    active_pc = prompt.split(',')
    
    return active_pc

def get_configs(user_m, add_dn=''):
    list_of_pcs = ['11','12','21','22','31','32','41','42','51','52','61','62','71','72','81','82','91','92']
    configs = [
        'telephony-service',
        f'ip source-address 10.{user_m}.100.8 port 2000',
        'ephone-dn 1',
        f'number {add_dn}{user_m}11',
        'ephone-dn 2',
        f'number {add_dn}{user_m}22',
        'ephone-dn 3',
        f'number {add_dn}{user_m}33',
        'ephone-dn 4',
        f'number {add_dn}{user_m}44',
        'ephone-dn 5',
        f'number {add_dn}{user_m}55',
        'ephone-dn 6',
        f'number {add_dn}{user_m}66',
        'ephone-dn 7',
        f'number {add_dn}{user_m}77',
        'ephone-dn 8',
        f'number {add_dn}{user_m}88',
        'ephone-dn 9',
        f'number {add_dn}{user_m}99',
        'ephone-dn 10',
        f'number {add_dn}{user_m}89',
        'ephone 1',
        'button 1:1 2:2 3:3 4:4',
        'restart',
        'ephone 2',
        'button 1:5 2:6 3:7 4:8',
        'restart',
        'exit',
        'telephony-service',
        'create cnf-files',
        'exit'
    ]
    
    for pc in list_of_pcs:
        outgoing_peer = [
            f'dial-peer voice {pc} Voip',
            f'destination-pattern {add_dn}{pc}..',
            f'session target ipv4:10.{pc}.100.8',
            'codec g711ULAW'
        ]
        configs.extend(outgoing_peer)
    
    configs.append('end')
    
    return configs
    
def config_devices(user_m, add_dn='', terminal=False):
    device_info = {
        'device_type': 'cisco_ios_telnet',
        'host': f'10.{user_m}.100.8',
        'username': 'admin',
        'password': 'pass',
        'secret': 'pass'
    }
    
    configs = get_configs(user_m, add_dn)
        
    access_cli = ConnectHandler(**device_info)
    access_cli.enable()
    output = access_cli.send_config_set(configs)
    access_cli.disconnect()
    
    if terminal:
        print(output)
        


if __name__ == '__main__':
    import argparse
    import multiprocessing
    import netmiko
    from netmiko import ConnectHandler

    ### ARGUMENT PARSER
    parser = argparse.ArgumentParser()
    parser.add_argument('--add_dn', type=str, help='enter additional dn digits')
    args = parser.parse_args()
    add_dn = args.add_dn

    if not add_dn:
        add_dn = ''
    
    process_list = []
    device_list = get_devices()
    
    ### Use multiprocessing to configure multiple devices at the same time
    for m in device_list:
      proc = multiprocessing.Process(target=config_devices, args=[m, add_dn])
      process_list.append(proc)
    
    ### run the function for each process
    for i in process_list:
        i.start()
    
    ### wait for all the process to finish before moving on to the next line
    for i in process_list:
        i.join()
    
    print('Configuration Complete')

