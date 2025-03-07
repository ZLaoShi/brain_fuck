#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
棍语言编码器测试套件
Created by: ZLaoShi
Last modified: 2025-03-06 17:52:49 UTC
"""

import os
import tempfile
import unittest
from gun_lang import GunEncoder

class TestGunEncoder(unittest.TestCase):
    """测试棍语言编码器的所有功能"""
    
    def setUp(self):
        """每个测试前的设置"""
        # 使用临时文件作为历史记录
        self.temp_dir = tempfile.mkdtemp()
        self.history_file = os.path.join(self.temp_dir, '.gun_history')
        self.encoder = GunEncoder(self.history_file)

    def tearDown(self):
        """每个测试后的清理"""
        # 删除临时文件和目录
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
        os.rmdir(self.temp_dir)

    def test_encode_normal_text(self):
        """测试普通文本编码"""
        text = "test"
        octal, gun_code = self.encoder.encode_text(text)
        self.assertEqual(len(octal), 8, 
                        f"八进制长度应为8位，实际为{len(octal)}位: {octal}")
        self.assertEqual(len(gun_code), 8, 
                        f"棍语言长度应为8位，实际为{len(gun_code)}位: {gun_code}")
        
    def test_encode_with_md_extension(self):
        """测试.md文件编码"""
        text = "test.md"
        octal, gun_code = self.encoder.encode_text(text)
        self.assertTrue(octal.endswith('.md'))
        self.assertTrue(gun_code.endswith('.md'))

    def test_encode_with_other_extension(self):
        """测试其他扩展名编码"""
        text = "test.txt"
        octal, gun_code = self.encoder.encode_text(text)
        self.assertTrue('.' in octal)
        self.assertTrue('.' in gun_code)
        self.assertEqual(len(octal.split('.')[1]), 2)  # 扩展名应该是2位

    def test_decode_normal(self):
        """测试普通棍语言解码"""
        gun_code = "Il|∣╸⏐｜ "
        octal = self.encoder.decode_text(gun_code)
        self.assertEqual(len(octal), 8)

    def test_decode_with_md(self):
        """测试带.md扩展名的解码"""
        gun_code = "Il|∣╸⏐｜ .md"
        octal = self.encoder.decode_text(gun_code)
        self.assertTrue(octal.endswith('.md'))

    def test_decode_with_extension(self):
        """测试带其他扩展名的解码"""
        gun_code = "Il|∣╸⏐｜ .∣｜"
        octal = self.encoder.decode_text(gun_code)
        self.assertTrue('.' in octal)
        self.assertEqual(len(octal.split('.')[1]), 2)

    def test_history_operations(self):
        """测试历史记录操作"""
        # 测试添加历史记录
        text = "test.txt"
        octal, gun_code = self.encoder.encode_text(text)
        self.encoder.add_history(text, octal, gun_code)
        
        # 测试搜索历史记录
        result = self.encoder.search_history(octal)
        self.assertIsNotNone(result)
        self.assertIn(text, result)
        
        # 测试清空历史记录
        self.encoder.clear_history()
        self.assertFalse(os.path.exists(self.history_file))

    def test_chinese_text(self):
        """测试中文文本"""
        text = "测试文本.txt"
        octal, gun_code = self.encoder.encode_text(text)
        main_octal = octal.split('.')[0]
        main_gun = gun_code.split('.')[0]
        self.assertEqual(len(main_octal), 8, 
                        f"八进制主要部分长度应为8位，实际为{len(main_octal)}位: {main_octal}")
        self.assertEqual(len(main_gun), 8, 
                        f"棍语言主要部分长度应为8位，实际为{len(main_gun)}位: {main_gun}")

    def test_special_characters(self):
        """测试特殊字符"""
        text = "test!@#$%^&*.txt"
        octal, gun_code = self.encoder.encode_text(text)
        main_octal = octal.split('.')[0]
        main_gun = gun_code.split('.')[0]
        self.assertEqual(len(main_octal), 8, 
                        f"八进制主要部分长度应为8位，实际为{len(main_octal)}位: {main_octal}")
        self.assertEqual(len(main_gun), 8, 
                        f"棍语言主要部分长度应为8位，实际为{len(main_gun)}位: {main_gun}")

def run_tests():
    """运行所有测试"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGunEncoder)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_tests()