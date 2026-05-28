from netmiko import ConnectHandler
from getpass import getpass
def connect_nodes(**device_dict):
    for nodes,nodes_data in device_dict['topology']['nodes'].items():
        if 'login' not in nodes_data:
            continue
        nodes_data['conn_obj'] = ConnectHandler(**nodes_data['login'])
        nodes_data['conn_obj'].enable()  # Enter enable mode if required
        prompt = nodes_data['conn_obj'].find_prompt()
        print(f"Connected to {prompt}")
        # Execute a command
        # output = net_connect.send_command("show version")
        # print(output)
    return device_dict
def Configure_device(**device_dict):
    for nodes,nodes_data in device_dict['topology']['nodes'].items():
        if 'login' not in nodes_data:
            continue
        with open(f'./config/{nodes}.conf', 'r') as file:
            config_commands = file.readlines()
            # print(config_commands)
        nodes_data['conn_obj'].send_config_set(config_commands)
        if 'cisco' in nodes_data['login']['device_type']:
            nodes_data['conn_obj'].commit()
        elif 'arista' in nodes_data['login']['device_type']:
            nodes_data['conn_obj'].save_config()
        elif 'junos' in nodes_data['login']['device_type']:
            nodes_data['conn_obj'].commit()

def get_isis_adj(**device_dict):
    for nodes,nodes_data in device_dict['topology']['nodes'].items():
        print(f"\n***** {nodes_data['login']['host']}*******")
        if 'cisco' in nodes_data['login']['device_type']:
            command="show isis adj"
            output = nodes_data['conn_obj'].send_command(command)
        elif 'arista' in nodes_data['login']['device_type']:
            command="show isis neighbors"
            output = nodes_data['conn_obj'].send_command(command)
        print(output)

def get_v4_bgp_summary(**device_dict):
    for nodes,nodes_data in device_dict['topology']['nodes'].items():
        print(f"\n***** {nodes_data['login']['host']}*******")
        if 'cisco' in nodes_data['login']['device_type']:
            command="show bgp ipv4 unicast summary"
            output = nodes_data['conn_obj'].send_command(command)
        elif 'arista' in nodes_data['login']['device_type']:
            command="show bgp ipv4 unicast summary"
            output = nodes_data['conn_obj'].send_command(command)
        print(output)

def get_v6_bgp_summary(**device_dict):
    for nodes,nodes_data in device_dict['topology']['nodes'].items():
        print(f"\n***** {nodes_data['login']['host']}*******")
        if 'cisco' in nodes_data['login']['device_type']:
            command="show bgp ipv6 unicast summary | in 100"
            output = nodes_data['conn_obj'].send_command(command)
        elif 'arista' in nodes_data['login']['device_type']:
            command="show bgp ipv6 unicast summary"
            output = nodes_data['conn_obj'].send_command(command)
        print(output)