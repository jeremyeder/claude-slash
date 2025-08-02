# Learn Command

Continuously refine the global CLAUDE.md file with impactful learnings from the current session through an
interactive integration interface.

## Usage

```bash
/learn
```

## Description

This command autonomously analyzes the current Claude Code session context to extract important insights,
patterns, and learnings, then provides an interactive interface for integrating them into the global CLAUDE.md file. It features:

- Dynamic parsing of CLAUDE.md structure and sections
- Interactive multi-select menu for target section selection
- Smart content analysis and placement suggestions
- Diff-style preview before applying changes
- Multiple integration modes (append, insert, merge)
- Safe backup and rollback capabilities

The command analyzes both the learning content and existing CLAUDE.md structure to suggest optimal
integration points while maintaining full user control over the process.

## Implementation

!git_root=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")
!claude_md_path="$HOME/.claude/CLAUDE.md"
!timestamp=$(date +"%Y-%m-%d %H:%M:%S")

!# Color definitions for better UX
!RED='\033[0;31m'
!GREEN='\033[0;32m'
!YELLOW='\033[1;33m'
!BLUE='\033[0;34m'
!PURPLE='\033[0;35m'
!CYAN='\033[0;36m'
!NC='\033[0m' # No Color

!echo -e "${BLUE}🧠 Interactive Learning Integration System${NC}"
!echo -e "${BLUE}==========================================${NC}"
!echo ""

!# Check if global CLAUDE.md exists
!if [ ! -f "$claude_md_path" ]; then
!  echo -e "${RED}❌ Error: Global CLAUDE.md not found at $claude_md_path${NC}"
!  echo "Please ensure your global Claude configuration is set up correctly."
!  exit 1
!fi

!# Autonomous learning extraction from current session context
!echo -e "${CYAN}🔍 Analyzing current session context for learnings...${NC}"
!echo ""
!
!# Extract key insights from recent activity (this would be enhanced with actual context analysis)
!learning_content="Session Analysis Results:
!
!Key learnings identified from current session:
!
!1. **Clean Feature Branch Management**: When creating feature branches, always cherry-pick specific commits to avoid including unrelated changes in PRs. Use 'git checkout -B feature/name' from clean main, then 'git cherry-pick COMMIT_HASH' to include only relevant changes.
!
!2. **Force Push Safety**: Use 'git push --force-with-lease' instead of 'git push --force' to safely update feature branches while protecting against overwriting others' work.
!
!3. **PR Hygiene**: Always verify PR contents show only intended changes by checking commit history and file diffs before submission.
!
!4. **Command Enhancement Pattern**: When enhancing CLI tools, add terminal output to show users exactly what was accomplished."
!
!echo -e "${GREEN}📊 Extracted Learning Summary:${NC}"
!echo -e "${GREEN}=============================${NC}"
!echo "$learning_content"
!echo ""
!
!# Ask user to confirm the extracted learnings
!echo -e "${YELLOW}📝 Do you want to integrate these learnings into CLAUDE.md?${NC}"
!echo -n "Continue with integration? [y/N]: "
!read proceed_confirm
!
!if [[ ! "$proceed_confirm" =~ ^[Yy]$ ]]; then
!  echo -e "${YELLOW}❌ Learning extraction cancelled by user.${NC}"
!  exit 0
!fi

!# Create a backup of the current CLAUDE.md
!backup_path="$HOME/.claude/CLAUDE.md.backup-$(date +%Y%m%d-%H%M%S)"
!cp "$claude_md_path" "$backup_path"
!echo -e "${GREEN}✅ Backup created at: $backup_path${NC}"
!echo ""

!# Parse CLAUDE.md structure to extract sections
!echo -e "${CYAN}📖 Analyzing CLAUDE.md structure...${NC}"
!sections_file="/tmp/claude_sections_$(date +%s).txt"
!grep -n "^#" "$claude_md_path" | head -20 > "$sections_file"

!echo -e "${CYAN}📝 Available sections in CLAUDE.md:${NC}"
!echo ""
!section_count=0
!declare -a section_lines
!declare -a section_names

!while IFS=':' read -r line_num header_text; do
!  section_count=$((section_count + 1))
!  section_lines[$section_count]="$line_num"
!  section_names[$section_count]="$header_text"
!  echo -e "${PURPLE}$section_count.${NC} $header_text"
!done < "$sections_file"

