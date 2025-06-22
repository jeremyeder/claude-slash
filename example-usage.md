# GitHub Init Slash Command Usage

This slash command helps you quickly initialize and configure new GitHub repositories.

**Important:** Repositories are created as **private by default** for security. Use the `--public` flag to create public repositories.

## Basic Usage

```bash
/github-init my-new-project
```

This will:
1. Create a new directory called `my-new-project`
2. Initialize a git repository
3. Create a README.md file
4. Create a **private** GitHub repository (default)
5. Push the initial commit

## Advanced Examples

### Public repository with MIT license
```bash
/github-init my-oss-project --public --license=MIT --desc="An open source project"
```

### Private Python project with gitignore
```bash
/github-init python-api --gitignore=python --topics=api,fastapi,python
```

### Public Node.js project
```bash
/github-init node-app --public --gitignore=node --topics=nodejs,typescript,express
```

### Private project with custom branch
```bash
/github-init secure-app --gitignore=python --branch=develop --license=MIT
```

### Documentation website
```bash
/github-init my-docs --create-website --public --desc="Project documentation"
```

### Full-featured project with website
```bash
/github-init awesome-project --public --create-website --gitignore=python --license=MIT --topics=python,docs,api
```

## Prerequisites

Before using this command, ensure you have:
1. Python 3.6 or higher installed
2. GitHub CLI installed: `brew install gh` (macOS) or see [GitHub CLI docs](https://cli.github.com/)
3. Authenticated with GitHub: `gh auth login`
4. Git configured with your name and email
5. Node.js 18+ (only required when using `--create-website`)

## Running the Command

You can run this command directly:
```bash
python github_init_command.py my-new-repo --public --license=MIT
```

Or make it executable:
```bash
chmod +x github_init_command.py
./github_init_command.py my-new-repo --desc="My awesome project"
```

### With Docusaurus website:
```bash
./github_init_command.py my-docs-site --create-website --public
```

This will create a complete Docusaurus site with:
- Automatic GitHub Pages deployment
- PR preview deployments  
- Modern documentation framework
- Ready-to-use CI/CD pipelines

## Integration with Claude

To use this as a slash command in Claude:
1. The command needs to be registered with Claude's command system
2. Once registered, it would be available as `/github-init` in your Claude interface
3. Claude would parse the arguments and execute the Python script

## Testing

Run the tests to ensure everything works correctly:
```bash
python -m pytest test_github_init_command.py
# or
python test_github_init_command.py
```