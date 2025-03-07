# 棍语言转换器 (Gun Language Converter)

![版本](https://img.shields.io/badge/version-0.0.1-blue.svg)
![Python版本](https://img.shields.io/badge/python-3.6%2B-blue)
![许可证](https://img.shields.io/badge/license-MIT-green.svg)

> 🔄 一个将普通文件名转换为棍语言(Gun Language)的工具
>
> 作者: ZLaoShi
>
> 最后更新: 2025-03-07

## 📝 简介

棍语言转换器是一个用于将普通文件名转换为棍语言的工具。它可以批量处理目录中的文件，自动生成映射关系文档，并支持 .md 文件内容的转换。

### 什么是棍语言？

棍语言是一种使用 `|`、`I`、`l`、`∣` 等字符组合的特殊编码方式，能够将普通文本转换为类似竖线的表示形式。

### 灵感来源



## 🚀 功能特点

- 批量转换文件名为棍语言
- 保持 .md 文件名不变，仅转换其内容，会跳过#符号后的内容
- 自动生成名称映射文档
- 支持 Windows 和 Linux 系统
- 提供图形界面和命令行两种使用方式

## 📦 安装

### 方式一：使用预编译的可执行文件

1. 从 [Releases](https://github.com/ZLaoShi/brain_fuck/releases) 页面下载最新版本
2. 解压下载的文件
3. 直接运行可执行文件

### 方式二：从源码安装

```bash
# 克隆仓库
git clone https://github.com/ZLaoShi/brain_fuck.git
cd brain_fuck

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install pyinstaller

# 打包
pyinstaller --onefile main.py --name gun_converter
```

## 💻 使用方法

### 命令行使用

```bash
# Windows
gun_converter.exe <directory>

# Linux/Mac
./gun_converter <directory>
```

### 示例

```bash
# 转换当前目录
gun_converter.exe .

# 转换指定目录
gun_converter.exe path/to/directory
```

## 📄 输出文件

- `name_mapping.md`: 记录原始文件名和转换后文件名的对应关系
- 转换后的文件将保持原有目录结构

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 注意事项

- 建议在使用前备份重要文件
- 某些特殊字符可能在不同操作系统中显示不同
- Windows 系统中某些特殊字符可能无法用作文件名

## 🔧 故障排除

### 常见问题

1. **文件名无效**
   - 问题：Windows 系统报告文件名无效
   - 解决：程序会自动将无效字符替换为下划线

2. **权限问题**
   - 问题：无法访问或修改文件
   - 解决：确保有足够的文件系统权限

## 📜 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🔗 相关链接

- [项目主页](https://github.com/ZLaoShi/brain_fuck)
- [问题报告](https://github.com/ZLaoShi/brain_fuck/issues)
- [更新日志](CHANGELOG.md)

## 📞 联系方式

- GitHub: [@ZLaoShi](https://github.com/ZLaoShi)

## 🙏 鸣谢

感谢所有贡献者对本项目的支持！

---

> 注：本项目仅供学习和研究使用，请勿用于非法用途。