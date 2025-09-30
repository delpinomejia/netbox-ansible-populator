# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please send an email to security@your-domain.com. All security vulnerabilities will be promptly addressed.

## Security Best Practices

### API Token Management
- Never commit API tokens or credentials to the repository
- Use environment variables for sensitive data
- Store tokens in secure credential stores
- Rotate API tokens regularly
- Use read-only tokens for testing environments

### Local Development
1. Use `.env` files (included in `.gitignore`) for local credentials:
```bash
# .env example
NETBOX_URL=https://netbox.example.com
NETBOX_TOKEN=your-token-here
```

2. Secure token file permissions:
```bash
# If using token file
echo "your-token-here" > ~/.netbox_token
chmod 600 ~/.netbox_token
```

3. Use secure environment variables:
```bash
# Preferred method
export NETBOX_TOKEN="your-token-here"
```

### CI/CD Security
- Use GitHub Secrets or equivalent for CI/CD credentials
- Implement the principle of least privilege
- Regular audit of GitHub Actions workflows
- Enable required status checks for protected branches

### Data Security
- All example data must use:
  - Reserved IP ranges (RFC 5737)
  - Example domains (RFC 2606)
  - Generic device names and locations
  - Fictional organization names
- Never commit real infrastructure data

### Pre-commit Checks
This repository includes pre-commit hooks that check for:
- Hardcoded credentials
- Real IP addresses
- Real domain names
- Personal information
- Infrastructure-specific data

### SSL/TLS Security
- Always validate SSL certificates in production
- Only disable SSL verification in development with self-signed certificates
- Document any SSL verification changes

## Security Controls

### Required
- [ ] Environment variables for credentials
- [ ] Protected main branch
- [ ] Code review requirements
- [ ] Pre-commit hooks
- [ ] Security scanning in CI/CD

### Recommended
- [ ] Dependabot alerts
- [ ] Regular dependency updates
- [ ] Automated security scanning
- [ ] Contributor security guidelines

## Compliance

### Data Privacy
- Do not include personal information
- Use placeholder data for examples
- Comply with relevant data protection regulations

### Access Control
- Use role-based access control in NetBox
- Implement principle of least privilege
- Regular access review

## Updates and Maintenance
This security policy is reviewed and updated regularly. Last update: September 2025