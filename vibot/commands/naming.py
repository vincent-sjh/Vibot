#!/usr/bin/env python3
"""vibot naming command implementation - AI-powered naming convention analysis"""

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

# Token usage tracking for naming analysis
class NamingTokenTracker:
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

# Global token tracker for naming analysis
naming_token_tracker = NamingTokenTracker()


def analyze_naming_with_ai(file_content, file_path, api_key, api_proxy, model):
    """Analyze naming conventions and issues using AI"""
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
As a code quality expert specializing in naming conventions and best practices, analyze the following code file for naming-related issues.

File path: {file_path}

Code content:
```
{file_content}
```

Please analyze the code and return results strictly in the following JSON format:

{{
  "has_naming_issues": true/false,
  "total_issues_found": number_of_naming_issues,
  "naming_issues": [
    {{
      "issue_id": "unique_id_for_this_issue",
      "issue_type": "Oversimplified Names|Obscure Abbreviations|Inconsistent Style|Meaningless Names|Constant Naming|Poor Class Names|Function Naming|Variable Scope",
      "severity": "high|medium|low",
      "description": "detailed description of the naming issue",
      "suggestion": "specific naming improvement suggestion",
      "examples": [
        {{
          "line_number": line_number,
          "current_name": "current problematic name",
          "suggested_name": "suggested better name",
          "context": "code context where the issue occurs"
        }}
      ]
    }}
  ]
}}

Analysis criteria for naming issues:

1. **Oversimplified Names**: 
   - Single letter variables (except for short loops): a, b, c, x, y, z
   - Generic names in non-trivial contexts: i, j, k outside simple loops
   - Overly short names that don't convey meaning

2. **Obscure Abbreviations**:
   - Unclear abbreviations: calcTotPrc instead of calculateTotalPrice
   - Domain-specific abbreviations without context
   - Inconsistent abbreviation patterns

3. **Inconsistent Style**:
   - Mixed snake_case and camelCase in same file/project
   - Inconsistent capitalization patterns
   - Mixed naming conventions for similar entities

4. **Meaningless Names**:
   - Generic names: data, temp, foo, bar, stuff, thing
   - Non-descriptive class names: myclass, handler, manager (without context)
   - Placeholder names left in production code

5. **Constant Naming**:
   - Constants not in UPPER_CASE: max_retries instead of MAX_RETRIES
   - Magic numbers without named constants
   - Configuration values not properly named

6. **Poor Class Names**:
   - Non-noun class names
   - Overly generic class names
   - Class names that don't represent entities

7. **Function Naming**:
   - Non-verb function names for actions
   - Unclear function purposes
   - Inconsistent function naming patterns

8. **Variable Scope Issues**:
   - Short names for long-lived variables
   - Long names for short-lived variables
   - Inappropriate naming for variable scope

Severity guidelines:
- High: Critical naming issues that significantly impact code readability and maintainability
- Medium: Moderate naming issues that could cause confusion
- Low: Minor naming inconsistencies or style issues

Focus on:
- Variables, functions, classes, constants, and method names
- Naming consistency within the file
- Clarity and descriptiveness of names
- Following language-specific naming conventions
- Avoiding misleading or confusing names

Ignore:
- Standard library names and built-in functions
- Third-party library conventions
- Domain-specific terminology that is well-established
- Single-letter variables in very short, obvious contexts (like simple math operations)

Return valid JSON only, no additional text.
"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional code naming convention expert. Analyze code for naming issues and return results in the specified JSON format only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.1
        )
        
        # Track token usage
        if hasattr(response, 'usage'):
            naming_token_tracker.add_usage(response.usage)
        
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
            return {"has_naming_issues": False, "total_issues_found": 0, "naming_issues": []}
        
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


