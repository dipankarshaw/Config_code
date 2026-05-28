import yaml,os
from pprint import pprint
from jinja2 import Environment, FileSystemLoader
import shutil

def read_yaml_file(file_path):
    """Reads a YAML file and returns its contents as a dictionary."""
    with open(file_path, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print(f"Error reading YAML file: {e}")
            return None
        

def render_template(template_name, input_dict,login_dict):
    env = Environment(loader=FileSystemLoader(f'./src/templates/{login_dict["device_type"]}'))
    template = env.get_template(template_name)
    rendered_output = template.render(input_dict)
    with open(f"./config/R{input_dict['id']}.conf", 'a') as file:
        file.write(rendered_output)
        print(f"{template_name} config generated for {login_dict['host']}")

def convert_topo(yaml_data,config_data):
    pprint(yaml_data)
    for node_name,node_data in yaml_data['topology']['nodes'].items():
        node_data['variables'] = {}
        node_data['variables']['id'] = node_name[-1]
        node_data['variables']['mesh'] = []
        node_data['variables']['l2vpn_interfaces'] = []
    for node_name,node_data in yaml_data['topology']['nodes'].items():
        for k,v in yaml_data['topology']['nodes'].items():
            if node_data['variables']['id'] == v['variables']['id']:
                pass
            else:
                node_data['variables']['mesh'].append(v['variables']['id'])
    if yaml_data is not None:
        login_data = read_yaml_file('./src/login/login.yaml')
        for node_name,node_data in yaml_data['topology']['nodes'].items():
            if node_data['kind'] not in login_data:
                continue
            node_data['login']={}
            node_data['login']['host'] = f'clab-{yaml_data["name"]}-{node_name}'
            node_data['login'].update(login_data[node_data['kind']])
            node_data['variables']['lks'] = []
            node_data['variables']['kind'] = node_data['kind']
            # Detect interfaces connecting to Linux hosts for L2VPN
            for links in yaml_data['topology']['links']:
                # Check if this link connects to a Linux host
                if node_name in links['endpoints'][0]:
                    remote_node = links['endpoints'][1].split(":")[0]
                    if remote_node in yaml_data['topology']['nodes'] and yaml_data['topology']['nodes'][remote_node].get('kind') == 'linux':
                        local_interface_name = links['endpoints'][0].split(":")[-1]
                        if node_data['kind'] == 'juniper_vjunosrouter':
                            local_interface_name = int(local_interface_name[-1]) - 1
                            local_interface_name = f'ge-0/0/{local_interface_name}'
                        node_data['variables']['l2vpn_interfaces'].append({'name': local_interface_name})
                elif node_name in links['endpoints'][1]:
                    remote_node = links['endpoints'][0].split(":")[0]
                    if remote_node in yaml_data['topology']['nodes'] and yaml_data['topology']['nodes'][remote_node].get('kind') == 'linux':
                        local_interface_name = links['endpoints'][1].split(":")[-1]
                        if node_data['kind'] == 'juniper_vjunosrouter':
                            local_interface_name = int(local_interface_name[-1]) - 1
                            local_interface_name = f'ge-0/0/{local_interface_name}'
                        node_data['variables']['l2vpn_interfaces'].append({'name': local_interface_name})
            
            # Build a set of L2VPN interface names to exclude from regular IP config
            l2vpn_interface_names = {intf['name'] for intf in node_data['variables']['l2vpn_interfaces']}
            
            for links in yaml_data['topology']['links']:
                if node_name in links['endpoints'][0]:
                    if int(node_data['variables']['id']) < int(links['endpoints'][1].split(":")[0][-1]):
                        ip_blc = f"{node_data['variables']['id']}{links['endpoints'][1].split(':')[0][-1]}"
                    else:
                        ip_blc = f"{links['endpoints'][1].split(':')[0][-1]}{node_data['variables']['id']}"
                    if node_data['kind'] == 'juniper_vjunosrouter':
                        local_interface_name = links['endpoints'][0].split(":")[-1]
                        local_interface_name = int(local_interface_name[-1]) - 1
                        local_interface_name = f'ge-0/0/{local_interface_name}'
                    else:
                        local_interface_name = links['endpoints'][0].split(":")[-1]
                    # Skip if this interface is marked for L2VPN
                    if local_interface_name not in l2vpn_interface_names:
                        node_data['variables']['lks'].append(
                                {
                                'name': local_interface_name,
                                'des':links['endpoints'][1],
                                'r_id': links['endpoints'][1].split(":")[0][-1],
                                'ip_blc': ip_blc
                                }
                            )
                elif node_name in links['endpoints'][1]:
                    if int(node_data['variables']['id']) < int(links['endpoints'][0].split(":")[0][-1]):
                        ip_blc = f"{node_data['variables']['id']}{links['endpoints'][0].split(':')[0][-1]}"
                    else:
                        ip_blc = f"{links['endpoints'][0].split(':')[0][-1]}{node_data['variables']['id']}"
                    if node_data['kind'] == 'juniper_vjunosrouter':
                        local_interface_name = links['endpoints'][1].split(":")[-1]
                        local_interface_name = int(local_interface_name[-1]) - 1
                        local_interface_name = f'ge-0/0/{local_interface_name}'
                    else:
                        local_interface_name = links['endpoints'][1].split(":")[-1]
                    # Skip if this interface is marked for L2VPN
                    if local_interface_name not in l2vpn_interface_names:
                        node_data['variables']['lks'].append(
                                {
                                'name': local_interface_name,
                                'des':links['endpoints'][0],
                                'r_id': links['endpoints'][0].split(":")[0][-1],
                                'ip_blc': ip_blc
                                }
                            )
                else:
                    pass
            try:
                os.remove(f"./config/R{node_data['variables']['id']}.conf")
            except FileNotFoundError:
                print("file was not found create the file")
            for items in config_data['config']:
                render_template(f'{items}.j2', node_data['variables'],node_data['login'])
            print("**** \n")
    return yaml_data