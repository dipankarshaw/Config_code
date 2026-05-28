# Network Configuration Code

An automated network configuration management system that uses Jinja2 templates to generate device configurations and deploy them to multi-vendor network topologies using Containerlab.

## Overview

This project automates the configuration of network devices across multiple vendors (Cisco IOS-XR, Juniper Junos, Arista EOS) through a combination of:
- **Topology parsing** from Containerlab YAML files
- **Jinja2 template-based configuration generation** for different device types
- **Automated device connectivity and configuration deployment** using Netmiko
- **Web-based UI** (Streamlit) for interactive configuration management

## Key Features

✨ **Multi-Vendor Support**
- Cisco IOS-XR (cisco_xr)
- Juniper Junos (juniper_junos)
- Arista EOS (arista_eos)

📋 **Configuration Options**
- Interface configuration
- IS-IS routing protocol
- MPLS Traffic Engineering (MPLS-TE)
- Segment Routing (SR)
- BGP configuration
- EVPN Layer 2 VPN
- Layer 3 VPN

🔧 **Automation Capabilities**
- Parse Containerlab topology files (.clab.yaml)
- Generate device-specific configurations from templates
- Connect to devices via SSH (Netmiko)
- Deploy configurations automatically
- Validate device connectivity
- Query network device status (ISIS adjacencies, BGP summaries)

## Project Structure

```
├── src/
│   ├── main.py                 # CLI entry point
│   ├── streamlit_app.py        # Web UI for configuration management
│   ├── config.yaml             # Configuration options
│   ├── topo.yaml               # Topology configuration
│   ├── helper/
│   │   ├── topo_convert.py     # Topology parsing and template rendering
│   │   └── connect.py          # Device connectivity and configuration deployment
│   ├── login/
│   │   └── login.yaml          # Device login credentials
│   └── templates/
│       ├── arista_eos/         # Arista configuration templates
│       ├── cisco_xr/           # Cisco IOS-XR configuration templates
│       └── juniper_junos/      # Juniper Junos configuration templates
├── config/                      # Generated device configurations
│   ├── R1.conf
│   ├── R2.conf
│   └── ...
├── docs/                        # Documentation
├── tests/                       # Test files
├── requirements.txt             # Python dependencies
├── config.yaml                  # Global configuration
├── run_streamlit.sh            # Streamlit launcher script
└── README.md                    # This file
```

## Installation

### Prerequisites
- Python 3.8+
- Git
- Access to network devices (or Containerlab setup)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dipankarshaw/Config_code.git
   cd Config_code
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure device login credentials:**
   Edit `src/login/login.yaml` with your device credentials:
   ```yaml
   cisco_xr:
     device_type: cisco_xr
     username: admin
     password: admin
     secret: admin
     port: 22
   ```

4. **Configure topology path:**
   Edit `src/config.yaml` to specify which configurations to deploy

## Usage

### Option 1: Using the Streamlit Web UI (Recommended)

**Start the application:**
```bash
./run_streamlit.sh
```

Then open your browser and navigate to `http://localhost:8501`

**Features:**
- Select topology folder from your system
- Choose which configuration templates to apply
- Real-time progress tracking
- Live status updates for each deployment step

### Option 2: Using the CLI

**Run the main script:**
```bash
cd src
python main.py
```

This will:
1. Read the topology from `.clab.yaml`
2. Parse configuration options from `config.yaml`
3. Generate device-specific configurations from Jinja2 templates
4. Connect to each device via SSH
5. Deploy the generated configurations
6. Wait for device stabilization (30 seconds)

### Option 3: Running Individual Operations

```python
from helper.topo_convert import convert_topo, read_yaml_file
from helper.connect import connect_nodes, Configure_device

# Load and parse topology
yaml_data = read_yaml_file('.clab.yaml')
config_data = read_yaml_file('config.yaml')
device_dict = convert_topo(yaml_data, config_data)

# Connect and configure devices
device_dict = connect_nodes(**device_dict)
Configure_device(**device_dict)
```

## Configuration Templates

### Template Variables

The Jinja2 templates receive device-specific variables:

- `id` - Device identifier (extracted from device name)
- `kind` - Device type (cisco_xr, juniper_junos, arista_eos)
- `mesh` - List of peer device IDs for mesh topology
- `l2vpn_interfaces` - Interfaces connecting to L2VPN endpoints
- `lks` - Link state tracking list

### Example Template Usage

```jinja2
! Interface Configuration for R{{ id }}
{% for interface in interfaces %}
interface {{ interface.name }}
  ip address {{ interface.ip }} {{ interface.mask }}
{% endfor %}
```

## Dependencies

- **streamlit** - Web UI framework
- **pyyaml** - YAML file parsing
- **jinja2** - Template engine
- **paramiko** - SSH library (via netmiko)
- **netmiko** - Multi-vendor device connectivity

## Supported Commands

The system can execute various network commands:

- `show isis adjacencies` - Display ISIS neighbors
- `show bgp ipv4 unicast summary` - BGP IPv4 summary
- `show bgp ipv6 unicast summary` - BGP IPv6 summary

Commands are automatically adapted based on device type (Cisco, Arista, Juniper).

## Development

### Adding a New Vendor

1. Create a new template directory: `src/templates/vendor_name/`
2. Add Jinja2 templates for each configuration type
3. Update `src/login/login.yaml` with vendor credentials
4. Update `src/helper/connect.py` to handle vendor-specific commands

### Adding a New Configuration Type

1. Create a Jinja2 template in the appropriate vendor directory
2. Add the template name to `config.yaml`
3. The system will automatically render and deploy it

## Troubleshooting

### Connection Issues
- Verify device credentials in `src/login/login.yaml`
- Ensure devices are reachable via SSH
- Check firewall rules and port access (default: 22)

### Template Rendering Errors
- Verify template syntax in Jinja2 files
- Check that required variables are provided in topology
- Review generated config files in `config/` directory

### Configuration Deployment Failures
- Check device-specific command syntax
- Verify configuration doesn't conflict with existing settings
- Review device logs for detailed error messages

## Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- New features include appropriate documentation
- Templates are tested on actual devices

## License

MIT License

## Author

Dipankar Shaw

## Repository

https://github.com/dipankarshaw/Config_code