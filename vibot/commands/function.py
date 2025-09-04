#!/usr/bin/env python3
"""vibot function command implementation - AI-powered function quality analysis"""

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

# Token usage tracking for function analysis
class FunctionTokenTracker:
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

# Global token tracker for function analysis
function_token_tracker = FunctionTokenTracker()


def analyze_code_functions_with_ai(file_content, file_path, api_key, api_proxy, model, max_lines=50, max_params=5):
    """Analyze code functions using AI"""
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
As a code quality expert, analyze the following code file for function quality issues.

File path: {file_path}

Code content:
```
{file_content}
```

Please analyze all functions/methods in this code and return results strictly in the following JSON format:

{{
  "has_issues": true/false,
  "functions_analyzed": number_of_functions_found,
  "issues": [
    {{
      "function_name": "function_name",
      "line_number": line_number,
      "issue_type": "Long Function|Too Many Parameters|Missing Type Annotations",
      "severity": "high|medium|low",
      "description": "detailed description of the issue",
      "suggestion": "specific suggestion to fix the issue",
      "metrics": {{
        "estimated_lines": number,
        "estimated_parameters": number,
        "missing_return_type": true/false,
        "missing_param_types": number
      }}
    }}
  ]
}}

Analysis criteria:
1. Function Length: Functions should be ≤{max_lines} lines of code
2. Parameter Count: Functions should have ≤{max_params} parameters
3. Type Annotations: Functions should have proper type annotations for parameters and return values

Focus on:
- Functions that are too long (many lines of code)
- Functions with too many parameters
- Functions missing type annotations (for Python, TypeScript, Java, C#, etc.)

Type annotation rules:
- Python: Check for parameter type hints and return type annotations (def func(param: int) -> str:)
- TypeScript: Check for parameter types and return types (function func(param: number): string)
- Java: Check for parameter types and return types (public String func(int param))
- C#: Check for parameter types and return types (public string Func(int param))
- Other languages: Apply similar type annotation standards

Ignore:
- Simple getter/setter methods
- Constructor methods with many parameters (if justified for initialization)
- Test methods (unless extremely long)
- Empty functions or functions with only comments/docstrings
- __init__, __str__, __repr__ methods in Python (for type annotations)
- Main functions or entry points

Severity guidelines:
- High: Functions >100 lines or >10 parameters
- Medium: Functions >{max_lines*2} lines or >{max_params*2} parameters, or missing multiple type annotations
- Low: Functions slightly over thresholds, or missing few type annotations

Return valid JSON only, no additional text.
"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional code quality analysis expert. Analyze functions for quality issues and return results in the specified JSON format only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.1
        )
        
        # Track token usage
        if hasattr(response, 'usage'):
            function_token_tracker.add_usage(response.usage)
        
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
            return {"has_issues": False, "functions_analyzed": 0, "issues": []}
        
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


