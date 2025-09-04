#!/usr/bin/env python3
"""vibot overlap command implementation - AI-powered code duplication analysis"""

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

# Token usage tracking for overlap analysis
class OverlapTokenTracker:
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

# Global token tracker for overlap analysis
overlap_token_tracker = OverlapTokenTracker()


def analyze_code_overlap_with_ai(file_content, file_path, api_key, api_proxy, model, min_lines=3):
    """Analyze code overlap and duplication using AI"""
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
As a code quality expert specializing in DRY (Don't Repeat Yourself) principle, analyze the following code file for duplicate or overlapping logic.

File path: {file_path}

Code content:
```
{file_content}
```

Please analyze the code and return results strictly in the following JSON format:

{{
  "has_duplications": true/false,
  "total_duplications_found": number_of_duplication_groups,
  "duplications": [
    {{
      "duplication_id": "unique_id_for_this_duplication_group",
      "duplication_type": "Exact Duplicate|Similar Logic|Repeated Pattern",
      "severity": "high|medium|low",
      "description": "detailed description of the duplication",
      "suggestion": "specific refactoring suggestion",
      "instances": [
        {{
          "start_line": line_number,
          "end_line": line_number,
          "code_snippet": "actual duplicated code content"
        }},
        {{
          "start_line": line_number,
          "end_line": line_number,
          "code_snippet": "actual duplicated code content"
        }}
      ]
    }}
  ]
}}

Analysis criteria:
1. Exact Duplicates: Identical or nearly identical code blocks
2. Similar Logic: Different implementation but same logical purpose
3. Repeated Patterns: Similar code structures that could be abstracted

Focus on:
- Code blocks that are repeated with minor variations
- Similar logic implemented in different ways
- Repeated patterns that violate DRY principle
- Functions or methods that do very similar things
- Copy-paste code with small modifications

Ignore:
- Standard boilerplate code (imports, basic class structure)
- Simple getter/setter methods
- Standard error handling patterns
- Configuration or initialization code that naturally repeats
- Single-line duplications unless they form a pattern

Severity guidelines:
- High: Large blocks of identical or nearly identical code (>10 lines)
- Medium: Similar logic blocks or repeated patterns (5-10 lines)
- Low: Small repeated patterns or minor duplications (>={min_lines} lines)

Minimum duplication size: {min_lines} lines

For each duplication group, identify ALL instances where the duplication occurs.
Return valid JSON only, no additional text.
"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional code duplication analysis expert. Analyze code for violations of the DRY principle and return results in the specified JSON format only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000,
            temperature=0.1
        )
        
        # Track token usage
        if hasattr(response, 'usage'):
            overlap_token_tracker.add_usage(response.usage)
        
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
            return {"has_duplications": False, "total_duplications_found": 0, "duplications": []}
        
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



