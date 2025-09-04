#!/usr/bin/env python3
"""vibot detect command implementation"""

import os
from ..utils import should_skip_file


def print_file_tree(path, prefix="", is_last=True):
    """Recursively print file tree"""
    try:
        items = sorted(os.listdir(path))
        dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
        files = [item for item in items if os.path.isfile(os.path.join(path, item))]
        
        # Print files first
        for i, file in enumerate(files):
            is_last_file = (i == len(files) - 1) and len(dirs) == 0
            connector = "└── " if is_last_file else "├── "
            print(f"{prefix}{connector}{file}")
        
        # Then print directories
        for i, dir_name in enumerate(dirs):
            is_last_dir = (i == len(dirs) - 1)
            connector = "└── " if is_last_dir else "├── "
            print(f"{prefix}{connector}{dir_name}/")
            
            # Recursively print subdirectories
            new_prefix = prefix + ("    " if is_last_dir else "│   ")
            print_file_tree(os.path.join(path, dir_name), new_prefix, is_last_dir)
            
    except PermissionError:
        print(f"{prefix}├── [Permission Denied]")
    except Exception as e:
        print(f"{prefix}├── [Error: {e}]")


def count_files_by_extension(path):
    """Recursively count files by extension in specified path"""
    extension_count = {}
    total_files = 0
    
    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                total_files += 1
                # Get file extension
                _, ext = os.path.splitext(file)
                
                # If no extension, use special identifier
                if not ext:
                    ext = "[no extension]"
                else:
                    # Convert to lowercase
                    ext = ext.lower()
                
                # Count
                extension_count[ext] = extension_count.get(ext, 0) + 1
                
    except PermissionError:
        print(f"Error: Permission denied for path '{path}'")
        return {}, 0
    except Exception as e:
        print(f"Error: {e}")
        return {}, 0
    
    return extension_count, total_files


def detect_files_in_directory(path):
    """Detect and display directory information"""
    try:
        if not os.path.exists(path):
            print(f"Error: Path '{path}' does not exist")
            return
        
        if not os.path.isdir(path):
            print(f"Error: '{path}' is not a directory")
            return
        
        print(f"Directory tree for: {os.path.abspath(path)}")
        print("=" * 50)
        
        # Print root directory name
        print(f"{os.path.basename(os.path.abspath(path))}/")
        
        # Print file tree
        print_file_tree(path)
        
        print("=" * 50)
        
        # Recursively count files and extension distribution
        extension_count, total_files = count_files_by_extension(path)
        
        print(f"Total files found: {total_files}")
        
        if extension_count:
            print("\nFile extension statistics:")
            print("-" * 30)
            
            # Sort by file count in descending order
            sorted_extensions = sorted(extension_count.items(), key=lambda x: x[1], reverse=True)
            
            for ext, count in sorted_extensions:
                if ext == "[no extension]":
                    print(f"  {ext:<15}: {count:>4} files")
                else:
                    print(f"  {ext:<15}: {count:>4} files")
        
    except Exception as e:
        print(f"Error: {e}")