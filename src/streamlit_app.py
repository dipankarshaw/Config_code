import streamlit as st
import yaml
import os
import shutil
from pprint import pprint
from helper.topo_convert import *
from helper.connect import *
import time

st.set_page_config(page_title="Network Configuration", layout="wide")

st.title("🌐 Network Topology Configuration")

st.markdown("---")

# Sidebar for folder selection
st.sidebar.header("Configuration Settings")
base_path = st.sidebar.text_input(
    "Enter the base path to your topologies",
    value="/home/dshaw/clabs",
    help="Path where your topology folders are located"
)

folder_name = st.sidebar.text_input(
    "Topology Folder Name",
    value="jnpr-wtt",
    placeholder="e.g., jnpr-wtt",
    help="Folder name containing .clab.yaml"
)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Available Configuration Options")
    
    # Check if folder exists
    source_file = os.path.join(base_path, folder_name, ".clab.yaml")
    config_file = "config.yaml"
    
    if not os.path.exists(source_file):
        st.error(f"❌ Topology file not found at: {source_file}")
        st.stop()
    
    # Read current config.yaml
    try:
        with open(config_file, 'r') as f:
            current_config = yaml.safe_load(f)
        available_options = current_config.get('config', [])
    except FileNotFoundError:
        st.error(f"❌ config.yaml not found in current directory")
        st.stop()
    
    # Display available options
    st.info(f"📁 Source: `{source_file}`")
    st.write(f"Total available templates: **{len(available_options)}**")
    
    # Create checkboxes for each option
    selected_options = []
    cols = st.columns(2)
    for idx, option in enumerate(available_options):
        if isinstance(option, str):  # Skip comments
            with cols[idx % 2]:
                is_selected = st.checkbox(
                    option,
                    value=True,
                    key=f"config_{option}"
                )
                if is_selected:
                    selected_options.append(option)
    
    st.markdown("---")
    
    # Configuration preview
    st.subheader("Selected Configuration")
    if selected_options:
        preview_config = {'config': selected_options}
        st.code(yaml.dump(preview_config, default_flow_style=False), language="yaml")
    else:
        st.warning("⚠️ No configuration options selected")

with col2:
    st.subheader("Status")
    
    # Validate inputs
    if not folder_name.strip():
        st.error("Please enter a folder name")
        st.stop()
    
    if not selected_options:
        st.warning("Select at least one option to proceed")
        configure_button = st.button(
            "▶️ Configure",
            disabled=True,
            use_container_width=True,
            help="Select configuration options first"
        )
    else:
        configure_button = st.button(
            "▶️ Configure Topology",
            use_container_width=True,
            type="primary",
            help="Start configuration process"
        )

# Execute configuration
if configure_button and selected_options:
    st.subheader("📋 Configuration Output")
    
    with st.spinner("Initializing configuration..."):
        try:
            # Create a container for live output
            output_container = st.container()
            
            with output_container:
                status = st.status("Running configuration...", expanded=True)
                
                # Step 1: Copy topology file
                status.write("📋 Step 1: Copying topology file...")
                shutil.copy(source_file, '.clab.yaml')
                status.write("✅ Topology file copied")
                
                # Step 2: Read YAML files
                status.write("📖 Step 2: Reading configuration files...")
                yaml_data = read_yaml_file('.clab.yaml')
                config_data = {'config': selected_options}
                status.write(f"✅ Loaded topology: **{yaml_data.get('name', 'N/A')}**")
                
                # Step 3: Convert topology
                status.write("🔄 Step 3: Converting topology...")
                device_dict = convert_topo(yaml_data, config_data)
                num_devices = len(device_dict.get('topology', {}).get('nodes', {}))
                status.write(f"✅ Topology converted for **{num_devices} devices**")
                
                # Step 4: Connect to devices
                status.write("🔌 Step 4: Connecting to devices...")
                device_dict = connect_nodes(**device_dict)
                status.write("✅ Devices connected")
                
                # Step 5: Configure devices
                status.write("⚙️ Step 5: Configuring devices...")
                Configure_device(**device_dict)
                status.write("✅ Configuration applied to all devices")
                
                # Step 6: Wait for stabilization
                status.write("⏳ Step 6: Waiting for devices to stabilize (30 seconds)...")
                for i in range(30):
                    time.sleep(1)
                    if (i + 1) % 5 == 0:
                        status.write(f"   {i + 1}/30 seconds elapsed...")
                status.write("✅ Device stabilization complete")
                
                status.update(label="Configuration Complete! ✨", state="complete")
                
            st.success("🎉 Configuration completed successfully!")
            st.balloons()
            
            # Display summary
            st.subheader("Configuration Summary")
            summary_col1, summary_col2, summary_col3 = st.columns(3)
            
            with summary_col1:
                st.metric("Topology", yaml_data.get('name', 'N/A'))
            
            with summary_col2:
                st.metric("Devices Configured", num_devices)
            
            with summary_col3:
                st.metric("Templates Applied", len(selected_options))
            
            # Display device details
            with st.expander("📊 Device Details"):
                st.json(device_dict)
        
        except Exception as e:
            st.error(f"❌ Configuration failed: {str(e)}")
            st.exception(e)

st.markdown("---")
st.markdown("""
### 📖 How to Use:
1. Enter the base path where your topology folders are located
2. Enter the folder name (e.g., `jnpr-wtt`)
3. Select which configuration templates to apply
4. Click **Configure Topology** to deploy
5. Monitor progress in real-time as each step completes

### 📝 Configuration Templates:
- **interface**: Basic interface configuration
- **isis**: IS-IS routing protocol
- **sr**: Segment Routing
- **bgp**: BGP routing configuration
- **evpn_l2vpn**: EVPN Layer 2 VPN

*Last updated: 2026-03-22*
""")