def analyze_overlap_in_directory(path, min_duplicate_lines=3):
    """Analyze code overlap and duplication in directory using AI"""
    try:
        # Check if openai package is available
        if not OPENAI_AVAILABLE:
            print(f"{Colors.BRIGHT_ORANGE_RED}❌ Error: openai package not found{Colors.RESET}")
            print("The openai package is required for AI-powered overlap analysis.")
            print("\nTrying to install openai package...")
            
            try:
                # Try to auto-install openai package
                subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
                print(f"{Colors.YELLOW}✅ Successfully installed openai package{Colors.RESET}")
                print("Please run the command again to use AI overlap analysis.")
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
        overlap_token_tracker.start_tracking(model)
        
        print(f"🤖 AI-powered code overlap analysis in: {os.path.abspath(path)}")
        print(f"Using model: {model}")
        print(f"Minimum duplicate lines: {min_duplicate_lines}")
        print("Checking for DRY principle violations...")
        print("=" * 70)
        
        all_duplications = []
        total_files_scanned = 0
        total_duplications_found = 0
        files_with_duplications = 0
        
        # Supported file extensions for overlap analysis
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
                    analysis_result = analyze_code_overlap_with_ai(
                        file_content, relative_path, api_key, api_proxy, model, min_duplicate_lines
                    )
                    
                    if analysis_result is None:
                        print(f"{Colors.BRIGHT_ORANGE_RED}Failed{Colors.RESET}")
                        continue
                    
                    # Update duplications count
                    file_duplications = analysis_result.get('total_duplications_found', 0)
                    total_duplications_found += file_duplications
                    
                    if analysis_result.get('has_duplications', False) and analysis_result.get('duplications'):
                        files_with_duplications += 1
                        print(f"{Colors.BRIGHT_ORANGE_RED}Duplications found{Colors.RESET}")
                        
                        # Display found duplications
                        for duplication in analysis_result['duplications']:
                                print(f"\n{Colors.YELLOW}Duplication Group: {duplication.get('duplication_id', 'Unknown')}{Colors.RESET}")
                                print(f"   File: {relative_path}")
                                print(f"   Type: {duplication.get('duplication_type', 'Unknown')}")
                                
                                severity_color = Colors.BRIGHT_ORANGE_RED if duplication.get('severity') == 'high' else Colors.YELLOW
                                print(f"   {severity_color}⚠️  {duplication.get('description', '')}{Colors.RESET}")
                                
                                # Show all instances of this duplication
                                instances = duplication.get('instances', [])
                                print(f"   Found {len(instances)} instances:")
                                
                                for i, instance in enumerate(instances, 1):
                                    start_line = instance.get('start_line', '?')
                                    end_line = instance.get('end_line', '?')
                                    code_snippet = instance.get('code_snippet', '').strip()
                                    
                                    print(f"   Instance {i}: Lines {start_line}-{end_line}")
                                    if code_snippet:
                                        # Show first few lines of the code snippet
                                        snippet_lines = code_snippet.split('\n')[:3]
                                        for line in snippet_lines:
                                            print(f"     {line}")
                                        if len(code_snippet.split('\n')) > 3:
                                            print(f"     ... ({len(code_snippet.split('\n')) - 3} more lines)")
                                
                                if duplication.get('suggestion'):
                                    print(f"   💡 {duplication.get('suggestion', '')}")
                                
                                # Add to total results
                                all_duplications.append({
                                    'file': relative_path,
                                    'duplication_id': duplication.get('duplication_id'),
                                    'type': duplication.get('duplication_type'),
                                    'severity': duplication.get('severity'),
                                    'description': duplication.get('description'),
                                    'suggestion': duplication.get('suggestion'),
                                    'instances': instances
                                })
                    else:
                        print(f"{Colors.YELLOW}Clean{Colors.RESET}")
                
                except (UnicodeDecodeError, PermissionError, IsADirectoryError):
                    continue
                except Exception as e:
                    print(f"Error analyzing file {file_path}: {e}")
        
        print("\n" + "=" * 70)
        print(f"🔍 AI Code Overlap Analysis Results:")
        print(f"  Files scanned: {total_files_scanned}")
        print(f"  Files with duplications: {files_with_duplications}")
        print(f"  Total duplication groups: {len(all_duplications)}")
        
        if all_duplications:
            print(f"\n{Colors.BRIGHT_ORANGE_RED}🚨 Code Duplications Detected by AI!{Colors.RESET}")
            
            # Classify duplications by type and severity
            duplication_types = {}
            severity_counts = {'high': 0, 'medium': 0, 'low': 0}
            
            for duplication in all_duplications:
                dup_type = duplication.get('type', 'Unknown')
                duplication_types[dup_type] = duplication_types.get(dup_type, 0) + 1
                severity = duplication.get('severity', 'unknown')
                if severity in severity_counts:
                    severity_counts[severity] += 1
            
            print(f"\n📊 Duplications by type:")
            for dup_type, count in sorted(duplication_types.items()):
                print(f"  {dup_type}: {count}")
                
            print(f"\n📊 Duplications by severity:")
            for severity, count in severity_counts.items():
                if count > 0:
                    color = Colors.BRIGHT_ORANGE_RED if severity == 'high' else Colors.YELLOW if severity == 'medium' else Colors.RESET
                    print(f"  {color}{severity.upper()}: {count}{Colors.RESET}")
            
            print(f"\n{Colors.YELLOW}💡 AI DRY Principle Recommendations:{Colors.RESET}")
            print("1. Extract common code into reusable functions")
            print("2. Create utility modules for repeated patterns")
            print("3. Use inheritance or composition to reduce duplication")
            print("4. Implement template methods for similar algorithms")
            print("5. Consider using design patterns (Strategy, Template Method, etc.)")
            print("6. Refactor similar logic into parameterized functions")
            
        else:
            print(f"\n{Colors.YELLOW}✅ AI overlap analysis complete - No code duplications detected!{Colors.RESET}")
            print("Your code follows the DRY principle well.")
        
        # Print token usage summary
        overlap_token_tracker.print_summary()
        
    except Exception as e:
        print(f"Error: {e}")