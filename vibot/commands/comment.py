#!/usr/bin/env python3
"""vibot comment command implementation - AI-powered code comments analysis"""

import os
import json
import sys
import subprocess
import time
from ..utils import should_skip_file, Colors

# Try to import openai, provide installation hint if failed
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Token usage tracking for comment analysis
class CommentTokenTracker:
    def __init__(self):
        self.total_api_calls = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_tokens = 0
        self.model_name = ""
        self.start_time = None
        
    def start_tracking(self, model):
        self.model_name = model
        self.start_time = time.time()
        
    def add_usage(self, usage):
        self.total_api_calls += 1
        if hasattr(usage, 'prompt_tokens'):
            self.total_prompt_tokens += usage.prompt_tokens
        if hasattr(usage, 'completion_tokens'):
            self.total_completion_tokens += usage.completion_tokens
        if hasattr(usage, 'total_tokens'):
            self.total_tokens += usage.total_tokens
            
    def print_summary(self):
        if self.total_api_calls > 0:
            # Estimate cost based on common pricing
            estimated_cost = (self.total_prompt_tokens * 0.0000015) + (self.total_completion_tokens * 0.000002)
            duration = time.time() - self.start_time if self.start_time else 0
            
            print(f"\n{Colors.YELLOW}🤖 AI Token Usage Summary:{Colors.RESET}")
            print(f"  Model: {self.model_name}")
            print(f"  API Calls: {self.total_api_calls}")
            print(f"  Prompt Tokens: {self.total_prompt_tokens:,}")
            print(f"  Completion Tokens: {self.total_completion_tokens:,}")
            print(f"  Total Tokens: {self.total_tokens:,}")
            print(f"  Estimated Cost: ${estimated_cost:.5f}")
            print(f"  Duration: {duration:.2f}s")

# Global token tracker for comment analysis
comment_token_tracker = CommentTokenTracker()


