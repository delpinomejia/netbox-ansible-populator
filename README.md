# NetBox Ansible Populator

[![CI/CD](https://github.com/delpinomejia/netbox-ansible-populator/actions/workflows/main.yml/badge.svg)](https://github.com/delpinomejia/netbox-ansible-populator/actions/workflows/main.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ansible](https://img.shields.io/badge/Ansible-2.15%2B-red)](https://www.ansible.com/)
[![NetBox](https://img.shields.io/badge/NetBox-3.0%2B-blue)](https://netbox.dev/)

Automate the population of your NetBox instance with network infrastructure data using Ansible.

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Data Structure](#-data-structure)
- [GitHub Actions CI/CD](#-github-actions-cicd)
- [Security](#-security)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- 🚀 **Automated NetBox Population** - Bulk import sites, devices, IP addresses, and more
- 📦 **Modular Data Structure** - Organize your infrastructure data in YAML files
- 🔄 **Idempotent Operations** - Safe to run multiple times
- 🔐 **Secure Credential Handling** - Multiple secure methods for API token management
- 🎯 **CI/CD Ready** - GitHub Actions workflow included
- 📝 **Comprehensive Examples** - Sample data files with real-world examples
- 🛡️ **Validation** - Built-in linting and validation

## 📚 Prerequisites

- Python 3.8 or higher
- Ansible 2.15 or higher
- Access to a NetBox instance (3.0+)
- NetBox API token with write permissions

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/delpinomejia/netbox-ansible-populator.git
cd netbox-ansible-populator
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Ansible collections
ansible-galaxy collection install -r collections/requirements.yml
```

### 3. Configure NetBox Connection

Set your NetBox credentials using one of these methods:

#### Method 1: Environment Variables (Recommended)

```bash
export NETBOX_URL="https://netbox.example.com"
export NETBOX_TOKEN="your-api-token-here"
```

#### Method 2: Create a Token File

```bash
echo "your-api-token-here" > ~/.netbox_token
chmod 600 ~/.netbox_token
```

#### Method 3: Update group_vars (Less Secure)

Edit `group_vars/all/netbox.yml` and set your values directly (not recommended for production).

### 4. Customize Your Data

Review and modify the data files in the `data/` directory:

```bash
# Example: Edit sites configuration
vim data/sites.yml

# Example: Edit devices configuration  
vim data/devices.yml

# Example: Edit IP addresses
vim data/ip_addresses.yml
```

### 5. Run the Playbook

```bash
# Dry run (check mode)
ansible-playbook playbooks/populate.yml --check

# Actual run
ansible-playbook playbooks/populate.yml
```

## ⚙️ Configuration

### NetBox Connection Settings

The connection settings are configured in `group_vars/all/netbox.yml`:

```yaml
# NetBox API URL (can be overridden by NETBOX_URL env var)
netbox_url: "https://netbox.example.com"

# NetBox API Token (can be overridden by NETBOX_TOKEN env var)
netbox_token: "your-token-here"

# SSL Certificate Validation
netbox_validate_certs: true  # Set to false for self-signed certificates
```

### Data Files Structure

All infrastructure data is organized in YAML files under the `data/` directory:

| File | Purpose | Required |
|------|---------|----------|
| `sites.yml` | Physical locations/sites | Yes |
| `manufacturers.yml` | Hardware manufacturers | Yes |
| `device_types.yml` | Device models | Yes |
| `device_roles.yml` | Device functions/roles | Yes |
| `devices.yml` | Actual devices | Yes |
| `interfaces.yml` | Device interfaces | No |
| `ip_addresses.yml` | IP address assignments | No |

## 📊 Data Structure

### Sites Example (`data/sites.yml`)

```yaml
netbox_sites:
  - name: Main Data Center
    slug: main-dc
    status: active
    physical_address: "123 Tech Street, City, State"
    latitude: 37.7749
    longitude: -122.4194
```

### Devices Example (`data/devices.yml`)

```yaml
netbox_devices:
  - name: core-router-01
    site: Main Data Center
    device_role: Router
    device_type: ISR-4451
    manufacturer: Cisco Systems
    status: active
    serial: "SERIAL123456"
    asset_tag: "ASSET-001"
```

### IP Addresses Example (`data/ip_addresses.yml`)

```yaml
netbox_ip_addresses:
  - address: 10.0.1.1/24
    device: core-router-01
    interface: GigabitEthernet0/0
    description: "LAN Gateway"
    status: active
```

## 🎬 GitHub Actions CI/CD

This repository includes a GitHub Actions workflow that:

1. **Lints** your Ansible playbooks
2. **Validates** YAML syntax
3. **Runs** the population playbook (when configured)

### Setting up GitHub Actions

1. Go to your repository's **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:
   - `NETBOX_URL`: Your NetBox instance URL
   - `NETBOX_TOKEN`: Your NetBox API token

3. The workflow will run automatically on:
   - Push to `main` branch
   - Pull requests
   - Manual trigger (workflow_dispatch)

### Disabling Automatic Population

If you only want CI/CD for validation (not automatic population), edit `.github/workflows/main.yml` and comment out the `populate_netbox` job.

## 🔐 Security

### Best Practices

1. **Never commit credentials** to the repository
2. **Use environment variables** or GitHub Secrets for sensitive data
3. **Rotate API tokens** regularly
4. **Use read-only tokens** for testing
5. **Enable SSL verification** in production

### Secure Token Storage

For local development, create a `.env` file (already in `.gitignore`):

```bash
# .env
NETBOX_URL=https://netbox.example.com
NETBOX_TOKEN=your-token-here
```

Load it before running:

```bash
source .env  # Linux/Mac
# or
set -a; . .env; set +a  # POSIX compliant
```

## 🔧 Troubleshooting

### Common Issues

#### 1. SSL Certificate Verification Failed

```yaml
# In group_vars/all/netbox.yml, set:
netbox_validate_certs: false
```

#### 2. Authentication Failed

Check your token:
```bash
curl -H "Authorization: Token $NETBOX_TOKEN" \
     -H "Content-Type: application/json" \
     "${NETBOX_URL}/api/users/me/"
```

#### 3. Module Not Found

```bash
# Reinstall collections
ansible-galaxy collection install -r collections/requirements.yml --force
```

#### 4. Connection Timeout

- Verify NetBox URL is accessible
- Check firewall rules
- Verify proxy settings if applicable

### Debug Mode

Run with increased verbosity:
```bash
ansible-playbook playbooks/populate.yml -vvv
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
ansible-lint playbooks/*.yml

# Run tests (if available)
pytest tests/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [NetBox](https://netbox.dev/) - The amazing DCIM/IPAM solution
- [Ansible](https://www.ansible.com/) - Powerful automation platform
- Community contributors and maintainers

## 📞 Support

- 📖 [Documentation](https://github.com/delpinomejia/netbox-ansible-populator/wiki)
- 🐛 [Issue Tracker](https://github.com/delpinomejia/netbox-ansible-populator/issues)
- 💬 [Discussions](https://github.com/delpinomejia/netbox-ansible-populator/discussions)

---

**⚠️ Important:** Remember to replace `delpinomejia` with your actual GitHub username throughout this README!