# Network Configuration Streamlit Application

A user-friendly web interface built with Streamlit for configuring network topologies with customizable template options.

## Features

✨ **Interactive Web Interface**
- Select topology folder from your system
- Choose which configuration templates to apply
- Real-time configuration progress tracking
- Live status updates for each deployment step

📋 **Configuration Options**
- Interface configuration
- IS-IS routing protocol
- Segment Routing (SR)
- BGP configuration
- EVPN Layer 2 VPN

🔄 **Automated Workflow**
- Copies topology files automatically
- Validates device connectivity
- Applies selected configurations
- Waits for device stabilization

## Installation

### Prerequisites
- Python 3.8+
- Git

### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Make the script executable (Linux/macOS):**
   ```bash
   chmod +x run_streamlit.sh
   ```

## Usage

### Option 1: Using the Shell Script (Recommended)

**Linux/macOS:**
```bash
./run_streamlit.sh
```

**Windows:**
```bash
streamlit run src/streamlit_app.py
```

### Option 2: Direct Command

```bash
cd /home/dshaw/clabs/config_code
streamlit run src/streamlit_app.py
```

### Option 3: From Any Location

```bash
streamlit run /home/dshaw/clabs/config_code/src/streamlit_app.py
```

## Using the App

1. **Open the Application**
   - After running the command, the app will automatically open in your browser
   - Default URL: `http://localhost:8501`

2. **Configure Settings (Left Sidebar)**
   - **Base Path**: Path where your topology folders are located (default: `/home/dshaw/clabs`)
   - **Topology Folder Name**: The folder containing `.clab.yaml` (e.g., `jnpr-wtt`)

3. **Select Configuration Options (Main Area)**
   - Check/uncheck desired configuration templates
   - Available options are dynamically loaded from `config.yaml`
   - Preview shows selected configuration in YAML format

4. **Deploy Configuration**
   - Click **"Configure Topology"** button
   - Monitor real-time progress with:
     - ✅ Topology file copying
     - ✅ Configuration file reading
     - ✅ Topology conversion
     - ✅ Device connectivity
     - ✅ Configuration deployment
     - ✅ Device stabilization (30 seconds)

5. **View Results**
   - Configuration summary with metrics
   - Expandable device details section
   - Success notification with balloons animation

## Configuration Files

### `config.yaml`
Located in the working directory, defines available configuration templates:
```yaml
config:
  - interface
  - isis
  - sr
  - bgp
  - evpn_l2vpn
```

### Topology File Structure
Expected `.clab.yaml` format:
```yaml
name: topology-name
topology:
  nodes:
    R1:
      kind: juniper_vjunosrouter
      image: vrnetlab/vr-vjunosrouter:23.2R1.15
  links:
    - endpoints: ["R1:eth1", "R2:eth1"]
```

## Supported Device Types

- Juniper vJunos Router (`juniper_vjunosrouter`)
- Juniper cRPD (`juniper_crpd`)
- Cisco XRd (`cisco_xrd`)
- Arista cEOS (`ceos`)
- Linux hosts (`linux`)

## Troubleshooting

### App won't start
```bash
# Check if streamlit is installed
pip list | grep streamlit

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Connection issues
- Verify the base path exists and contains topology folders
- Check that `.clab.yaml` file is present in the specified folder
- Ensure all devices are running and reachable

### Configuration fails
- Check logs in the terminal running the Streamlit app
- Verify device credentials in `src/login/login.yaml`
- Ensure proper network connectivity to all devices

## Files Created/Modified

- `src/streamlit_app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `run_streamlit.sh` - Quick start script

## Performance Notes

- Initial connection to devices may take 30-60 seconds
- Configuration stabilization time: ~30 seconds (configurable)
- Large topologies (10+ nodes) may take 2-5 minutes total

## Advanced Options

### Custom Port
```bash
streamlit run src/streamlit_app.py --server.port 8502
```

### Disable Browser Auto-Open
```bash
streamlit run src/streamlit_app.py --logger.level=warning --client.showErrorDetails=false
```

### Run in Server Mode
```bash
streamlit run src/streamlit_app.py --server.headless true
```

## Support

For issues or questions:
1. Check terminal output for detailed error messages
2. Review configuration files for syntax errors
3. Verify device connectivity with manual SSH test
4. Check `src/login/login.yaml` for correct credentials

---
**Last Updated**: 2026-03-22
