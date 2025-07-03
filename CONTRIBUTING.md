# Contributing to claude-slash

Thank you for your interest in contributing to claude-slash! This document provides guidelines for contributing to this project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or fix
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/claude-slash.git
cd claude-slash

# Create a new branch
git checkout -b feature/your-feature-name

# Make your changes
# ...

# Test your changes
./tests/test_commands.sh

# Commit and push
git commit -m "Add your feature"
git push origin feature/your-feature-name
```

## Creating New Commands

### Command File Structure

All commands should follow this structure:

```markdown
# Command Name

Brief description of what the command does.

## Usage
\```
/project:command-name [arguments]
\```

## Description
Detailed description of the command functionality.

## Implementation

!# Your shell commands here
!echo "Hello, world!"
```

### Guidelines

1. **Naming**: Use descriptive names and provide aliases for common operations
2. **Documentation**: Include comprehensive usage examples
3. **Security**: Never include dangerous operations (rm -rf, sudo, etc.)
4. **Testing**: Test commands thoroughly before submitting
5. **Error Handling**: Handle edge cases gracefully

### Command Best Practices

- Use `git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")` to find repository root
- Store outputs in the git repository when possible
- Provide clear status messages to users
- Use `$ARGUMENTS` for user-provided arguments
- Include error handling for missing dependencies

## Testing

Before submitting a pull request:

1. Run the test suite:
   ```bash
   ./tests/test_commands.sh
   ```

2. Test your commands manually in a Claude Code session

3. Ensure all GitHub Actions checks pass

## Code Review Process

1. All submissions require review
2. We may suggest changes or improvements
3. Once approved, maintainers will merge your PR

## Reporting Issues

- Use GitHub Issues for bug reports and feature requests
- Include detailed reproduction steps
- Mention your operating system and Claude Code version

## Security

- Never include secrets, API keys, or sensitive data
- Avoid commands that could harm the user's system
- Review the security implications of shell commands

## Style Guide

### Markdown
- Use consistent heading levels
- Include code blocks with proper syntax highlighting
- Keep lines under 80 characters when possible

### Shell Scripts
- Use `set -e` for error handling
- Quote variables properly
- Use descriptive variable names
- Include comments for complex logic

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Include detailed description if necessary

## License

By contributing to claude-slash, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue if you have questions about contributing!

---

*Thank you for contributing to claude-slash! 🚀*