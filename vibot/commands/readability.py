#!/usr/bin/env python3
"""vibot readability command implementation - AI-powered code readability analysis"""

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

# Token usage tracking for readability analysis
class ReadabilityTokenTracker:
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

# Global token tracker for readability analysis
readability_token_tracker = ReadabilityTokenTracker()


def analyze_code_readability_with_ai(file_content, file_path, api_key, api_proxy, model, max_line_length=80):
    """Analyze code readability using AI"""
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
As a code readability expert, analyze the following code file for readability issues.

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
      "issue_type": "Long Line|Complex Ternary|Missing Line Separation",
      "severity": "high|medium|low",
      "description": "detailed description of the readability issue",
      "suggestion": "specific suggestion to improve readability"
    }}
  ]
}}

Analysis criteria:
1. Long Lines: Lines longer than {max_line_length} characters
2. Complex Ternary: Nested or overly complex ternary operators (? :)
3. Missing Line Separation: Dense code blocks without blank lines to separate logical sections

Focus on:
- Lines that are too long and hard to read
- Complex ternary operators that reduce readability
- Dense code blocks where functions, classes, or logical sections are not separated by blank lines

Single-line issues (provide line_number, column_start, column_end):
- Long Line: Specific line that exceeds length limit
- Complex Ternary: Specific ternary operator location

Multi-line issues (provide line_number as start, line_end as end):
- Missing Line Separation: Dense code section without proper spacing (provide start and end line of the dense section)

Missing Line Separation detection:
- Look for multiple functions defined consecutively without blank lines between them
- Identify logical code blocks (like variable declarations, processing, return) squeezed together
- Find class methods or properties without proper spacing
- Detect import statements mixed with code without separation

Ignore:
- Short lines even if they contain simple ternary operators
- Simple getter/setter methods
- Single blank lines (only flag when there are NO blank lines where needed)

Severity guidelines:
- High: Very long lines (>150 chars), deeply nested ternary, functions crammed together without any separation
- Medium: Moderately long lines, complex ternary, some missing line separations
- Low: Slightly long lines, simple readability improvements, minor spacing issues

Return valid JSON only, no additional text.
"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional code readability analysis expert. Analyze code for readability issues and return results in the specified JSON format only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.1
        )
        
        # Track token usage
        if hasattr(response, 'usage'):
            readability_token_tracker.add_usage(response.usage)
        
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


def analyze_readability_in_directory(path, max_line_length=80):
    """Analyze code readability in directory using AI"""
    try:
        # Check if openai package is available
        if not OPENAI_AVAILABLE:
            print(f"{Colors.BRIGHT_ORANGE_RED}❌ Error: openai package not found{Colors.RESET}")
            print("The openai package is required for AI-powered readability analysis.")
            print("\nTrying to install openai package...")
            
            try:
                # Try to auto-install openai package
                subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
                print(f"{Colors.YELLOW}✅ Successfully installed openai package{Colors.RESET}")
                print("Please run the command again to use AI readability analysis.")
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
        readability_token_tracker.start_tracking(model)
        
        print(f"🤖 AI-powered code readability analysis in: {os.path.abspath(path)}")
        print(f"Using model: {model}")
        print(f"Max line length: {max_line_length} characters")
        print("=" * 70)
        
        all_issues = []
        total_files_scanned = 0
        total_lines_analyzed = 0
        files_with_issues = 0
        
        # Supported file extensions for readability analysis
        supported_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go', '.kt', '.swift', '.rs', '.html', '.css', '.scss', '.less'}
        
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
                    analysis_result = analyze_code_readability_with_ai(
                        file_content, relative_path, api_key, api_proxy, model, max_line_length
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
                            issue_type = issue.get('issue_type', 'Readability Issue')
                            
                            # Handle single-line vs multi-line issues
                            if issue_type in ['Long Line', 'Complex Ternary']:
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
        print(f"🔍 AI Code Readability Analysis Results:")
        print(f"  Files scanned: {total_files_scanned}")
        print(f"  Lines analyzed: {total_lines_analyzed}")
        print(f"  Files with issues: {files_with_issues}")
        print(f"  Total readability issues: {len(all_issues)}")
        
        if all_issues:
            print(f"\n{Colors.BRIGHT_ORANGE_RED}🚨 Code Readability Issues Detected by AI!{Colors.RESET}")
            
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
            
            print(f"\n{Colors.YELLOW}💡 AI Readability Recommendations:{Colors.RESET}")
            print("1. Break long lines into multiple lines for better readability")
            print("2. Replace complex ternary operators with if-else statements")
            print("3. Use blank lines to separate logical code blocks and functions")
            print("4. Group related code together and separate different concerns with blank lines")
            print("5. Use descriptive variable names instead of cryptic abbreviations")
            
        else:
            print(f"\n{Colors.YELLOW}✅ AI readability analysis complete - No readability issues detected!{Colors.RESET}")
            print("Your code follows good readability practices.")
        
        # Print token usage summary
        readability_token_tracker.print_summary()
        
    except Exception as e:
        print(f"Error: {e}")