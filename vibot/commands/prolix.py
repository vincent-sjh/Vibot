#!/usr/bin/env python3
"""vibot prolix command implementation"""

import os
from ..utils import should_skip_file


def find_prolix_files(path, max_lines=200):
    """Find verbose files with lines exceeding specified value in given path"""
    try:
        if not os.path.exists(path):
            print(f"Error: Path '{path}' does not exist")
            return
        
        if not os.path.isdir(path):
            print(f"Error: '{path}' is not a directory")
            return
        
        print(f"Searching for files with more than {max_lines} lines in: {os.path.abspath(path)}")
        print("=" * 60)
        
        prolix_files = []
        
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip binary files and special files
                if should_skip_file(file):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        line_count = sum(1 for _ in f)
                    
                    if line_count > max_lines:
                        relative_path = os.path.relpath(file_path, path)
                        prolix_files.append((relative_path, line_count))
                        
                except (UnicodeDecodeError, PermissionError, IsADirectoryError):
                    # Skip unreadable files
                    continue
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
        
        if prolix_files:
            # Sort by line count in descending order
            prolix_files.sort(key=lambda x: x[1], reverse=True)
            
            print(f"Found {len(prolix_files)} files with more than {max_lines} lines:")
            print("-" * 60)
            
            for file_path, line_count in prolix_files:
                print(f"{file_path:<50} {line_count:>6} lines")
        else:
            print(f"No files found with more than {max_lines} lines.")
        
        print("=" * 60)
        print(f"Search completed. Threshold: {max_lines} lines")
        
    except Exception as e:
        print(f"Error: {e}")