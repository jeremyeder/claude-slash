# Example Command - Development Template

Example command to test the command discovery system with Rich formatting and demonstrate best practices for creating new claude-slash commands.

## Usage

Test the command discovery system with custom messages:

```bash
/example                           # Default hello message
/example --message "Custom text"   # Custom message
claude-slash example               # CLI mode
```

## Description

The Example command serves as both a functional test for the command discovery system and a template for developers creating new commands. It demonstrates proper BaseCommand inheritance, custom argument handling, and Rich-formatted output.

### Key Features

- **Command Discovery Testing**: Verifies automatic command registration works
- **Rich Formatting**: Demonstrates proper use of Rich terminal formatting
- **Custom Arguments**: Shows how to implement optional command arguments
- **Error Handling**: Includes proper error handling patterns
- **Template Pattern**: Serves as copy/paste template for new commands

### Command Structure

This command demonstrates the standard claude-slash command pattern:

1. **BaseCommand Inheritance**: Extends BaseCommand for consistent behavior
2. **Property Methods**: Implements `name` and `help_text` properties
3. **Execute Method**: Contains core command logic with kwargs handling
4. **Typer Integration**: Creates proper Typer command wrapper
5. **Rich Output**: Uses Rich formatting for success messages

## Implementation

This command is implemented as a Python class in `src/claude_slash/commands/example.py` that integrates with the Typer CLI framework and Rich terminal UI library.

### Technical Details

- **Framework**: Python with Typer/Rich
- **Arguments**: Optional `--message` parameter with default value
- **Output**: Rich-formatted success messages
- **Error Handling**: Comprehensive error handling with user feedback
- **Discovery**: Automatically discovered by command loading system

### Code Pattern

```python
class ExampleCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "example"

    @property
    def help_text(self) -> str:
        return "Command description with examples..."

    def execute(self, **kwargs: Any) -> None:
        # Command logic here
        self.success("Command completed successfully")

    def create_typer_command(self):
        # Typer command wrapper with arguments
        def command_wrapper(arg: str = typer.Option(default, help="Description")):
            self.execute(arg=arg)
        return command_wrapper
```

### Dependencies

- Python 3.13+
- Rich library for terminal formatting
- Typer for CLI argument handling
- BaseCommand from claude-slash framework

## Examples

### Basic Usage
```bash
# Default message
/example
# Output: ✅ Example command executed with message: Hello, World!

# Custom message
/example --message "Testing the system"
# Output: ✅ Example command executed with message: Testing the system
```

### Development Template

Developers can copy this command structure to create new commands:

1. Copy `example.py` to new command file
2. Update class name and command name
3. Implement custom `execute()` logic
4. Update help text and arguments
5. Create corresponding markdown file in `.claude/commands/`

## Related Commands

- `/menuconfig` - TUI editor for CLAUDE.md
- `/learn` - Interactive learning integration
- `/github-init` - Repository initialization
- Other development workflow commands

## Notes

- Serves as both functional test and development template
- Demonstrates proper Rich formatting usage
- Shows standard error handling patterns
- Automatically discovered by command loading system
- Safe to run - only displays messages, makes no changes
