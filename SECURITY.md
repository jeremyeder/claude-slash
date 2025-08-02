# Security Policy

## Supported Versions

We support the latest version of claude-slash. Security updates are applied to the main branch.

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Security Considerations

### Command Execution
- All commands are executed in your local environment
- Commands run with your user permissions
- No external network calls without explicit user consent
- All data stays local to your git repository

### Safe Command Design
Commands in this repository are designed to be safe:
- No destructive operations (rm -rf, format, etc.)
- No privilege escalation (sudo, su, etc.)
- No automatic execution of downloaded code
- No hardcoded credentials or secrets

### Data Privacy
- Checkpoint data is stored locally in your git repository
- No data is transmitted to external servers
- Session information includes only basic environment details
- No sensitive information is captured or stored

## Reporting Security Issues

If you discover a security vulnerability, please report it responsibly:

1. **Do NOT** open a public issue
2. Email security concerns to: [jeremy.eder@gmail.com]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

## Security Best Practices

### For Users
- Review command implementations before installation
- Only install commands from trusted sources
- Keep your git repository private if it contains sensitive data
- Regularly review checkpoint files for any sensitive information

### For Contributors
- Never include hardcoded secrets or credentials
- Avoid commands that could harm the user's system
- Use safe shell practices (proper quoting, error handling)
- Test commands in isolated environments first

## Acknowledgments

We appreciate responsible disclosure of security issues and will acknowledge contributors who help improve the security of this project.

## Questions?

If you have questions about security that don't constitute a vulnerability report, please open a regular GitHub issue.

---

*Security is everyone's responsibility. Thank you for helping keep claude-slash secure! 🔒*