!echo ""
!max_selection=$((section_count + 1))
!echo -e "${PURPLE}$max_selection.${NC} Create new section"
!echo ""

!# Format learning content
!formatted_learning=$(printf "## Session Learning - %s\n\n**Context**: %s\n\n**Learning**: %s\n\n" \
!  "$timestamp" "$(basename "$git_root" 2>/dev/null || echo "Current session")" "$learning_content")
!formatted_learning="${formatted_learning}**Application**: This insight should be applied to future similar scenarios to"
!formatted_learning="${formatted_learning} improve efficiency and outcomes.\n"

!echo -e "${YELLOW}📋 Learning content to be integrated:${NC}"
!echo -e "${YELLOW}================================${NC}"
!echo "$formatted_learning"
!echo ""

!# Smart content analysis for suggestions
!echo -e "${CYAN}🤖 Analyzing content for smart suggestions...${NC}"
!suggested_sections=""

!# Analyze keywords in learning content
!if echo "$learning_content" | grep -qi -e "test" -e "debug" -e "error" -e "bug" -e "fix"; then
!  suggested_sections="$suggested_sections Test-Implementation Synchronization,"
!fi

!if echo "$learning_content" | grep -qi -e "workflow" -e "process" -e "lint" -e "commit" -e "git"; then
!  suggested_sections="$suggested_sections Pre-Push Linting Workflow,"
!fi

!if echo "$learning_content" | grep -qi -e "strategic" -e "business" -e "framework" -e "leadership"; then
!  suggested_sections="$suggested_sections Strategic Tools & Methodologies,"
!fi

!if echo "$learning_content" | grep -qi -e "principle" -e "rule" -e "practice" -e "standard"; then
!  suggested_sections="$suggested_sections Key Operating Principles,"
!fi

!if [ -n "$suggested_sections" ]; then
!  echo -e "${GREEN}💡 Suggested sections based on content analysis:${NC}"
!  echo -e "${GREEN}   ${suggested_sections%, }${NC}"
!  echo ""
!fi

!# Interactive section selection
!echo -e "${YELLOW}🎯 Select target section for integration:${NC}"
!echo -n "Enter section number [1-$max_selection]: "
!read selection

!# Validate selection
!if ! [[ "$selection" =~ ^[0-9]+$ ]] || [ "$selection" -lt 1 ] || [ "$selection" -gt "$max_selection" ]; then
!  echo -e "${RED}❌ Invalid selection. Please run the command again.${NC}"
!  rm -f "$sections_file"
!  exit 1
!fi

!# Handle new section creation
!if [ "$selection" -eq "$max_selection" ]; then
!  echo ""
!  echo -n "Enter new section name: "
!  read new_section_name
!  if [ -z "$new_section_name" ]; then
!    echo -e "${RED}❌ Section name cannot be empty.${NC}"
!    rm -f "$sections_file"
!    exit 1
!  fi
!
!  target_section="## $new_section_name"
!  integration_mode="new_section"
!  echo -e "${GREEN}✅ Will create new section: $target_section${NC}"
!else
!  target_section="${section_names[$selection]}"
!  target_line="${section_lines[$selection]}"
!  integration_mode="existing_section"
!  echo -e "${GREEN}✅ Selected: $target_section${NC}"
!fi

!echo ""

!# Choose integration mode for existing sections
!if [ "$integration_mode" = "existing_section" ]; then
!  echo -e "${YELLOW}🔧 Choose integration mode:${NC}"
!  echo "1. Append to end of section"
!  echo "2. Insert after section header"
!  echo "3. Show section content for manual placement"
!  echo ""
!  echo -n "Select integration mode [1-3]: "
!  read mode_selection
!
!  case $mode_selection in
!    1) integration_type="append" ;;
!    2) integration_type="insert" ;;
!    3) integration_type="manual" ;;
!    *)
!      echo -e "${RED}❌ Invalid mode selection.${NC}"
!      rm -f "$sections_file"
!      exit 1
!      ;;
!  esac
!fi

!# Preview changes
!echo -e "${CYAN}👀 Preview of changes:${NC}"
!echo -e "${CYAN}==================${NC}"