def analyze_naming_in_directory(path):
    """Analyze naming conventions in directory using AI"""
    try:
        # Check if openai package is available
        if not OPENAI_AVAILABLE:
            print(f"{Colors.BRIGHT_ORANGE_RED}❌ Error: openai package not found{Colors.RESET}")
            print("The openai package is required for AI-powered naming analysis.")
            print("\nTrying to install openai package...")
            
            try:
                # Try to auto-install openai package
                subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
                print(f"{Colors.YELLOW}✅ Successfully installed openai package{Colors.RESET}")
                print("Please run the command again to use AI naming analysis.")
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
        naming_token_tracker.start_tracking(model)
        
        print(f"🤖 AI-powered naming convention analysis in: {os.path.abspath(path)}")
        print(f"Using model: {model}")
        print("Checking for naming issues and conventions...")
        print("=" * 70)
        
        all_naming_issues = []
        total_files_scanned = 0
        total_issues_found = 0
        files_with_issues = 0
        
        # Supported file extensions for naming analysis
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
                    if len(file_content.strip()) < 50:
                        continue
                    
                    total_files_scanned += 1
                    relative_path = os.path.relpath(file_path, path)
                    
                    print(f"Analyzing: {relative_path}...", end=" ")
                    
                    # Analyze file with AI
                    analysis_result = analyze_naming_with_ai(
                        file_content, relative_path, api_key, api_proxy, model
                    )
                    
                    if analysis_result is None:
                        print(f"{Colors.BRIGHT_ORANGE_RED}Failed{Colors.RESET}")
                        continue
                    
                    # Update issues count
                    file_issues = analysis_result.get('total_issues_found', 0)
                    total_issues_found += file_issues
                    
                    if analysis_result.get('has_naming_issues', False) and analysis_result.get('naming_issues'):
                        files_with_issues += 1
                        print(f"{Colors.BRIGHT_ORANGE_RED}Issues found{Colors.RESET}")
                        
                        # Display found naming issues
                        for issue in analysis_result['naming_issues']:
                            print(f"\n{Colors.YELLOW}Naming Issue: {issue.get('issue_id', 'Unknown')}{Colors.RESET}")
                            print(f"   File: {relative_path}")
                            print(f"   Type: {issue.get('issue_type', 'Unknown')}")
                            
                            severity_color = Colors.BRIGHT_ORANGE_RED if issue.get('severity') == 'high' else Colors.YELLOW
                            print(f"   {severity_color}⚠️  {issue.get('description', '')}{Colors.RESET}")
                            
                            # Show all examples of this naming issue
                            examples = issue.get('examples', [])
                            print(f"   Found {len(examples)} examples:")
                            
                            for i, example in enumerate(examples, 1):
                                line_number = example.get('line_number', '?')
                                current_name = example.get('current_name', '')
                                suggested_name = example.get('suggested_name', '')
                                context = example.get('context', '').strip()
                                
                                print(f"   Example {i}: Line {line_number}")
                                print(f"     Current: {current_name}")
                                print(f"     Suggested: {suggested_name}")
                                if context:
                                    # Show context (first line only to keep output clean)
                                    context_line = context.split('\n')[0][:80]
                                    print(f"     Context: {context_line}")
                            
                            if issue.get('suggestion'):
                                print(f"   💡 {issue.get('suggestion', '')}")
                            
                            # Add to total results
                            all_naming_issues.append({
                                'file': relative_path,
                                'issue_id': issue.get('issue_id'),
                                'type': issue.get('issue_type'),
                                'severity': issue.get('severity'),
                                'description': issue.get('description'),
                                'suggestion': issue.get('suggestion'),
                                'examples': examples
                            })
                    else:
                        print(f"{Colors.YELLOW}Clean{Colors.RESET}")
                
                except (UnicodeDecodeError, PermissionError, IsADirectoryError):
                    continue
                except Exception as e:
                    print(f"Error analyzing file {file_path}: {e}")
        
        print("\n" + "=" * 70)
        print(f"🔍 AI Naming Convention Analysis Results:")
        print(f"  Files scanned: {total_files_scanned}")
        print(f"  Files with issues: {files_with_issues}")
        print(f"  Total naming issues: {len(all_naming_issues)}")
        
        if all_naming_issues:
            print(f"\n{Colors.BRIGHT_ORANGE_RED}🚨 Naming Issues Detected by AI!{Colors.RESET}")
            
            # Classify issues by type and severity
            issue_types = {}
            severity_counts = {'high': 0, 'medium': 0, 'low': 0}
            
            for issue in all_naming_issues:
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
            
            print(f"\n{Colors.YELLOW}💡 AI Naming Best Practices:{Colors.RESET}")
            print("1. Use descriptive and meaningful names")
            print("2. Follow consistent naming conventions (snake_case or camelCase)")
            print("3. Use UPPER_CASE for constants")
            print("4. Avoid abbreviations unless they are well-known")
            print("5. Use verbs for functions and nouns for variables/classes")
            print("6. Make names searchable and pronounceable")
            print("7. Use intention-revealing names")
            print("8. Avoid mental mapping and misleading names")
            
        else:
            print(f"\n{Colors.YELLOW}✅ AI naming analysis complete - No naming issues detected!{Colors.RESET}")
            print("Your code follows good naming conventions.")
        
        # Print token usage summary
        naming_token_tracker.print_summary()
        
    except Exception as e:
        print(f"Error: {e}")