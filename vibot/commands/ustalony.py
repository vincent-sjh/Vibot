#!/usr/bin/env python3
"""vibot ustalony command implementation - AI-powered hardcoded secrets detection"""

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

# Token usage tracking
class TokenUsageTracker:
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
            # Estimate cost based on common pricing (rough estimate)
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

# Global token tracker
token_tracker = TokenUsageTracker()


def analyze_code_with_ai(file_content, file_path, api_key, api_proxy, model):
    """Analyze code for sensitive information using AI"""
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
As a code security expert, analyze the following code file for hardcoded sensitive information.

File path: {file_path}

Code content:
```
{file_content}
```

Please return analysis results strictly in the following JSON format, without any other text:

{{
  "has_issues": true/false,
  "issues": [
    {{
      "line_number": line_number,
      "line_content": "specific code line content",
      "issue_type": "sensitive information type",
      "description": "issue description",
      "severity": "high/medium/low",
      "suggestion": "fix suggestion"
    }}
  ]
}}

Types of sensitive information to detect:
- API keys and access tokens
- Database connection strings and passwords
- Private keys and certificates
- Hardcoded usernames and passwords
- Service endpoint URLs (containing sensitive information)
- Encryption keys and salt values
- Third-party service credentials

Notes:
1. Ignore example code in comments
2. Ignore obvious test/demo data
3. Only report real security risks
4. Must return valid JSON format
"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional code security analysis expert. Please strictly return analysis results in the required JSON format without any additional text or explanations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.1
        )
        
        # Track token usage
        if hasattr(response, 'usage'):
            token_tracker.add_usage(response.usage)
        
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
            return {"has_issues": False, "issues": []}
        
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


def detect_hardcoded_secrets(path):
    """Detect hardcoded sensitive information using AI"""
    try:
        # Check if openai package is available
        if not OPENAI_AVAILABLE:
            print(f"{Colors.BRIGHT_ORANGE_RED}❌ Error: openai package not found{Colors.RESET}")
            print("The openai package is required for AI-powered security scanning.")
            print("\nTrying to install openai package...")
            
            try:
                # Try to auto-install openai package
                subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
                print(f"{Colors.YELLOW}✅ Successfully installed openai package{Colors.RESET}")
                print("Please run the command again to use AI security scanning.")
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
        token_tracker.start_tracking(model)
        
        print(f"🤖 AI-powered security scan in: {os.path.abspath(path)}")
        print(f"Using model: {model}")
        print("=" * 60)
        
        all_issues = []
        total_files_scanned = 0
        files_with_issues = 0
        
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip binary files and special files
                if should_skip_file(file):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read()
                    
                    # Skip empty files or too small files
                    if len(file_content.strip()) < 10:
                        continue
                    
                    total_files_scanned += 1
                    relative_path = os.path.relpath(file_path, path)
                    
                    print(f"Analyzing: {relative_path}...", end=" ")
                    
                    # Analyze file with AI
                    analysis_result = analyze_code_with_ai(file_content, relative_path, api_key, api_proxy, model)
                    
                    if analysis_result is None:
                        print(f"{Colors.BRIGHT_ORANGE_RED}Failed{Colors.RESET}")
                        continue
                    
                    if analysis_result.get('has_issues', False) and analysis_result.get('issues'):
                        files_with_issues += 1
                        print(f"{Colors.BRIGHT_ORANGE_RED}Issues found{Colors.RESET}")
                        
                        # Display found issues
                        for issue in analysis_result['issues']:
                            print(f"\n{Colors.BRIGHT_ORANGE_RED}⚠️  {issue.get('issue_type', 'Security Issue')} detected:{Colors.RESET}")
                            print(f"   File: {Colors.YELLOW}{relative_path}{Colors.RESET}")
                            print(f"   Line {issue.get('line_number', '?')}: {issue.get('line_content', '').strip()}")
                            print(f"   Severity: {Colors.BRIGHT_ORANGE_RED}{issue.get('severity', 'unknown').upper()}{Colors.RESET}")
                            print(f"   Description: {issue.get('description', '')}")
                            if issue.get('suggestion'):
                                print(f"   Suggestion: {Colors.YELLOW}{issue.get('suggestion', '')}{Colors.RESET}")
                            
                            # Add to total results
                            all_issues.append({
                                'file': relative_path,
                                'line': issue.get('line_number'),
                                'type': issue.get('issue_type'),
                                'description': issue.get('description'),
                                'severity': issue.get('severity'),
                                'suggestion': issue.get('suggestion')
                            })
                    else:
                        print(f"{Colors.YELLOW}Clean{Colors.RESET}")
                
                except (UnicodeDecodeError, PermissionError, IsADirectoryError):
                    continue
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
        
        print("\n" + "=" * 60)
        print(f"🔍 AI Security Scan Results:")
        print(f"  Files scanned: {total_files_scanned}")
        print(f"  Files with issues: {files_with_issues}")
        print(f"  Total issues found: {len(all_issues)}")
        
        if all_issues:
            print(f"\n{Colors.BRIGHT_ORANGE_RED}🚨 Security Issues Detected by AI!{Colors.RESET}")
            
            # Classify by severity
            severity_counts = {}
            for issue in all_issues:
                severity = issue.get('severity', 'unknown')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            print(f"\n📊 Issues by severity:")
            for severity, count in severity_counts.items():
                color = Colors.BRIGHT_ORANGE_RED if severity == 'high' else Colors.YELLOW if severity == 'medium' else Colors.RESET
                print(f"  {color}{severity.upper()}: {count}{Colors.RESET}")
            
            print(f"\n{Colors.YELLOW}💡 AI Recommendations:{Colors.RESET}")
            print("1. Review all HIGH severity issues immediately")
            print("2. Use environment variables for sensitive configuration")
            print("3. Implement proper secret management practices")
            print("4. Consider using tools like HashiCorp Vault or cloud secret managers")
            print("5. Add sensitive files to .gitignore to prevent accidental commits")
            
        else:
            print(f"\n{Colors.YELLOW}✅ AI analysis complete - No security issues detected!{Colors.RESET}")
            print("Your code appears to follow good security practices.")
        
        # Print token usage summary
        token_tracker.print_summary()
        
    except Exception as e:
        print(f"Error: {e}")