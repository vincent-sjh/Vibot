#!/usr/bin/env python3
"""vibot 公共工具函数"""

import os


class Colors:
    """ANSI 颜色代码"""
    ORANGE = '\033[93m'  # 使用亮黄色作为橙色
    BRIGHT_ORANGE_RED = '\033[91m'  # 接近红色的亮橙色（亮红色）
    YELLOW = '\033[93m'
    BROWN = '\033[33m'
    RESET = '\033[0m'


def print_logo():
    """打印 vibot 字符画 logo"""
    logo_color = Colors.BRIGHT_ORANGE_RED
    subtitle_color = Colors.BRIGHT_ORANGE_RED
    reset_code = Colors.RESET
    
    logo = f"""{logo_color}
██╗   ██╗██╗██████╗  ██████╗ ████████╗
██║   ██║██║██╔══██╗██╔═══██╗╚══██╔══╝
██║   ██║██║██████╔╝██║   ██║   ██║   
╚██╗ ██╔╝██║██╔══██╗██║   ██║   ██║   
 ╚████╔╝ ██║██████╔╝╚██████╔╝   ██║   
  ╚═══╝  ╚═╝╚═════╝  ╚═════╝    ╚═╝{reset_code}
  
{subtitle_color}
| Your AI Code Assistant Specifically designed for Vibe-Coding. |
| ^^^^ ^^ ^^^^ ^^^^^^^^^ ^^^^^^^^^^^^ ^^^^^^^^ ^^^ ^^^^^^^^^^^^ |{reset_code}  
"""
    print(logo)


def should_skip_file(filename):
    """判断是否应该跳过某个文件"""
    # 跳过的文件扩展名
    skip_extensions = {
        '.exe', '.dll', '.so', '.dylib', '.bin', '.obj', '.o',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.svg',
        '.mp3', '.mp4', '.avi', '.mov', '.wav', '.flac',
        '.zip', '.tar', '.gz', '.rar', '.7z',
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'
    }
    
    # 跳过的文件名
    skip_names = {
        '.DS_Store', 'Thumbs.db', '.gitignore', '.git'
    }
    
    _, ext = os.path.splitext(filename)
    return ext.lower() in skip_extensions or filename in skip_names