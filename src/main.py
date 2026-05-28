import yaml,os
import shutil
from pprint import pprint
from helper.topo_convert import *
from helper.connect import *
import time

def main():
    source_file = '/home/dshaw/clabs/xrd-srte/.clab.yaml'
    shutil.copy(source_file, '.')
    yaml_data = read_yaml_file('.clab.yaml')
    config_data = read_yaml_file('config.yaml')
    device_dict = convert_topo(yaml_data,config_data)
    pprint(device_dict)
    device_dict = connect_nodes(**device_dict)
    Configure_device(**device_dict)
    time.sleep(30)
    # get_isis_adj(**device_dict)
    # get_v4_bgp_summary(**device_dict)
    # get_v6_bgp_summary(**device_dict)
        
if __name__ == "__main__":
    main()