def analyze_code_comments_with_ai(file_content, file_path, api_key, api_proxy, model):
    """Analyze code comments using AI"""
    if not OPENAI_AVAILABLE:
        return None
        
    try:
        # Configure OpenAI client
        client = openai.OpenAI(
            api_key=api_key,
            base_url=api_proxy
        )
        
        # Build analysis prompt
        prompt = f"""
As a code documentation expert, analyze the following code file for comment-related issues.

File path: {file_path}

Code content:
```
{file_content}
```

Please analyze the code and return results strictly in the following JSON format:

{{
  "has_issues": true/false,
  "lines_analyzed": number_of_lines_analyzed,
  "issues": [
    {{
      "line_number": line_number,
      "line_end": line_end_number_for_multiline_issues,
      "column_start": column_start_position_for_single_line,
      "column_end": column_end_position_for_single_line,
      "line_content": "actual code line content",
      "issue_type": "Useless Comments|Missing Comments",
      "severity": "high|medium|low",
      "description": "detailed description of the comment issue",
      "suggestion": "specific suggestion to improve comments"
    }}
  ]
}}

Analysis criteria:
1. Useless Comments: Comments that don't add value, are outdated, state the obvious, inconsistent with code behavior, or contain code snippets
2. Missing Comments: Complex logic blocks (algorithms, calculations, business logic) without explanatory comments

Focus on Useless Comments (single-line issues):
- Comments that simply restate what the code does (e.g., "increment i" for i++)
- Outdated comments that no longer match the code
- Commented-out code that should be removed
- Comments that add no value or context
- Generic comments like "TODO: fix this" without specifics
- Comments that contradict the code behavior
- Comments that are incorrect or misleading
- Overly obvious comments for simple operations
- Comments that include actual code snippets instead of explanations
- Comments that duplicate code logic without adding context

Focus on Missing Comments (multi-line issues):
- Complex algorithms without explanation
- Mathematical calculations or formulas without context
- Business logic or rules without documentation
- Complex conditional logic without explanation
- Data transformations or processing without description
- Non-obvious code patterns or optimizations

Single-line issues (provide line_number, column_start, column_end):
- Useless Comments: Specific comment line that is useless, misleading, contradicts code, or contains code snippets

Multi-line issues (provide line_number as start, line_end as end):
- Missing Comments: Complex code block that lacks necessary explanatory comments

Missing Comments detection guidelines:
- Look for complex algorithms, mathematical calculations, or business logic without comments
- Identify loops with complex conditions or nested logic without explanation
- Find conditional blocks with complex business rules without comments
- Detect data transformations or processing without explanatory comments
- Flag functions with complex logic but no internal comments (beyond docstrings)

Ignore:
- Function/method docstrings (these are good documentation)
- Class-level documentation
- Module-level documentation
- Debug or TODO comments (these are acceptable if specific)
- Simple getter/setter methods (don't need internal comments)
- Self-explanatory code with clear variable names
- Standard code patterns that are widely understood

Severity guidelines:
- High: Completely misleading comments, complex algorithms without any explanation
- Medium: Outdated comments, moderately complex logic without comments
- Low: Minor comment improvements, slightly unclear code sections

Return valid JSON only, no additional text.
"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional code documentation analysis expert. Analyze code for comment-related issues and return results in the specified JSON format only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.1
        )
        
        # Track token usage
        if hasattr(response, 'usage'):
            comment_token_tracker.add_usage(response.usage)
        
        # Parse AI response JSON result
        ai_response = response.choices[0].message.content.strip()
        
        # Try to extract JSON part (if AI returned extra text)
        if "```json" in ai_response:
            json_start = ai_response.find("```json") + 7
            json_end = ai_response.find("```", json_start)
            ai_response = ai_response[json_start:json_end].strip()
        elif ai_response.startswith("```") and ai_response.endswith("```"):
            ai_response = ai_response[3:-3].strip()
        
        try:
            result = json.loads(ai_response)
            return result
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse AI response as JSON: {e}")
            print(f"AI Response: {ai_response}")
            return {"has_issues": False, "lines_analyzed": 0, "issues": []}
        
    except Exception as e:
        error_msg = str(e)
        if "socksio" in error_msg:
            print(f"Error: SOCKS proxy support missing. Installing required package...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "httpx[socks]"])
                print("Please run the command again.")
            except subprocess.CalledProcessError:
                print("Failed to install httpx[socks]. Please install manually: pip install httpx[socks]")
        else:
            print(f"Error analyzing with AI: {e}")
        return None


def analyze_comments_in_directory(path):
    """Analyze code comments in directory using AI"""
    try:
        # Check if openai package is available
        if not OPENAI_AVAILABLE:
            print(f"{Colors.BRIGHT_ORANGE_RED}❌ Error: openai package not found{Colors.RESET}")
            print("The openai package is required for AI-powered comment analysis.")
            print("\nTrying to install openai package...")
            
            try:
                # Try to auto-install openai package
                subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
                print(f"{Colors.YELLOW}✅ Successfully installed openai package{Colors.RESET}")
                print("Please run the command again to use AI comment analysis.")
                return
            except subprocess.CalledProcessError:
                print(f"{Colors.BRIGHT_ORANGE_RED}❌ Failed to install openai package{Colors.RESET}")
                print("Please install it manually with: pip install openai")
                return
        
        # Check required environment variables
        api_key = os.getenv('VIBOT_API_KEY')
        api_proxy = os.getenv('VIBOT_API_PROXY')
        model = os.getenv('VIBOT_API_MODEL', 'deepseek-v3')
        
        if not api_key or not api_proxy:
            print(f"{Colors.BRIGHT_ORANGE_RED}❌ Error: AI API configuration missing{Colors.RESET}")
            print("Please set the following environment variables:")
            print("  VIBOT_API_KEY - Your API key")
            print("  VIBOT_API_PROXY - API proxy URL")
            print("  VIBOT_API_MODEL - Model name (optional, default: deepseek-v3)")
            print("\nExample:")
            print("  export VIBOT_API_KEY='your-api-key'")
            print("  export VIBOT_API_PROXY='https://api.deepseek.com'")
            return
        
        if not os.path.exists(path):
            print(f"Error: Path '{path}' does not exist")
            return
        
        if not os.path.isdir(path):
            print(f"Error: '{path}' is not a directory")
            return
        
        # Initialize token tracking
        comment_token_tracker.start_tracking(model)
        
        print(f"🤖 AI-powered code comments analysis in: {os.path.abspath(path)}")
        print(f"Using model: {model}")
        print("=" * 70)
        
        all_issues = []
        total_files_scanned = 0
        total_lines_analyzed = 0
        files_with_issues = 0
        
        # Supported file extensions for comment analysis
        supported_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.kt', '.swift', '.rs'}
        
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip non-code files
                if should_skip_file(file):
                    continue
                    
                # Only analyze supported file types
                _, ext = os.path.splitext(file)
                if ext.lower() not in supported_extensions:
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read()
                    
                    # Skip empty files or too small files
                    if len(file_content.strip()) < 20:
                        continue
                    
                    total_files_scanned += 1
                    relative_path = os.path.relpath(file_path, path)
                    
                    print(f"Analyzing: {relative_path}...", end=" ")
                    
                    # Analyze file with AI
                    analysis_result = analyze_code_comments_with_ai(
                        file_content, relative_path, api_key, api_proxy, model
                    )
                    
                    if analysis_result is None:
                        print(f"{Colors.BRIGHT_ORANGE_RED}Failed{Colors.RESET}")
                        continue
                    
                    # Update lines count
                    total_lines_analyzed += analysis_result.get('lines_analyzed', 0)
                    
                    if analysis_result.get('has_issues', False) and analysis_result.get('issues'):
                        files_with_issues += 1
                        print(f"{Colors.BRIGHT_ORANGE_RED}Issues found{Colors.RESET}")
                        
                        # Display found issues
                        for issue in analysis_result['issues']:
                            issue_type = issue.get('issue_type', 'Comment Issue')
                            
                            # Handle single-line vs multi-line issues
                            if issue_type == 'Useless Comments':
                                # Single-line issues with column positions
                                col_start = issue.get('column_start', '?')
                                col_end = issue.get('column_end', '?')
                                print(f"\n{Colors.YELLOW}Line {issue.get('line_number', '?')}:{col_start}-{col_end}:{Colors.RESET}")
                                print(f"   File: {relative_path}")
                                print(f"   Code: {issue.get('line_content', '').strip()}")
                            else:
                                # Multi-line issues with start and end lines
                                line_start = issue.get('line_number', '?')
                                line_end = issue.get('line_end', line_start)
                                if line_end and line_end != line_start:
                                    print(f"\n{Colors.YELLOW}Lines {line_start}-{line_end}:{Colors.RESET}")
                                else:
                                    print(f"\n{Colors.YELLOW}Line {line_start}:{Colors.RESET}")
                                print(f"   File: {relative_path}")
                                if issue.get('line_content'):
                                    print(f"   Code: {issue.get('line_content', '').strip()}")
                            
                            severity_color = Colors.BRIGHT_ORANGE_RED if issue.get('severity') == 'high' else Colors.YELLOW
                            print(f"   {severity_color}⚠️  {issue_type}: {issue.get('description', '')}{Colors.RESET}")
                            if issue.get('suggestion'):
                                print(f"   💡 {issue.get('suggestion', '')}")
                            
                            # Add to total results
                            all_issues.append({
                                'file': relative_path,
                                'line': issue.get('line_number'),
                                'line_end': issue.get('line_end'),
                                'column_start': issue.get('column_start'),
                                'column_end': issue.get('column_end'),
                                'type': issue_type,
                                'severity': issue.get('severity'),
                                'description': issue.get('description'),
                                'suggestion': issue.get('suggestion'),
                                'line_content': issue.get('line_content', '')
                            })
                    else:
                        print(f"{Colors.YELLOW}Clean{Colors.RESET}")
                
                except (UnicodeDecodeError, PermissionError, IsADirectoryError):
                    continue
                except Exception as e:
                    print(f"Error analyzing file {file_path}: {e}")
        
        print("\n" + "=" * 70)
        print(f"🔍 AI Code Comments Analysis Results:")
        print(f"  Files scanned: {total_files_scanned}")
        print(f"  Lines analyzed: {total_lines_analyzed}")
        print(f"  Files with issues: {files_with_issues}")
        print(f"  Total comment issues: {len(all_issues)}")
        
        if all_issues:
            print(f"\n{Colors.BRIGHT_ORANGE_RED}🚨 Code Comment Issues Detected by AI!{Colors.RESET}")
            
            # Classify issues by type and severity
            issue_types = {}
            severity_counts = {'high': 0, 'medium': 0, 'low': 0}
            
            for issue in all_issues:
                issue_type = issue.get('type', 'Unknown')
                issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
                severity = issue.get('severity', 'unknown')
                if severity in severity_counts:
                    severity_counts[severity] += 1
            
            print(f"\n📊 Issues by type:")
            for issue_type, count in sorted(issue_types.items()):
                print(f"  {issue_type}: {count}")
                
            print(f"\n📊 Issues by severity:")
            for severity, count in severity_counts.items():
                if count > 0:
                    color = Colors.BRIGHT_ORANGE_RED if severity == 'high' else Colors.YELLOW if severity == 'medium' else Colors.RESET
                    print(f"  {color}{severity.upper()}: {count}{Colors.RESET}")
            
            print(f"\n{Colors.YELLOW}💡 AI Comment Recommendations:{Colors.RESET}")
            print("1. Remove or update useless, outdated, and incorrect comments")
            print("2. Add explanatory comments for complex algorithms and business logic")
            print("3. Document the 'why' behind non-obvious code decisions")
            print("4. Use clear, concise language in comments")
            print("5. Keep comments up-to-date with code changes")
            print("6. Remove commented-out code that is no longer needed")
            print("7. Add context for complex mathematical formulas or calculations")
            print("8. Replace code snippets in comments with clear explanations")
            
        else:
            print(f"\n{Colors.YELLOW}✅ AI comment analysis complete - No comment issues detected!{Colors.RESET}")
            print("Your code has appropriate and meaningful comments.")
        
        # Print token usage summary
        comment_token_tracker.print_summary()
        
    except Exception as e:
        print(f"Error: {e}")