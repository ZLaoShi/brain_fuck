#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
棍语言文件转换器
Created by: ZLaoShi
Last modified: 2025-03-06 19:22:51 UTC
"""

import os
import re
import platform
from typing import List, Tuple, Dict
from gun_lang import GunEncoder

class GunConverter:
    """棍语言文件转换器类"""
    
    def __init__(self):
        """初始化转换器"""
        self.encoder = GunEncoder()
        self.processed_files: Dict[str, Tuple[str, str]] = {}  # 记录处理过的文件
        # 检测操作系统类型
        self.is_windows = platform.system().lower() == 'windows'
        # Windows 不允许用作文件名的字符
        self.windows_invalid_chars = '<>:"/\\|?*'
        
    def sanitize_filename(self, filename: str) -> str:
        """根据操作系统清理文件名"""
        if self.is_windows:
            # Windows 路径处理
            # 替换 Windows 不允许的字符
            for char in self.windows_invalid_chars:
                filename = filename.replace(char, '_')
            # 确保文件名不以点或空格结尾
            filename = filename.rstrip('. ')
            # 限制文件名长度
            name, ext = os.path.splitext(filename)
            if len(filename) > 255:
                return name[:255-len(ext)] + ext
        return filename
    
    def process_directory(self, directory: str) -> List[Tuple[str, str, str]]:
        """递归处理目录
        Returns: List of (original_path, converted_path, original_name)
        """
        results = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                original_path = os.path.join(root, file)
                if file.endswith('.md'):
                    # 处理 Markdown 文件内容
                    self.process_markdown_file(original_path)
                    results.append((original_path, original_path, file))
                else:
                    # 转换非 .md 文件名
                    converted_name = self.convert_filename(file)
                    # 应用平台特定的文件名清理
                    converted_name = self.sanitize_filename(converted_name)
                    converted_path = os.path.join(root, converted_name)
                    
                    try:
                        # 检查目标路径是否已存在
                        if os.path.exists(converted_path) and original_path != converted_path:
                            base, ext = os.path.splitext(converted_name)
                            counter = 1
                            while os.path.exists(converted_path):
                                new_name = f"{base}_{counter}{ext}"
                                converted_path = os.path.join(root, new_name)
                                counter += 1
                        
                        # 实际重命名文件
                        if original_path != converted_path:
                            os.rename(original_path, converted_path)
                            
                        results.append((original_path, converted_path, file))
                        self.processed_files[converted_path] = (original_path, file)
                    except OSError as e:
                        print(f"警告：无法重命名文件 {original_path} -> {converted_path}")
                        print(f"错误信息：{str(e)}")
                        # 保持原始文件名
                        results.append((original_path, original_path, file))
                        self.processed_files[original_path] = (original_path, file)
        
        return results
    
    def convert_filename(self, filename: str) -> str:
        """转换文件名为棍语言，保留点号但转换扩展名"""
        if filename.endswith('.md'):
            return filename
        
        # 分离文件名和扩展名（包含点号）
        name, ext = os.path.splitext(filename)
        
        # 如果有扩展名（ext包含点号）
        if ext:
            # 保留点号，但转换扩展名中除点号外的部分
            dot_ext = ext[1:]  # 去掉点号
            if dot_ext:  # 如果扩展名非空
                _, gun_ext = self.encoder.encode_text(dot_ext)
                ext = '.' + gun_ext  # 重新加上点号
        
        # 转换主文件名
        _, gun_name = self.encoder.encode_text(name)
        
        # 组合转换后的文件名和扩展名
        return gun_name + ext
    
    def process_markdown_file(self, file_path: str) -> List[Tuple[str, str, int]]:
        """处理 Markdown 文件
        Returns: List of (original_line, converted_line, line_number)
        """
        converted_lines = []
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines, 1):
            # 跳过注释行（以 # 开头的行）
            if line.strip().startswith('#'):
                converted_lines.append((line, line, i))
                continue
            
            # 转换非注释行
            converted_line = self.convert_markdown_line(line)
            converted_lines.append((line, converted_line, i))
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            for _, converted, _ in converted_lines:
                f.write(converted)
        
        return converted_lines
    
    def convert_markdown_line(self, line: str) -> str:
        """转换 Markdown 行内容为棍语言，保留 Markdown 语法结构"""
        # 保持以下行不变
        if any(line.strip().startswith(prefix) for prefix in ['#', '>', '```', '    ', '\t']):
            return line
            
        # 处理代码块
        if '```' in line:
            return line
        
        # 使用更精确的正则表达式保留 Markdown 语法
        def convert_text(match):
            text = match.group(0)
            # 跳过所有 Markdown 语法标记
            if any(marker in text for marker in ('`', '[', ']', '(', ')', '*', '_', '#', '```', '>', '|')):
                return text
            # 只转换普通文本
            if text.strip():
                octal, gun_code = self.encoder.encode_text(text)
                return gun_code
            return text  # 保留空白字符
        
        # 更新正则表达式模式
        pattern = r'[^`\[\]()\\<>*_#>|]+|[`\[\]()\\<>*_#>|]+'
        parts = re.finditer(pattern, line)
        return ''.join(convert_text(match) for match in parts)
    
    def get_original_name(self, converted_path: str) -> Tuple[str, str]:
        """获取原始文件路径和名称"""
        return self.processed_files.get(converted_path, (converted_path, converted_path))
    
    def create_name_mapping(self, directory: str, output_file: str = "name_mapping.md"):
        """创建文件名映射的 Markdown 文档"""
        results = self.process_directory(directory)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 文件名映射关系\n\n")
            f.write("| 原始文件名 | 转换后文件名 | 说明 |\n")
            f.write("|------------|--------------|------|\n")
            
            for orig_path, conv_path, orig_name in results:
                # 提取相对路径
                rel_orig = os.path.relpath(orig_path, directory)
                rel_conv = os.path.relpath(conv_path, directory)
                f.write(f"| {rel_orig} | {rel_conv} | |\n")

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) != 2:
        print("使用方法: python3 gun_converter.py <directory>")
        return
    
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"错误：{directory} 不是一个有效的目录")
        return
    
    converter = GunConverter()
    
    try:
        # 创建映射文件
        converter.create_name_mapping(directory)
        print(f"转换完成，映射关系已保存到 name_mapping.md")
    except Exception as e:
        print(f"错误：转换过程中发生异常：{str(e)}")

if __name__ == "__main__":
    main()