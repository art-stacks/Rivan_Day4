import json
import yaml

class GeneratePlaybook:
    def __init__(self, 
                 monitor_num,
                 username,
                 password):
        
        self.m = monitor_num
        self.usr = username
        self.passw = password
        
        self.assets = promptAssetInfo()
        
        self.cam_6 = self.assets['cam_6']
        self.cam_8 = self.assets['cam_8']
        self.ephone_1 = self.assets['ephone_1']
        self.ephone_2 = self.assets['ephone_2']
        
        self.coreTaas()
        self.coreBaba()
        self.callManager()
        self.edgeRouter()
        self.ivrs()
        self.runAll()
    
    def coreTaas(self):
        self.ctaas_config = [
            {
                'name': 'Configuring Console Access',
                'ios_command': {
                    'commands': [
                        'conf t',
                        f'hostname coreTaas-{self.m}',
                        'enable secret pass',
                        'service password-encryption',
                        'no logging console',
                        'no ip domain-lookup',
                        'line cons 0',
                        'password pass',
                        'login',
                        'exec-timeout 0 0',
                        'exit',
                        'line vty 0 14',
                        'password pass',
                        'login local',
                        'exec-timeout 0 0',
                        'end'
                    ]
                },
                'tags': ['accesscli']
            },
            {
                'name': 'Creating SVIs (Switch Virtual Interfaces)',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'int vlan 1',
                        'no shut',
                        f'ip add 10.{self.m}.1.2 255.255.255.0',
                        'desc VLAN-MGMT-DATA',
                        'exit',
                        'int vlan 10',
                        'no shut',
                        f'ip add 10.{self.m}.10.2 255.255.255.0',
                        'desc VLAN-MGMT-WIFI',
                        'exit',
                        'int vlan 50',
                        'no shut',
                        f'ip add 10.{self.m}.50.2 255.255.255.0',
                        'desc VLAN-MGMT-CCTV',
                        'exit',
                        'int vlan 100',
                        'no shut',
                        f'ip add 10.{self.m}.100.2 255.255.255.0',
                        'desc VLAN-MGMT-VOICE',
                        'end'
                    ]
                },
                'tags': ['svi']
            }
        ]
        
        with open('ctaas.yml', 'w') as file:
            self.output = yaml.safe_dump(self.ctaas_config, explicit_start=True)
            file.write(self.output)
    
    def coreBaba(self):
        self.cbaba_config = [
            {
                'name': 'Configuring Console Access',
                'ios_command': {
                    'commands': [
                        'conf t',
                        f'hostname coreBaba-{self.m}',   
                        'enable secret pass',
                        'service password-encryption',
                        'no logging console',
                        'no ip domain lookup',        
                        'line cons 0',
                        'password pass',
                        'login',
                        'exec-timeout 0 0',
                        'exit',
                        'line vty 0 14',
                        'password pass',
                        'login local',
                        'exec-timeout 0 0',
                        'end'
                    ]
                },
                'tags': ['accesscli']
            },
            {
                'name': 'Creating SVIs and Applying IP addresses',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'int gi 0/1',
                        'no shut',
                        'no switchport',
                        f'ip add 10.{self.m}.{self.m}.4 255.255.255.0',
                        'int vlan 1',
                        'no shut',
                        f'ip add 10.{self.m}.1.4 255.255.255.0',
                        'desc VLAN-MGMT-DATA',
                        'exit',
                        'int vlan 10',
                        'no shut',
                        f'ip add 10.{self.m}.10.4 255.255.255.0',
                        'desc VLAN-MGMT-WIFI',
                        'exit',
                        'int vlan 50',
                        'no shut',
                        f'ip add 10.{self.m}.50.4 255.255.255.0',
                        'desc VLAN-MGMT-CCTV',
                        'exit',
                        'int vlan 100',
                        'no shut',
                        f'ip add 10.{self.m}.100.4 255.255.255.0',
                        'desc VLAN-MGMT-VOICE',
                        'end'
                    ]
                },
                'tags': ['svi']
            },
            {
                'name': 'Configuring DHCP Pools',
                'ios_command': {
                    'commands': [
                        'conf t',
                        f'ip dhcp excluded-add 10.{self.m}.1.1 10.{self.m}.1.100',
                        f'ip dhcp excluded-add 10.{self.m}.10.1 10.{self.m}.10.100',
                        f'ip dhcp excluded-add 10.{self.m}.50.1 10.{self.m}.50.100',
                        f'ip dhcp excluded-add 10.{self.m}.100.1 10.{self.m}.100.100',
                        'ip dhcp pool POOLDATA',
                        f'network 10.{self.m}.1.0 255.255.255.0',
                        f'default-router 10.{self.m}.1.4',
                        'domain-name MGMTDATA.COM',
                        f'dns-server 10.{self.m}.1.10',
                        'ip dhcp pool POOLWIFI',
                        f'network 10.{self.m}.10.0 255.255.255.0',
                        f'default-router 10.{self.m}.10.4',
                        'domain-name WIFIDATA.COM',
                        f'dns-server 10.{self.m}.1.10',
                        'ip dhcp pool POOLCCTV',
                        f'network 10.{self.m}.50.0 255.255.255.0',
                        f'default-router 10.{self.m}.50.4',
                        'domain-name CCTVDATA.COM',
                        f'dns-server 10.{self.m}.1.10',
                        'ip dhcp pool POOLVOICE',
                        f'network 10.{self.m}.100.0 255.255.255.0',
                        f'default-router 10.{self.m}.100.4',
                        'domain-name VOICEDATA.COM',
                        f'dns-server 10.{self.m}.1.10',
                        f'option 150 ip 10.{self.m}.100.8',
                        'end'
                    ]
                },
                'tags': ['dhcp']
            },
            {
                'name': 'Creating VLANs and Assigning Switchports',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'vlan 10',
                        'name WIFIVLAN',
                        'vlan 50',
                        'name CCTVVLAN',
                        'vlan 100',
                        'name VOICEVLAN',
                        'int fa 0/2',
                        'switchport mode access',
                        'switchport access vlan 10',
                        'int fa 0/4',
                        'switchport mode access',
                        'switchport access vlan 10',
                        'int fa 0/6',
                        'switchport mode access',
                        'switchport access vlan 50',
                        'int fa 0/8',
                        'switchport mode access',
                        'switchport access vlan 50',
                        'int fa 0/3',
                        'switchport mode access',
                        'switchport access vlan 100',
                        'int fa 0/5',
                        'switchport mode access',
                        'switchport voice vlan 100',
                        'switchport access vlan 1',
                        'mls qos trust device cisco-phone',
                        'int fa 0/7',
                        'switchport mode access',
                        'switchport voice vlan 100',
                        'switchport access vlan 1',
                        'mls qos trust device cisco-phone',
                        'end'
                    ]
                },
                'tags': ['swport']
            },
            {
                'name': 'Reserving IPs for Cameras',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'ip routing',
                        'ip dhcp pool CAMERA6',
                        f'host 10.{self.m}.50.6 255.255.255.0',
                        f'client-identifier {self.cam_6}',
                        'ip dhcp pool CAMERA8',
                        f'host 10.{self.m}.50.8 255.255.255.0',
                        f'client-identifier {self.cam_8}',
                        'end'
                    ]
                },
                'tags': ['ipcam']
            },
            {
                'name': 'Assigning a Floating Static Default Route',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'ip routing',
                        f'ip route 0.0.0.0 0.0.0.0 10.{self.m}.{self.m}.1 254',
                        'end'
                    ]
                },
                'tags': ['defroute']
            },
            {
                'name': 'Configuring OSPF',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'router ospf 1',
                        f'router-id 10.{self.m}.{self.m}.4',
                        f'network 10.{self.m}.0.0 0.0.255.255 area 0',
                        'int gi 0/1',
                        'ip ospf network point-to-point',
                        'end'
                    ]
                },
                'tags': ['ospf']
            }
        ]
        
        with open('cbaba.yml', 'w') as file:
            self.output = yaml.safe_dump(self.cbaba_config, explicit_start=True)
            file.write(self.output)
    
    def callManager(self):
        self.cucm_config = [
            {
                'name': 'Configuring Console Access',
                'ios_command': {
                    'commands': [
                        'conf t',
                        f'hostname cucm-{self.m}',
                        'enable secret pass',
                        'service password-encryption',
                        'no logging console',
                        'no ip domain-lookup',
                        'line cons 0',
                        'password pass',
                        'login',
                        'exec-timeout 0 0',
                        'exit',
                        'line vty 0 14',
                        'password pass',
                        'login local',
                        'exec-timeout 0 0',
                        'end'
                    ]
                },
                'tags': ['accesscli']
            },
            {
                'name': 'Assigning IP Addresses',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'int fa0/0',
                        'no shut',
                        f'ip add 10.{self.m}.100.8 255.255.255.0',
                        'end'
                    ]
                },
                'tags': ['interface']
            },
            {
                'name': 'Configuring Analogue Phones',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'dial-peer voice 1 pots',
                        f'destination-pattern {self.m}00',
                        'port 0/0/0',
                        'dial-peer voice 2 pots',
                        f'destination-pattern {self.m}01',
                        'port 0/0/1',
                        'dial-peer voice 3 pots',
                        f'destination-pattern {self.m}02',
                        'port 0/0/2',
                        'dial-peer voice 4 pots',
                        f'destination-pattern {self.m}03',
                        'port 0/0/3',
                        'end'
                    ]
                },
                'tags': ['analogue']
            },
            {
                'name': 'Initializing Telephony Service',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'no telephony-service',
                        'telephony-service',
                        'no auto assign',
                        'no auto-reg-ephone',
                        'max-ephones 5',
                        'max-dn 20',
                        f'ip source-address 10.{self.m}.100.8 port 2000',
                        'create cnf-files',
                        'ephone-dn 1',
                        f'number {self.m}11',
                        'ephone-dn 2',
                        f'number {self.m}22',
                        'ephone-dn 3',
                        f'number {self.m}33',
                        'ephone-dn 4',
                        f'number {self.m}44',
                        'ephone-dn 5',
                        f'number {self.m}55',
                        'ephone-dn 6',
                        f'number {self.m}66',
                        'ephone-dn 7',
                        f'number {self.m}77',
                        'ephone-dn 8',
                        f'number {self.m}88',
                        'ephone 1',
                        f'mac-address {self.ephone_1}',
                        'type 8945',
                        'button 1:1 2:2 3:3 4:4',
                        'restart',
                        'ephone 2',
                        f'mac-address {self.ephone_2}',
                        'type 8945',
                        'button 1:5 2:6 3:7 4:8',
                        'restart',
                        'end'
                    ]
                },
                'tags': ['telephony']
            },
            {
                'name': 'Activating Video Calls',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'ephone 1',
                        'video',
                        'voice service voip',
                        'h323',
                        'call start slow',
                        'ephone 2',
                        'video',
                        'voice service voip',
                        'h323',
                        'call start slow',
                        'end'
                    ]
                },
                'tags': ['video']
            },
            {
                'name': 'Allowing Incoming Calls',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'voice service voip',
                        'ip address trusted list',
                        'ipv4 0.0.0.0 0.0.0.0',
                        'end'
                    ]
                },
                'tags': ['incoming']
            },
            {
                'name': 'Allowing Outgoing Calls',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'dial-peer voice 11 Voip',
                        'destination-pattern 11..',
                        'session target ipv4:10.11.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 12 Voip',
                        'destination-pattern 12..',
                        'session target ipv4:10.12.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 21 Voip',
                        'destination-pattern 21..',
                        'session target ipv4:10.21.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 22 Voip',
                        'destination-pattern 22..',
                        'session target ipv4:10.22.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 31 Voip',
                        'destination-pattern 31..',
                        'session target ipv4:10.31.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 32 Voip',
                        'destination-pattern 32..',
                        'session target ipv4:10.32.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 41 Voip',
                        'destination-pattern 41..',
                        'session target ipv4:10.41.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 42 Voip',
                        'destination-pattern 42..',
                        'session target ipv4:10.42.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 51 Voip',
                        'destination-pattern 51..',
                        'session target ipv4:10.51.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 52 Voip',
                        'destination-pattern 52..',
                        'session target ipv4:10.52.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 61 Voip',
                        'destination-pattern 61..',
                        'session target ipv4:10.61.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 62 Voip',
                        'destination-pattern 62..',
                        'session target ipv4:10.62.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 71 Voip',
                        'destination-pattern 71..',
                        'session target ipv4:10.71.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 72 Voip',
                        'destination-pattern 72..',
                        'session target ipv4:10.72.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 81 Voip',
                        'destination-pattern 81..',
                        'session target ipv4:10.81.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 82 Voip',
                        'destination-pattern 82..',
                        'session target ipv4:10.82.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 91 Voip',
                        'destination-pattern 91..',
                        'session target ipv4:10.91.100.8',
                        'codec g711ULAW',
                        'dial-peer voice 92 Voip',
                        'destination-pattern 92..',
                        'session target ipv4:10.92.100.8',
                        'codec g711ULAW',
                        'end'
                    ]
                },
                'tags': ['outgoing']
            },
            {
                'name': 'Assigning a Floating Static Default Route',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'ip routing',
                        f'ip route 0.0.0.0 0.0.0.0 10.{self.m}.100.4 254',
                        'end'
                    ]
                },
                'tags': ['defroute']
            },
            {
                'name': 'Configuring OSPF',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'router ospf 1',
                        f'router-id 10.{self.m}.100.8',
                        f'network 10.{self.m}.100.0 0.0.0.255 area 0',
                        'end'
                    ]
                },
                'tags': ['ospf']
            },
            {
                'name': 'Register ePhones',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'telephony-service',
                        'create cnf-files',
                        'end'
                    ]
                },
                'tags': ['getcnf']
            }
        ]
        
        with open('cucm.yml', 'w') as file:
            self.output = yaml.safe_dump(self.cucm_config, explicit_start=True)
            file.write(self.output)
    
    def edgeRouter(self):
        self.edge_config = [
            {
                'name': 'Configuring Console Access',
                'ios_command': {
                    'commands': [
                        'conf t',
                        f'hostname edge-{self.m}',       
                        'enable secret pass',
                        'service password-encryption',
                        'no logging console',
                        'no ip domain-lookup',        
                        'line cons 0',
                        'password pass',
                        'login local',
                        'exec-timeout 0 0',
                        'end'
                    ]
                },
                'tags': ['accesscli']
            },
            {
                'name': 'Configuring IP addresses',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'int gi 0/0/0',
                        'no shut',
                        f'ip add 10.{self.m}.{self.m}.1 255.255.255.0',
                        'desc INSIDE',
                        'int gi 0/0/1',
                        'no shut',
                        f'ip add 200.0.0.{self.m} 255.255.255.0',
                        'desc OUTSIDE',
                        'int loopback 0',
                        f'ip add {self.m}.0.0.1 255.255.255.255',
                        'desc VIRTUALIP',
                        'end'
                    ]
                },
                'tags': ['interface']
            },
            {
                'name': 'Configuring Static Routes',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'ip routing',
                        'ip route 10.11.0.0 255.255.0.0 200.0.0.11 254',
                        'ip route 10.12.0.0 255.255.0.0 200.0.0.12 254',
                        'ip route 10.21.0.0 255.255.0.0 200.0.0.21 254',
                        'ip route 10.22.0.0 255.255.0.0 200.0.0.22 254',
                        'ip route 10.31.0.0 255.255.0.0 200.0.0.31 254',
                        'ip route 10.32.0.0 255.255.0.0 200.0.0.32 254',
                        'ip route 10.41.0.0 255.255.0.0 200.0.0.41 254',
                        'ip route 10.42.0.0 255.255.0.0 200.0.0.42 254',
                        'ip route 10.51.0.0 255.255.0.0 200.0.0.51 254',
                        'ip route 10.52.0.0 255.255.0.0 200.0.0.52 254',
                        'ip route 10.61.0.0 255.255.0.0 200.0.0.61 254',
                        'ip route 10.62.0.0 255.255.0.0 200.0.0.62 254',
                        'ip route 10.71.0.0 255.255.0.0 200.0.0.71 254',
                        'ip route 10.72.0.0 255.255.0.0 200.0.0.72 254',
                        'ip route 10.81.0.0 255.255.0.0 200.0.0.81 254',
                        'ip route 10.82.0.0 255.255.0.0 200.0.0.82 254',
                        f'ip route 10.{self.m}.0.0 255.255.0.0 10.{self.m}.{self.m}.4 253',
                        'end'
                    ]
                },
                'tags': ['static']
            },
            {
                'name': 'Configuring OSPF Routes',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'router ospf 1',
                        f'router-id {self.m}.0.0.1',
                        'network 200.0.0.0 0.0.0.255 area 0',
                        f'network 10.{self.m}.{self.m}.0 0.0.0.255 area 0',
                        f'network {self.m}.0.0.1 0.0.0.0 area 0',
                        'int gi 0/0/0',
                        'ip ospf network point-to-point',
                        'end'
                    ]
                },
                'tags': ['ospf']
            }
        ]
        
        with open('edge.yml', 'w') as file:
            self.output = yaml.safe_dump(self.edge_config, explicit_start=True)
            file.write(self.output)
    
    def ivrs(self):
        self.ivrs_config = [
            {
                'name': 'Assigning Dial Peer',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'dial-peer voice 69 voip',
                        'service rivanaa out-bound',
                        f'destination-pattern {self.m}69',
                        f'session target ipv4:10.{self.m}.100.8',
                        f'incoming called-number {self.m}69',
                        'dtmf-relay h245-alphanumeric',
                        'codec g711ulaw',
                        'no vad',
                        'end'
                    ]
                },
                'tags': ['dial']
            },
            {
                'name': 'Specifying Music on Hold',
                'ios_command': {
                    'commands': [
                        'conf t',
                        'telephony-service',
                        r'moh "flash:/en_bacd_music_on_hold.au"',
                        'end'
                    ]
                },
                'tags': ['moh']
            },
            {
                'name': 'Setting Application Parameters',
                'ios_command': {
                    'commands': [
                        'config t',
                        'application',
                        'service rivanaa flash:app-b-acd-aa-3.0.0.2.tcl',
                        'paramspace english index 1',
                        'param number-of-hunt-grps 2',
                        'param dial-by-extension-option 8',
                        'param handoff-string rivanaa',
                        'param welcome-prompt flash:en_bacd_welcome.au',
                        'paramspace english language en',
                        'param call-retry-timer 15',
                        'param service-name rivanqueue',
                        'paramspace english location flash:',
                        'param second-greeting-time 60',
                        'param max-time-vm-retry 2',
                        'param voice-mail 1234',
                        'param max-time-call-retry 700',
                        'param aa-pilot {self.m}69',
                        'service rivanqueue flash:app-b-acd-3.0.0.2.tcl',
                        'param queue-len 15',
                        f'param aa-hunt1 {self.m}00',
                        f'param aa-hunt2 {self.m}01',
                        f'param aa-hunt3 {self.m}77',
                        f'param aa-hunt4 {self.m}33',
                        'param queue-manager-debugs 1',
                        'param number-of-hunt-grps 4',
                        'end'
                    ]
                },
                'tags': ['app']
            }
        ]
        
        with open('ivrs.yml', 'w') as file:
            self.output = yaml.safe_dump(self.ivrs_config, explicit_start=True)
            file.write(self.output)
    
    def runAll(self):
        self.all_config = [
            {
                'name': 'CoreTaas',
                'hosts': 'ctaas',
                'gather_facts': False,
                'connection': 'local',
                'tasks': [
                    {'include_tasks': 'ctaas.yml'}
                ]
            },
            {
                'name': 'CoreBaba',
                'hosts': 'cbaba',
                'gather_facts': False,
                'connection': 'local',
                'tasks': [
                    {'include_tasks': 'cbaba.yml'}
                ]
            },
            {
                'name': 'CallManager',
                'hosts': 'cucm',
                'gather_facts': False,
                'connection': 'local',
                'tasks': [
                    {'include_tasks': 'cucm.yml'},
                    {'include_tasks': 'ivrs.yml'}
                ]
            },
            {
                'name': 'Edge',
                'hosts': 'edge',
                'gather_facts': False,
                'connection': 'local',
                'tasks': [
                    {'include_tasks': 'edge.yml'}
                ]
            }
        ]
        
        with open('run_all.yml', 'w') as file:
            self.output = yaml.safe_dump(self.all_config, explicit_start=True)
            file.write(self.output)


