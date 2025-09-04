#!/usr/bin/env python3
"""vibot magic command implementation - AI-powered magic numbers/strings detection"""

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

# Token usage tracking for magic detection analysis
class MagicTokenTracker:
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

# Global token tracker for magic detection analysis
magic_token_tracker = MagicTokenTracker()


def analyze_magic_values_with_ai(file_content, file_path, api_key, api_proxy, model):
    """Analyze magic numbers and strings using AI"""
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
As a code quality expert, analyze the following code file for magic numbers and magic strings.

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
      "column_start": column_start_position,
      "column_end": column_end_position,
      "line_content": "actual code line content",
      "issue_type": "Magic Number|Magic String",
      "severity": "high|medium|low",
      "magic_value": "the actual magic value found",
      "description": "detailed description of why this is a magic value",
      "suggestion": "specific suggestion with proposed constant name and value"
    }}
  ]
}}

Analysis criteria:
1. Magic Numbers: Hardcoded numbers without clear meaning (except standard values like 0, 1, -1, 2, 10, 100)
2. Magic Strings: Hardcoded strings that should be named constants (except simple display strings)

Focus on Magic Numbers:
- Mathematical constants that should be named (like 3.14159, 2.71828)
- Configuration values (timeouts, limits, thresholds)
- Array indices or sizes that aren't obvious
- Business logic numbers (tax rates, conversion factors)
- Error codes or status codes
- Port numbers, buffer sizes, retry counts

Focus on Magic Strings:
- API endpoints, URLs, file paths
- Database table/column names
- Configuration keys
- Error messages that are repeated
- File extensions or MIME types
- Regular expression patterns
- CSS selectors or HTML tags

Ignore:
- Standard constants: 0, 1, -1, 2, 10, 100, 1000
- Boolean values: true, false, null, undefined
- Simple array operations: arr[0], arr[1], arr.length
- Loop increments: i++, i += 1, i + 1
- Simple display strings in UI: "OK", "Cancel", "Yes", "No"
- Variable names or function names
- Comments and documentation strings
- Import statements and module paths
- Simple mathematical operations: x * 2, y / 2

Severity guidelines:
- High: Critical configuration values, complex mathematical constants, repeated business logic numbers
- Medium: Configuration strings, API endpoints, database identifiers
- Low: Simple constants that could benefit from naming

For each magic value found, provide:
- Exact line and column position
- The magic value itself
- Why it's considered magic
- Suggested constant name and usage

Return valid JSON only, no additional text.
"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional code quality analysis expert. Analyze code for magic numbers and strings, return results in the specified JSON format only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.1
        )
        
        # Track token usage
        if hasattr(response, 'usage'):
            magic_token_tracker.add_usage(response.usage)
        
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


def analyze_magic_in_directory(path):
    """Analyze magic numbers and strings in directory using AI"""
    try:
        # Check if openai package is available
        if not OPENAI_AVAILABLE:
            print(f"{Colors.BRIGHT_ORANGE_RED}❌ Error: openai package not found{Colors.RESET}")
            print("The openai package is required for AI-powered magic values analysis.")
            print("\nTrying to install openai package...")
            
            try:
                # Try to auto-install openai package
                subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
                print(f"{Colors.YELLOW}✅ Successfully installed openai package{Colors.RESET}")
                print("Please run the command again to use AI magic values analysis.")
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
        magic_token_tracker.start_tracking(model)
        
        print(f"🤖 AI-powered magic numbers/strings detection in: {os.path.abspath(path)}")
        print(f"Using model: {model}")
        print("=" * 70)
        
        all_issues = []
        total_files_scanned = 0
        total_lines_analyzed = 0
        files_with_issues = 0
        
        # Supported file extensions for magic values analysis
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
                    analysis_result = analyze_magic_values_with_ai(
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
                            print(f"\n{Colors.YELLOW}Line {issue.get('line_number', '?')}:{issue.get('column_start', '?')}-{issue.get('column_end', '?')}:{Colors.RESET}")
                            print(f"   File: {relative_path}")
                            print(f"   Code: {issue.get('line_content', '').strip()}")
                            print(f"   Magic Value: {Colors.BRIGHT_ORANGE_RED}{issue.get('magic_value', 'Unknown')}{Colors.RESET}")
                            
                            severity_color = Colors.BRIGHT_ORANGE_RED if issue.get('severity') == 'high' else Colors.YELLOW
                            print(f"   {severity_color}⚠️  {issue.get('issue_type', 'Magic Value')}: {issue.get('description', '')}{Colors.RESET}")
                            if issue.get('suggestion'):
                                print(f"   💡 {issue.get('suggestion', '')}")
                            
                            # Add to total results
                            all_issues.append({
                                'file': relative_path,
                                'line': issue.get('line_number'),
                                'column_start': issue.get('column_start'),
                                'column_end': issue.get('column_end'),
                                'type': issue.get('issue_type'),
                                'severity': issue.get('severity'),
                                'magic_value': issue.get('magic_value'),
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
        print(f"🔍 AI Magic Numbers/Strings Detection Results:")
        print(f"  Files scanned: {total_files_scanned}")
        print(f"  Lines analyzed: {total_lines_analyzed}")
        print(f"  Files with issues: {files_with_issues}")
        print(f"  Total magic values found: {len(all_issues)}")
        
        if all_issues:
            print(f"\n{Colors.BRIGHT_ORANGE_RED}🚨 Magic Numbers/Strings Detected by AI!{Colors.RESET}")
            
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
            
            print(f"\n{Colors.YELLOW}💡 AI Magic Values Recommendations:{Colors.RESET}")
            print("1. Replace magic numbers with named constants")
            print("2. Replace magic strings with configuration constants")
            print("3. Use enums or constant classes for related magic values")
            print("4. Document the meaning and purpose of constants")
            print("5. Group related constants together in a constants file")
            print("6. Use configuration files for environment-specific values")
            
        else:
            print(f"\n{Colors.YELLOW}✅ AI magic values analysis complete - No magic numbers/strings detected!{Colors.RESET}")
            print("Your code follows good practices for avoiding magic values.")
        
        # Print token usage summary
        magic_token_tracker.print_summary()
        
    except Exception as e:
        print(f"Error: {e}")