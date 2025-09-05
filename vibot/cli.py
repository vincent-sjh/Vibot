#!/usr/bin/env python3
"""vibot CLI main module"""

import argparse
import sys
import os

# Add current directory to Python path for vibot module import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vibot import __version__
from .utils import print_logo
from .commands import detect_files_in_directory, search_keyword_in_files, find_prolix_files, detect_hardcoded_secrets, analyze_functions_in_directory, analyze_readability_in_directory, analyze_comments_in_directory, analyze_magic_in_directory, analyze_overlap_in_directory, analyze_naming_in_directory


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog='vibot',
        description='VIBOT - AI Code Assistant Specifically designed for Vibe-Coding.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'vibot {__version__}'
    )
    
    parser.add_argument(
        '-d',
        '--detect',
        action='store_true',
        help='analyze directory structure and file distribution - detects file types, counts, and generates file tree visualization'
    )
    
    parser.add_argument(
        '-s',
        '--search',
        action='store_true',
        help='search for specific keywords in code files - finds function names, variables, TODO markers, API calls with context'
    )
    
    parser.add_argument(
        '-p',
        '--prolix',
        action='store_true',
        help='detect overly long files that may need refactoring - identifies files exceeding line count thresholds and suggests modularization'
    )
    
    parser.add_argument(
        '-l',
        '--logo',
        action='store_true',
        help='display the VIBOT ASCII art logo'
    )
    
    parser.add_argument(
        '-u',
        '--ustalony',
        action='store_true',
        help='🤖 AI-powered detection of hardcoded secrets, API keys, passwords, tokens, and sensitive information in code'
    )
    
    parser.add_argument(
        '-f',
        '--function',
        action='store_true',
        help='🤖 AI-powered function quality analysis - detects overly long functions, excessive parameters, and suggests refactoring'
    )
    
    parser.add_argument(
        '-r',
        '--readability',
        action='store_true',
        help='🤖 AI-powered code readability analysis - detects long lines, complex ternary operators, and missing line separations'
    )
    
    parser.add_argument(
        '-c',
        '--comment',
        action='store_true',
        help='🤖 AI-powered code comments analysis - detects useless comments and missing comments'
    )
    
    parser.add_argument(
        '-m',
        '--magic',
        action='store_true',
        help='🤖 AI-powered magic numbers/strings detection - identifies hardcoded values that should be named constants'
    )
    
    parser.add_argument(
        '-o',
        '--overlap',
        action='store_true',
        help='🤖 AI-powered duplicate code detection - identifies exact duplicates, similar logic, and repeated patterns that violate DRY principle'
    )
    
    parser.add_argument(
        '-n',
        '--name',
        action='store_true',
        help='🤖 AI-powered naming convention analysis - detects oversimplified names, obscure abbreviations, inconsistent styles, meaningless names, and constant naming issues'
    )
    
    parser.add_argument(
        '-g',
        '--gluttonous',
        action='store_true',
        help='Play a gluttonous snake game in terminal!'
    )
    
    parser.add_argument(
        '--map-size',
        type=int,
        default=10,
        help='Map size for gluttonous snake game (default: 10)'
    )
    
    parser.add_argument(
        '--path',
        type=str,
        default='.',
        help='specify the directory or file path to analyze (default: current directory)'
    )
    
    parser.add_argument(
        '--key',
        type=str,
        help='keyword or pattern to search for in code files (required with --search) - e.g., function names, TODO, FIXME, API calls'
    )
    
    parser.add_argument(
        '--max',
        type=int,
        default=200,
        help='maximum line count threshold for detecting overly long files that may need refactoring (default: 200)'
    )
    
    parser.add_argument(
        '--max-lines',
        type=int,
        default=50,
        help='maximum lines per function threshold for quality analysis - functions exceeding this may need refactoring (default: 50)'
    )
    
    parser.add_argument(
        '--max-params',
        type=int,
        default=5,
        help='maximum number of parameters per function threshold - functions with more parameters may have design issues (default: 5)'
    )
    
    parser.add_argument(
        '--max-line-length',
        type=int,
        default=80,
        help='maximum characters per line threshold for readability analysis - longer lines may hurt code readability (default: 80)'
    )
    
    parser.add_argument(
        '--min-duplicate-lines',
        type=int,
        default=3,
        help='minimum number of lines required to consider code as duplicate - smaller duplicates will be ignored (default: 3)'
    )
    

    

    # Check if logo should be displayed (except for --version, --logo, and --gluttonous arguments)
    if not any(arg in sys.argv for arg in ['-v', '--version', '-l', '--logo', '-g', '--gluttonous']):
        print_logo()
    
    
    args = parser.parse_args()
    

    if args.logo:
        print_logo()
    elif args.detect:
        detect_files_in_directory(args.path)
    elif args.search:
        if not args.key:
            print("Error: --key is required when using --search")
            parser.print_help()
            return
        search_keyword_in_files(args.path, args.key)
    elif args.prolix:
        find_prolix_files(args.path, getattr(args, 'max'))
    elif args.ustalony:
        detect_hardcoded_secrets(args.path)
    elif args.function:
        analyze_functions_in_directory(
            args.path, 
            getattr(args, 'max_lines', 50),
            getattr(args, 'max_params', 5)
        )
    elif args.readability:
        analyze_readability_in_directory(
            args.path,
            getattr(args, 'max_line_length', 80)
        )
    elif args.comment:
        analyze_comments_in_directory(args.path)
    elif args.magic:
        analyze_magic_in_directory(args.path)
    elif args.overlap:
        analyze_overlap_in_directory(
            args.path,
            getattr(args, 'min_duplicate_lines', 3)
        )
    elif args.name:
        analyze_naming_in_directory(args.path)
    elif args.gluttonous:
        from vibot.commands.gluttonous import main as snake_main
        snake_main(getattr(args, 'map_size', 10))
    elif len(sys.argv) == 1:
        parser.print_help()


if __name__ == '__main__':
    main()
