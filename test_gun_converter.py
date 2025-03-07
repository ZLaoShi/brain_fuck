#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tempfile
import unittest
from gun_converter import GunConverter

class TestGunConverter(unittest.TestCase):
    """测试棍语言文件转换器"""
    
    def setUp(self):
        """测试前设置"""
        self.temp_dir = tempfile.mkdtemp()
        self.converter = GunConverter()
        
        # 创建测试文件
        self.create_test_files()
    
    def tearDown(self):
        """测试后清理"""
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)
    
    def create_test_files(self):
        """创建测试文件结构"""
        # 创建测试 Markdown 文件
        md_content = """# 这是标题
            这是普通文本
            ## 这是二级标题
            这是更多的文本

            ```python
            print("这是代码块")
            ``` """ 
        with open(os.path.join(self.temp_dir, "test.md"), 'w', encoding='utf-8') as f: f.write(md_content)
        # 创建普通文本文件
        with open(os.path.join(self.temp_dir, "test.txt"), 'w', encoding='utf-8') as f:
            f.write("这是测试文本")
    
        # 创建子目录和文件
        os.makedirs(os.path.join(self.temp_dir, "subdir"))
        with open(os.path.join(self.temp_dir, "subdir", "test2.txt"), 'w', encoding='utf-8') as f:
            f.write("子目录中的测试文本")

    def test_directory_processing(self):
        """测试目录处理"""
        results = self.converter.process_directory(self.temp_dir)
        self.assertTrue(len(results) > 0)
        
        # 验证所有非 .md 文件都被转换
        for orig_path, conv_path, _ in results:
            if not orig_path.endswith('.md'):
                self.assertNotEqual(orig_path, conv_path)

    def test_markdown_processing(self):
        """测试 Markdown 文件处理"""
        md_file = os.path.join(self.temp_dir, "test.md")
        results = self.converter.process_markdown_file(md_file)
        
        for orig, conv, line_num in results:
            if orig.strip().startswith('#'):
                # 标题行应该保持不变
                self.assertEqual(orig, conv)
            elif '```' in orig:
                # 代码块应该保持不变
                self.assertEqual(orig, conv)
            elif '`' in orig:
                # 行内代码应该保持不变
                self.assertTrue('`' in conv)

    def test_filename_conversion(self):
        """测试文件名转换"""
        filename = "test.txt"
        converted = self.converter.convert_filename(filename)
        self.assertNotEqual(filename, converted)
        
        # .md 文件名应该保持不变
        md_filename = "test.md"
        converted_md = self.converter.convert_filename(md_filename)
        self.assertEqual(md_filename, converted_md)

    def test_name_mapping(self):
        """测试名称映射文件生成"""
        mapping_file = os.path.join(self.temp_dir, "name_mapping.md")
        self.converter.create_name_mapping(self.temp_dir, mapping_file)
        
        self.assertTrue(os.path.exists(mapping_file))
        with open(mapping_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("| 原始文件名 | 转换后文件名 | 说明 |", content)

def run_tests():
    """运行所有测试"""
    unittest.main(verbosity=2)

if __name__ == '__main__':
    run_tests()