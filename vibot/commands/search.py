#!/usr/bin/env python3
"""vibot search command implementation"""

import os
from ..utils import should_skip_file


def search_keyword_in_files(path, keyword):
    """Search for keyword in all files under specified path"""
    try:
        if not os.path.exists(path):
            print(f"Error: Path '{path}' does not exist")
            return
        
        if not os.path.isdir(path):
            print(f"Error: '{path}' is not a directory")
            return
        
        print(f"Searching for keyword '{keyword}' in: {os.path.abspath(path)}")
        print("=" * 60)
        
        total_matches = 0
        files_with_matches = 0
        
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip binary files and special files
                if should_skip_file(file):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        
                    file_matches = 0
                    for line_num, line in enumerate(lines, 1):
                        if keyword in line:
                            if file_matches == 0:
                                # First match found in this file, print file path
                                print(f"\nFile: {os.path.relpath(file_path, path)}")
                                print("-" * 40)
                            
                            # Print match information
                            print(f"Line {line_num}: {line.rstrip()}")
                            
                            # Use caret to indicate keyword position
                            pointer_line = " " * (len(f"Line {line_num}: "))
                            start_pos = 0
                            while True:
                                pos = line.find(keyword, start_pos)
                                if pos == -1:
                                    break
                                pointer_line += " " * (pos - start_pos) + "^" * len(keyword)
                                start_pos = pos + len(keyword)
                            
                            print(pointer_line)
                            file_matches += 1
                            total_matches += 1
                    
                    if file_matches > 0:
                        files_with_matches += 1
                        
                except (UnicodeDecodeError, PermissionError, IsADirectoryError):
                    # Skip unreadable files
                    continue
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
        
        print("\n" + "=" * 60)
        print(f"Search completed:")
        print(f"  Keyword: '{keyword}'")
        print(f"  Files with matches: {files_with_matches}")
        print(f"  Total matches: {total_matches}")
        
    except Exception as e:
        print(f"Error: {e}")