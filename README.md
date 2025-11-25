# MOU书自动化发布系统

## 项目简介

MOU书自动化发布系统是一个集成了Excel内容生成和MOU书自动发布功能的Python应用程序。该系统能够自动为Excel中的标题生成内容，并将生成的内容发布到MOU书平台，实现了从内容创作到发布的全流程自动化。

## 功能特性

### 1. Excel内容生成
- 支持从Excel文件读取标题
- 使用DeepSeek API自动生成符合MOU书风格的内容
- 生成的内容限制在700字符以内
- 智能过滤非BMP字符，确保ChromeDriver兼容性
- 自动保存生成的内容到原Excel文件

### 2. MOU书自动发布
- 支持Chrome浏览器自动化操作
- 提供复用浏览器功能，避免重复登录
- 自动处理登录流程
- 支持自动发布笔记，包括标题、内容和图片
- 提供详细的日志输出

### 3. 浏览器管理
- 支持无头模式和有头模式
- 支持Chrome配置文件复用
- 自动处理浏览器启动和关闭
- 支持浏览器窗口大小调整

### 4. 登录管理
- 支持手机号+密码登录
- 支持验证码登录
- 支持创作服务平台登录
- 自动处理登录弹窗

## 安装要求

### 硬件要求
- 操作系统：Windows 10/11
- CPU：Intel i5或同等性能以上
- 内存：8GB或以上
- 硬盘空间：至少500MB可用空间

### 软件要求
1. Python 3.11或以上版本
2. Chrome浏览器 142.0或以上版本
3. 对应版本的ChromeDriver（已包含在项目中）
4. 以下Python库：
   - selenium
   - openpyxl
   - openai
   - python-dotenv

### 环境配置

1. 克隆或下载项目到本地
2. 安装依赖库：
   ```bash
   pip install selenium openpyxl openai python-dotenv
   ```
3. 配置DeepSeek API密钥：
   - 打开`main.py`文件
   - 在第198行修改API密钥：
     ```python
     api_key = 'your_deepseek_api_key_here'
     ```

## 使用说明

### 1. 准备Excel文件

创建一个名为`xiaohongshu_content.xlsx`的Excel文件，格式如下：
- 第1列：标题（必填）
- 第2列：内容（自动生成）

示例：
| 标题 | 内容 |
|------|------|
| 春日穿搭指南 | （自动生成） |
| 美食探店分享 | （自动生成） |

### 2. 运行主程序

```bash
python main.py
```

### 3. 命令行参数

```bash
# 保持浏览器打开状态
python main.py --keep-browser-open

# 复用已打开的浏览器
python main.py --reuse-browser
```

## 项目结构

```
.
├── main.py                    # 主程序入口
├── browser_manager.py         # 浏览器管理模块
├── content_reader.py          # 内容读取模块
├── login_manager.py           # 登录管理模块
├── popup_handler.py           # 弹窗处理模块
├── publisher.py               # 发布管理模块
├── chromedriver.exe           # ChromeDriver可执行文件
├── xiaohongshu_content.xlsx   # Excel内容文件
├── chrome_profile/            # Chrome配置文件目录
├── .venv/                     # Python虚拟环境
└── README.md                  # 项目说明文档
```

## 模块说明

### main.py
主程序入口，集成了Excel内容生成和MOU书自动发布流程。

### browser_manager.py
负责浏览器的启动、配置和关闭，支持无头模式和有头模式。

### content_reader.py
负责从Excel文件读取笔记数据，包括标题、内容和图片路径。

### login_manager.py
处理MOU书登录流程，支持手机号+密码登录和验证码登录。

### popup_handler.py
处理浏览器中的各类弹窗，包括登录弹窗、广告弹窗等。

### publisher.py
负责笔记发布流程，包括标题输入、内容输入、图片上传和发布按钮点击。

## 配置说明

### ChromeDriver配置
ChromeDriver已包含在项目中，版本为142.0.7444.163，与Chrome 142.0版本兼容。如果需要使用其他版本的Chrome浏览器，请下载对应版本的ChromeDriver并替换项目中的`chromedriver.exe`文件。

### Chrome配置文件
项目使用`chrome_profile`目录作为Chrome配置文件目录，用于保存浏览器的历史记录、Cookie和登录状态。如果需要使用新的配置文件，可以删除该目录或指定其他目录。

### API密钥配置
在`main.py`文件中配置DeepSeek API密钥：

```python
api_key = 'your_deepseek_api_key_here'
```

## 注意事项

1. **MOU书平台限制**：MOU书平台可能会限制自动化操作，建议合理控制发布频率，避免账号被封。

2. **浏览器版本兼容**：确保Chrome浏览器版本与ChromeDriver版本兼容，否则可能导致自动化操作失败。

3. **API密钥安全**：请妥善保管DeepSeek API密钥，避免泄露。

4. **网络连接**：确保网络连接稳定，API调用和浏览器操作都需要网络支持。

5. **Excel文件格式**：请确保Excel文件格式正确，标题列不能为空。

6. **内容审核**：生成的内容可能需要人工审核，确保符合MOU书平台的内容规范。

7. **图片上传**：如果需要上传图片，请确保图片路径正确，且图片格式符合MOU书要求。

## 常见问题

### 1. 登录失败
- 检查手机号和密码是否正确
- 检查网络连接是否正常
- 检查是否需要验证码登录
- 尝试手动登录一次，确保账号状态正常

### 2. 内容生成失败
- 检查DeepSeek API密钥是否正确
- 检查网络连接是否正常
- 检查标题是否包含特殊字符

### 3. 发布失败
- 检查MOU书平台是否有发布限制
- 检查浏览器是否已登录MOU书账号
- 检查发布内容是否符合MOU书平台规范
- 检查图片格式是否符合要求

### 4. 浏览器启动失败
- 检查ChromeDriver是否与Chrome浏览器版本兼容
- 检查Chrome浏览器是否已正确安装
- 检查是否有其他Chrome进程正在运行

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 贡献

欢迎提交Issue和Pull Request，共同完善该项目。

## 更新日志

### v1.0.0 (2025-11-25)
- 初始版本发布
- 实现Excel内容生成功能
- 实现MOU书自动发布功能
- 支持浏览器复用
- 支持非BMP字符过滤

## 联系方式

如有问题或建议，请通过以下方式联系：
- 项目地址：https://github.com/Vinton211/moushu-automation
- 邮箱：

---

**注意**：本项目仅供学习和研究使用，请勿用于违反MOU书平台规则的行为。使用本项目产生的一切后果由使用者自行承担。
