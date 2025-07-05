Output claude-slash-demo.gif

Set FontSize 32
Set Width 1200
Set Height 600
Set TypingSpeed 0.1
Set Theme "Catppuccin Frappe"
Set Padding 20

Type "# 🚀 claude-slash v1.2.0"
Enter
Sleep 800ms

Type "curl -sSL https://raw.githubusercontent.com/jeremyeder/claude-slash/main/install.sh | bash"
Enter
Sleep 1200ms

Type "# ✅ Commands installed!"
Enter
Sleep 600ms

Type "echo 'Working on feature...' > feature.py"
Enter
Type "/project:checkpoint 'Before refactor'"
Enter
Sleep 1s

Type "# Checkpoint created! 📋"
Enter
Sleep 800ms

Type "echo 'Oops, broke it!' > feature.py"
Enter
Type "/project:restore"
Enter
Sleep 1s

Type "# ✨ Restored! Never lose progress again."
Enter
Sleep 800ms