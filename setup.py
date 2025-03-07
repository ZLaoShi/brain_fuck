#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
棍语言转换器安装配置
Created by: ZLaoShi
Last modified: 2025-03-06 18:46:39 UTC
"""

from setuptools import setup, find_packages

setup(
    name="gun_converter",
    version="1.0.0",
    author="ZLaoShi",
    description="棍语言文件转换器",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "pyinstaller",  # 用于打包exe
    ],
)