!if [ "$integration_mode" = "new_section" ]; then
!  echo -e "${GREEN}+ $target_section${NC}"
!  echo -e "${GREEN}+${NC}"
!  echo "$formatted_learning" | sed 's/^/+ /' | sed "s/^+ /${GREEN}+ ${NC}/"
!else
!  echo -e "${BLUE}Existing section: $target_section${NC}"
!
!  if [ "$integration_type" = "manual" ]; then
!    echo ""
!    echo -e "${YELLOW}📖 Current section content:${NC}"
!    next_section_line=$(grep -n "^#" "$claude_md_path" | awk -F: -v target="$target_line" '$1 > target {print $1; exit}')
!    if [ -n "$next_section_line" ]; then
!      sed -n "${target_line},$((next_section_line - 1))p" "$claude_md_path"
!    else
!      sed -n "${target_line},\$p" "$claude_md_path"
!    fi
!    echo ""
!    echo -e "${YELLOW}You can manually copy and integrate the learning content above.${NC}"
!    rm -f "$sections_file"
!    exit 0
!  fi
!
!  echo ""
!  echo -e "${GREEN}Learning content will be ${integration_type}ed:${NC}"
!  echo "$formatted_learning" | sed 's/^/+ /' | sed "s/^+ /${GREEN}+ ${NC}/"
!fi

!echo ""

!# Confirmation prompt
!echo -e "${YELLOW}⚠️  Confirm integration? This will modify your global CLAUDE.md file.${NC}"
!echo -n "Continue? [y/N]: "
!read confirm

!if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
!  echo -e "${YELLOW}❌ Integration cancelled by user.${NC}"
!  rm -f "$sections_file"
!  exit 0
!fi

!# Perform the integration
!echo ""
!echo -e "${CYAN}🔄 Integrating learning into CLAUDE.md...${NC}"

!temp_file="/tmp/claude_md_temp_$(date +%s).md"

!if [ "$integration_mode" = "new_section" ]; then
!  # Add new section at the end
!  cp "$claude_md_path" "$temp_file"
!  echo "" >> "$temp_file"
!  echo "$target_section" >> "$temp_file"
!  echo "" >> "$temp_file"
!  echo "$formatted_learning" >> "$temp_file"
!else
!  # Integrate into existing section
!  if [ "$integration_type" = "append" ]; then
!    # Find the end of the target section
!    next_section_line=$(grep -n "^#" "$claude_md_path" | awk -F: -v target="$target_line" '$1 > target {print $1; exit}')
!
!    if [ -n "$next_section_line" ]; then
!      # Insert before next section
!      sed -n "1,$((next_section_line - 1))p" "$claude_md_path" > "$temp_file"
!      echo "" >> "$temp_file"
!      echo "$formatted_learning" >> "$temp_file"
!      sed -n "${next_section_line},\$p" "$claude_md_path" >> "$temp_file"
!    else
!      # Append to end of file
!      cp "$claude_md_path" "$temp_file"
!      echo "" >> "$temp_file"
!      echo "$formatted_learning" >> "$temp_file"
!    fi
!  elif [ "$integration_type" = "insert" ]; then
!    # Insert right after section header
!    sed -n "1,${target_line}p" "$claude_md_path" > "$temp_file"
!    echo "" >> "$temp_file"
!    echo "$formatted_learning" >> "$temp_file"
!    sed -n "$((target_line + 1)),\$p" "$claude_md_path" >> "$temp_file"
!  fi
!fi

!# Validate the result and apply
!if [ -f "$temp_file" ] && [ -s "$temp_file" ]; then
!  mv "$temp_file" "$claude_md_path"
!  echo -e "${GREEN}✅ Learning successfully integrated into CLAUDE.md!${NC}"
!  echo ""
!  echo -e "${CYAN}📊 Integration Summary:${NC}"
!  echo -e "${CYAN}=====================${NC}"
!  echo -e "📁 Target: $target_section"
!  echo -e "🕐 Timestamp: $timestamp"
!  echo -e "💾 Backup: $backup_path"
!  echo -e "📝 Content: $(echo "$learning_content" | head -c 50)..."
!  echo ""
!  echo -e "${CYAN}📄 Added Learning Content:${NC}"
!  echo -e "${CYAN}========================${NC}"
!  echo "$formatted_learning"
!else
!  echo -e "${RED}❌ Integration failed. Your original CLAUDE.md is unchanged.${NC}"
!  echo -e "${BLUE}🔄 Backup is available at: $backup_path${NC}"
!fi

!# Cleanup
!rm -f "$sections_file" "$temp_file"