def promptUserInfo():
    
    monitor_num = input('What is your MONITOR NUMBER? ')
    username = input('What is the USERNAME configured on end devices? ')
    password = input('What is the PASSWORD configured on end devices? ')
    
    auth_info = {
        'monitor_num': monitor_num,
        'username': username,
        'password': password
    }
    
    return auth_info

def promptAssetInfo():
    cam_6 = input('What is the MAC Address of the camera on fa0/6? ')
    cam_8 = input('What is the MAC Address of the camera on fa0/8? ')
    ephone_1 = input('What is the MAC Address of the ephone on fa0/5? ')
    ephone_2 = input('What is the MAC Address of the ephone on fa0/7? ')
    
    asset_info = {
        'cam_6': cam_6,
        'cam_8': cam_8,
        'ephone_1': ephone_1,
        'ephone_2': ephone_2
    }
    
    return asset_info

def hostFile(monitor_num, 
             username, 
             password):
    
    m = monitor_num
    usr = username
    passw = password
    
    hosts = f'''
[ctaas]
10.{m}.1.2

[ctaas:vars]
ansible_user={usr}
ansible_password={passw}
ansible_connection=network_cli
ansible_network_os=ios


[cbaba]
10.{m}.1.4

[cbaba:vars]
ansible_user={usr}
ansible_password={passw}
ansible_connection=network_cli
ansible_network_os=ios


[cucm]
10.{m}.100.8

[cucm:vars]
ansible_user={usr}
ansible_password={passw}
ansible_connection=network_cli
ansible_network_os=ios


[edge]
10.{m}.{m}.1

[edge:vars]
ansible_user={usr}
ansible_password={passw}
ansible_connection=network_cli
ansible_network_os=ios
'''

    with open('hosts', 'w') as file:
        file.write(hosts)


if __name__ == '__main__':
    user_info = promptUserInfo()
    hostFile(**user_info)
    

    GeneratePlaybook(**user_info)
