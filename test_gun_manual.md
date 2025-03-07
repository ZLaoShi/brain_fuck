# 创建测试目录结构
mkdir -p test_convert/docs test_convert/src

# 创建一些测试文件
# Markdown文件
echo "# 测试文档
这是一个测试文件
## 第二节
代码示例：
\`\`\`python
print('hello')
\`\`\`" > test_convert/docs/readme.md

# 普通文本文件
echo "这是源代码" > test_convert/src/main.txt
echo "配置文件" > test_convert/config.txt

# 运行转换
python3 gun_converter.py test_convert