import re

# Read the original file
with open("vibot/commands/comment.py", "r", encoding="utf-8") as f:
    content = f.read()

# Define the new issue types in the JSON format section
new_issue_types = "\"issue_type\": \"Meaningless Comment|Missing Comments|Code Snippet in Comment|Comment-Code Inconsistency\""
old_issue_types = "\"issue_type\": \"Meaningless Comment|Missing Comments\""

# Replace the issue types
content = content.replace(old_issue_types, new_issue_types)

# Define the old focus sections pattern to replace
old_focus_pattern = r"Focus on Meaningless Comments.*?(?=\\n\\n[A-Z]|\\n\\nIgnore|$)"

# Define the new focus sections
new_focus_sections = """Focus on Meaningless Comments (single-line issues):
- Comments that simply restate what the code does (e.g., \"increment i\" for i++)
- Outdated comments that no longer match the code
- Commented-out code that should be removed
- Comments that add no value or context
- Generic comments like \"TODO: fix this\" without specifics

Focus on Missing Comments (multi-line issues):
- Complex algorithms without explanation
- Mathematical calculations or formulas without context
- Business logic or rules without documentation
- Complex conditional logic without explanation
- Data transformations or processing without description
- Non-obvious code patterns or optimizations

Focus on Code Snippets in Comments (single-line issues):
- Comments containing executable code that should be actual code
- Pseudo-code in comments that duplicates nearby actual code
- Code examples in comments that are outdated or incorrect
- Function calls or variable assignments written in comments instead of code
- Comments showing \"how to use\" that contain actual runnable code

Focus on Comment-Code Consistency (multi-line issues):
- Comments describing behavior that doesn\'t match the actual code implementation
- Function/method comments that contradict the actual parameters or return values
- Comments describing algorithms that differ from the implemented logic
- Variable or constant descriptions that don\'t match their actual usage
- Comments about error handling that don\'t match the actual exception handling
- Docstrings that describe incorrect function signatures or return types

Single-line issues (provide line_number, column_start, column_end):
- Meaningless Comment: Specific comment line that is useless or misleading
- Code Snippet in Comment: Comment containing code that should be implemented

Multi-line issues (provide line_number as start, line_end as end):
- Missing Comments: Complex code block that lacks necessary explanatory comments
- Comment-Code Inconsistency: Comment description that contradicts the actual code behavior"""

# Replace the focus sections
content = re.sub(old_focus_pattern, new_focus_sections, content, flags=re.DOTALL)

# Write the updated content back to the file
with open("vibot/commands/comment.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Comment analysis updated with new features:")
print("1. Code Snippet in Comment detection")
print("2. Comment-Code Consistency verification")
print("File updated successfully!")
