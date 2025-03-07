#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
棍语言编码器
Created by: ZLaoShi
Last modified: 2025-03-06 17:50:59 UTC
"""

import hashlib
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple

class GunEncoder:
    """棍语言编码器类"""
    
    # 字符映射规则
    CHAR_MAP = {
        '0': ' ',    # 空格
        '1': 'I',    # 大写字母I
        '2': 'l',    # 小写字母l
        '3': '|',    # 竖线
        '4': '∣',    # U+2223
        '5': '╸',    # U+2578
        '6': '⏐',    # U+23D0
        '7': '｜'    # U+FF5C
    }
    
    # 反向映射
    REVERSE_MAP = {v: k for k, v in CHAR_MAP.items()}
    
    def __init__(self, history_file: str = None):
        """初始化编码器"""
        if history_file is None:
            self.history_file = os.path.expanduser("~/.gun_history")
        else:
            self.history_file = history_file
        
        # 确保历史记录目录存在
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
    
    def _md5_to_binary(self, text: str) -> str:
        """将文本转换为MD5哈希，然后转换为二进制，确保生成24位二进制"""
        md5_hash = hashlib.md5(text.encode()).hexdigest()
        binary = ''
        # 修改：只取前6个字符，因为每个十六进制字符产生4位二进制
        # 6个十六进制字符 * 4位二进制 = 24位二进制
        # 24位二进制刚好可以生成8个三位组（用于八进制）
        for i in range(6):  # 改为6，而不是8
            hex_char = md5_hash[i]
            bin_str = bin(int(hex_char, 16))[2:].zfill(4)
            binary += bin_str
        return binary[:24]  # 确保只有24位

    def _binary_to_octal(self, binary: str) -> str:
        """将24位二进制转换为8位八进制"""
        octal = ''
        # 每3位二进制转换为1位八进制
        for i in range(0, 24, 3):
            group = binary[i:i+3]
            if len(group) < 3:  # 处理最后一组可能不足3位的情况
                group = group.ljust(3, '0')
            val = int(group, 2)
            octal += str(val)
        return octal
    
    def encode_text(self, text: str) -> Tuple[str, str]:
        """编码文本为棍语言"""
        # 检查是否是.md文件
        if text.endswith('.md'):
            extension = '.md'
            main_text = text[:-3]
        else:
            extension = ''
            main_text = text
            if '.' in text:
                base, ext = text.rsplit('.', 1)
                main_text = base
                # 对扩展名进行编码
                ext_hash = hashlib.md5(ext.encode()).hexdigest()
                ext_code = f".{int(ext_hash[0], 16) % 8}{int(ext_hash[1], 16) % 8}"
                extension = ext_code
        
        # 生成二进制
        binary = self._md5_to_binary(main_text)
        
        # 转换为八进制
        octal = self._binary_to_octal(binary)
        
        # 添加扩展名
        full_octal = octal + extension
        
        # 转换为棍语言
        gun_code = ''.join(self.CHAR_MAP[c] if c in self.CHAR_MAP else c for c in full_octal)
        
        return full_octal, gun_code
    
    def decode_text(self, gun_code: str) -> str:
        """解码棍语言"""
        # 分离扩展名
        if '.md' in gun_code:
            main_code = gun_code[:-3]
            extension = '.md'
        elif '.' in gun_code:
            main_code, ext_code = gun_code.rsplit('.', 1)
            extension = f".{ext_code}"
        else:
            main_code = gun_code
            extension = ''
        
        # 转换主要部分
        octal = ''.join(self.REVERSE_MAP.get(c, c) for c in main_code)
        
        # 如果有扩展名，添加回来
        if extension:
            octal += extension
            
        return octal
    
    def add_history(self, text: str, octal: str, gun_code: str):
        """添加到历史记录"""
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        
        with open(self.history_file, 'a', encoding='utf-8') as f:
            f.write('---\n')
            f.write(f'时间: {timestamp}\n')
            f.write(f'文本: {text}\n')
            f.write(f'八进制: {octal}\n')
            f.write(f'棍语言: {gun_code}\n')
    
    def search_history(self, octal: str) -> Optional[str]:
        """搜索历史记录"""
        if not os.path.exists(self.history_file):
            return None
            
        with open(self.history_file, 'r', encoding='utf-8') as f:
            content = f.read()
            records = content.split('---\n')
            
            for record in records:
                if f'八进制: {octal}\n' in record:
                    return '---\n' + record.strip()
        
        return None
    
    def show_history(self):
        """显示历史记录"""
        if not os.path.exists(self.history_file):
            print("没有找到历史记录")
            return
        
        print("编码历史记录：")
        count = 0
        
        with open(self.history_file, 'r', encoding='utf-8') as f:
            content = f.read()
            records = content.split('---\n')
            
            for record in records[1:]:  # 跳过第一个空记录
                count += 1
                print(f"\n记录 #{count}:")
                print(record.strip())
        
        if count == 0:
            print("暂无记录")
        else:
            print(f"\n共找到 {count} 条记录")
    
    def clear_history(self):
        """清空历史记录"""
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
            print("历史记录已清空")

def main():
    """主函数"""
    encoder = GunEncoder()
    
    if len(sys.argv) < 2:
        show_usage()
        return
    
    command = sys.argv[1]
    
    if command == "encode-text":
        print("请输入要编码的文本（支持中文）：")
        text = input().strip()
        if not text:
            print("错误：输入不能为空")
            return
            
        octal, gun_code = encoder.encode_text(text)
        print("\n编码结果：")
        print(f"输入文本: {text}")
        print(f"八进制值: {octal}")
        print(f"棍语言码: {gun_code}")
        
        encoder.add_history(text, octal, gun_code)
        
    elif command == "decode":
        print("请输入棍语言代码：")
        gun_code = input().strip()
        if not gun_code:
            print("错误：输入不能为空")
            return
            
        octal = encoder.decode_text(gun_code)
        print("\n解码结果：")
        print(f"棍语言码: {gun_code}")
        print(f"八进制值: {octal}")
        
        print("\n查找历史记录...")
        result = encoder.search_history(octal)
        if result:
            print(f"找到匹配记录：\n{result}")
        else:
            print("未找到对应的原始文本")
            
    elif command == "history":
        encoder.show_history()
        
    elif command == "clear-history":
        encoder.clear_history()
        
    elif command == "help":
        show_usage()
        
    else:
        print("无效的命令")
        show_usage()

def show_usage():
    """显示使用方法"""
    print(f"""棍语言编码器 v3.0 - 使用方法：
    编码文本:     {sys.argv[0]} encode-text
    解码:         {sys.argv[0]} decode
    显示历史:     {sys.argv[0]} history
    清空历史:     {sys.argv[0]} clear-history
    查看帮助:     {sys.argv[0]} help

字符映射关系：
    0 => [空格]
    1 => I（大写字母I）
    2 => l（小写字母l）
    3 => |（竖线）
    4 => ∣（U+2223）
    5 => ╸（U+2578）
    6 => ⏐（U+23D0）
    7 => ｜（U+FF5C）""")

if __name__ == "__main__":
    main()