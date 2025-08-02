# Contributing to claude-slash

## Pull Request Guidelines

### Linking Issues

Always link your PR to related issues using GitHub's automatic closing keywords:

**For bug fixes:**
```
Fixes #123
Closes #456
```

**For features:**
```
Resolves #789
Implements #012
```

**Multiple issues:**
```
Fixes #123, fixes #456, resolves #789
```

### Closing Keywords

These keywords automatically close issues when PRs merge to the main branch:

- `close`, `closes`, `closed`
- `fix`, `fixes`, `fixed`
- `resolve`, `resolves`, `resolved`

### Cross-Repository Issues

To close issues in other repositories:
```
Fixes username/repo#123
```

## Commit Message Guidelines

Include issue references in commit messages:
```bash
git commit -m "Fix API timeout handling

Resolves #123 by implementing exponential backoff
for network requests.

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Automation Features

### Automatic Issue Closing
- ✅ **Enabled by default** - No configuration needed
- ✅ **Works on main branch merges** only
- ✅ **Supports multiple issues** per PR
- ✅ **Cross-repository support** with proper syntax

### Issue Management Workflow
- 🔍 **Link checker** - Warns if PRs don't reference issues
- 🏷️ **Stale issue management** - Auto-marks inactive issues
- 📋 **PR template** - Guides proper issue linking

## Best Practices

1. **Create issues first** - Document the problem before the solution
2. **Use descriptive titles** - Help others understand the change
3. **Reference issues early** - Add keywords in initial PR description
4. **Test automation** - Verify issues close correctly after merge
5. **Update documentation** - Keep automation guidelines current

## Troubleshooting

**Issue not closing?**
- ✅ Check the keyword is in PR description (not just title)
- ✅ Verify PR merged to the default branch (main)
- ✅ Confirm issue number is correct
- ✅ Ensure no typos in closing keywords

**Need to prevent auto-closing?**
- Use different language: "Related to #123" or "See #123"
- Only `closes`/`fixes`/`resolves` trigger automation