def analyze_functions_in_directory(path, max_lines=50, max_params=5):
    """Analyze function quality in directory using AI"""
    try:
        # Check if openai package is available
        if not OPENAI_AVAILABLE:
            print(f"{Colors.BRIGHT_ORANGE_RED}❌ Error: openai package not found{Colors.RESET}")
            print("The openai package is required for AI-powered function analysis.")
            print("\nTrying to install openai package...")
            
            try:
                # Try to auto-install openai package
                subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
                print(f"{Colors.YELLOW}✅ Successfully installed openai package{Colors.RESET}")
                print("Please run the command again to use AI function analysis.")
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
        function_token_tracker.start_tracking(model)
        
        print(f"🤖 AI-powered function quality analysis in: {os.path.abspath(path)}")
        print(f"Using model: {model}")
        print(f"Thresholds: Lines≤{max_lines}, Params≤{max_params}")
        print("=" * 70)
        
        all_issues = []
        total_files_scanned = 0
        total_functions_analyzed = 0
        files_with_issues = 0
        
        # Supported file extensions for function analysis
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
                    analysis_result = analyze_code_functions_with_ai(
                        file_content, relative_path, api_key, api_proxy, model, 
                        max_lines, max_params
                    )
                    
                    if analysis_result is None:
                        print(f"{Colors.BRIGHT_ORANGE_RED}Failed{Colors.RESET}")
                        continue
                    
                    # Update function count
                    total_functions_analyzed += analysis_result.get('functions_analyzed', 0)
                    
                    if analysis_result.get('has_issues', False) and analysis_result.get('issues'):
                        files_with_issues += 1
                        print(f"{Colors.BRIGHT_ORANGE_RED}Issues found{Colors.RESET}")
                        
                        # Display found issues
                        for issue in analysis_result['issues']:
                            print(f"\n{Colors.YELLOW}Function: {issue.get('function_name', 'Unknown')}(){Colors.RESET}")
                            print(f"   File: {relative_path}")
                            print(f"   Line: {issue.get('line_number', '?')}")
                            
                            # Display metrics if available
                            metrics = issue.get('metrics', {})
                            if metrics:
                                if 'estimated_lines' in metrics:
                                    print(f"   Estimated Lines: {metrics.get('estimated_lines', '?')}")
                                if 'estimated_parameters' in metrics:
                                    print(f"   Estimated Parameters: {metrics.get('estimated_parameters', '?')}")
                                if 'missing_return_type' in metrics and metrics.get('missing_return_type'):
                                    print(f"   Missing Return Type: Yes")
                                if 'missing_param_types' in metrics and metrics.get('missing_param_types', 0) > 0:
                                    print(f"   Missing Parameter Types: {metrics.get('missing_param_types', 0)}")
                            
                            severity_color = Colors.BRIGHT_ORANGE_RED if issue.get('severity') == 'high' else Colors.YELLOW
                            print(f"   {severity_color}⚠️  {issue.get('issue_type', 'Quality Issue')}: {issue.get('description', '')}{Colors.RESET}")
                            if issue.get('suggestion'):
                                print(f"   💡 {issue.get('suggestion', '')}")
                            
                            # Add to total results
                            all_issues.append({
                                'file': relative_path,
                                'function': issue.get('function_name'),
                                'line': issue.get('line_number'),
                                'type': issue.get('issue_type'),
                                'severity': issue.get('severity'),
                                'description': issue.get('description'),
                                'suggestion': issue.get('suggestion')
                            })
                    else:
                        print(f"{Colors.YELLOW}Clean{Colors.RESET}")
                
                except (UnicodeDecodeError, PermissionError, IsADirectoryError):
                    continue
                except Exception as e:
                    print(f"Error analyzing file {file_path}: {e}")
        
        print("\n" + "=" * 70)
        print(f"🔍 AI Function Quality Analysis Results:")
        print(f"  Files scanned: {total_files_scanned}")
        print(f"  Functions analyzed: {total_functions_analyzed}")
        print(f"  Files with issues: {files_with_issues}")
        print(f"  Total function issues: {len(all_issues)}")
        
        if all_issues:
            print(f"\n{Colors.BRIGHT_ORANGE_RED}🚨 Function Quality Issues Detected by AI!{Colors.RESET}")
            
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
            
            print(f"\n{Colors.YELLOW}💡 AI Recommendations:{Colors.RESET}")
            print("1. Break long functions into smaller, focused functions")
            print("2. Reduce parameter count using parameter objects or configuration classes")
            print("3. Extract helper methods to reduce function length")
            print("4. Group related parameters into data structures")
            print("5. Consider using builder pattern for functions with many parameters")
            print("6. Add type annotations to improve code clarity and catch type errors")
            print("7. Use proper return type annotations for better IDE support")
            print("8. Consider using typing module for complex types (Union, Optional, etc.)")
            
        else:
            print(f"\n{Colors.YELLOW}✅ AI function analysis complete - No quality issues detected!{Colors.RESET}")
            print("Your functions follow good coding practices.")
        
        # Print token usage summary
        function_token_tracker.print_summary()
        
    except Exception as e:
        print(f"Error: {e}")