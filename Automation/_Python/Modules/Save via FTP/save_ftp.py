import multiprocessing
from netmiko import ConnectHandler

def get_ftp_server():
    ftp_server = input('What is the IP Address of the FTP Server? [ex. 10.11.1.10] ')

    return ftp_server

def prompt_user():
    device_list = input('Which hosts to save configs? [ex. 10.11.1.2,10.11.1.4] ')
    device_list = device_list.split(',')
    
    total_device = []
    for devices in device_list:
        device_info = {
            'device_type': 'cisco_ios_telnet',
            'host': devices,
            'username': 'admin',
            'password': 'pass',
            'secret': 'pass'
        }
        total_device.append(device_info)

    return total_device

def save_ftp(ftp_server, device_info):
    try: 
        access_cli = ConnectHandler(**device_info)
        access_cli.enable()

        command = f'copy run ftp'
        filename = f'{device_info["host"]}-configs.cfg'
        output = access_cli.send_command_timing(command)

        if "Address or name of remote host" in output:
            output += access_cli.send_command_timing(ftp_server)
        if "Destination filename" in output:
            output += access_cli.send_command_timing(filename)
        
        access_cli.disconnect()
        print(f'Save Configurations for {device_info["host"]}, Completed!!')

    except Exception as e:
        print(f'''
ERROR: An unexpected error occurred with device {device_info['host']}: 
        
{str(e)}

''')

if __name__ == '__main__':
    ftp_server = get_ftp_server()
    device_list = prompt_user()
    process_list = []

    for devices in device_list:
        proc = multiprocessing.Process(target=save_ftp, args=[ftp_server, devices])
        process_list.append(proc)
    
    for i in process_list:
        i.start()
    
    for i in process_list:
        i.join()
    
    print('Configuration Complete')
