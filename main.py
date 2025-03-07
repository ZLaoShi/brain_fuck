#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
棍语言转换器主程序
Created by: ZLaoShi
Last modified: 2025-03-06 18:46:39 UTC
"""

from gun_converter import GunConverter
import sys
import os

def main():
    """主程序入口"""
    if len(sys.argv) != 2:
        print("使用方法: gun_converter <directory>")
        return

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"错误：{directory} 不是有效目录")
        return

    converter = GunConverter()
    converter.create_name_mapping(directory)
    print(f"转换完成，映射关系已保存到 name_mapping.md")

if __name__ == "__main__":
    main()