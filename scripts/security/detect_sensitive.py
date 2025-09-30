#!/usr/bin/env python3
"""
Pre-commit hook to detect sensitive data in files.
"""

import sys
import re
import ipaddress
from pathlib import Path
import yaml

# Patterns for sensitive data
PATTERNS = {
    'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b',
    'domain': r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b',
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'api_token': r'\b[a-zA-Z0-9_\-]{32,}\b',
    'aws_key': r'\b(?:AKIA|ASIA)[0-9A-Z]{16}\b',
    'private_key': r'-----BEGIN (?:RSA )?PRIVATE KEY-----',
}

# Allowed patterns (examples and test data)
ALLOWED = {
    'domains': [
        r'example\.com$',
        r'netbox\.example\.com$',
        r'your-domain\.com$',
        r'localhost$',
    ],
    'ip_ranges': [
        ipaddress.ip_network('192.0.2.0/24'),    # RFC 5737
        ipaddress.ip_network('198.51.100.0/24'), # RFC 5737
        ipaddress.ip_network('203.0.113.0/24'),  # RFC 5737
        ipaddress.ip_network('10.0.0.0/8'),      # RFC 1918
        ipaddress.ip_network('172.16.0.0/12'),   # RFC 1918
        ipaddress.ip_network('192.168.0.0/16'),  # RFC 1918
    ]
}

def is_allowed_domain(domain):
    """Check if domain is in allowed list."""
    return any(re.search(pattern, domain) for pattern in ALLOWED['domains'])

def is_allowed_ip(ip_str):
    """Check if IP is in allowed ranges."""
    try:
        ip = ipaddress.ip_interface(ip_str.split('/')[0])
        return any(ip.ip in network for network in ALLOWED['ip_ranges'])
    except ValueError:
        return False

def check_file(filename):
    """Check a file for sensitive data."""
    issues = []
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Check each pattern
        for pattern_name, pattern in PATTERNS.items():
            matches = re.finditer(pattern, content)
            for match in matches:
                value = match.group(0)
                
                # Skip if it's an allowed value
                if pattern_name == 'domain' and is_allowed_domain(value):
                    continue
                if pattern_name == 'ip_address' and is_allowed_ip(value):
                    continue
                    
                issues.append(f'Found potential {pattern_name}: {value}')
    
    return issues

def main():
    """Main function."""
    exit_code = 0
    
    for filename in sys.argv[1:]:
        if not Path(filename).exists():
            continue
            
        issues = check_file(filename)
        if issues:
            print(f'\nPotential sensitive data in {filename}:')
            for issue in issues:
                print(f'  - {issue}')
            exit_code = 1
    
    sys.exit(exit_code)

if __name__ == '__main__':
    main()