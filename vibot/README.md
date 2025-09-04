# VIBOT - AI Code Assistant

> **Your AI Code Assistant Specifically designed for Vibe-Coding**

VIBOT 是一个专为代码质量分析和改进而设计的AI驱动的命令行工具。它提供了多种代码分析功能，帮助开发者识别和解决代码中的各种问题。

## 🚀 快速开始

```bash
# 安装依赖
pip install openai

# 设置环境变量（AI功能需要）
export VIBOT_API_KEY='your-api-key'
export VIBOT_API_PROXY='https://api.deepseek.com'
export VIBOT_API_MODEL='deepseek-v3'  # 可选

# 基本使用
vibot --help
```

## 📋 命令总览

| 命令 | 功能 | 类型 | 说明 |
|------|------|------|------|
| `-d/--detect` | 文件检测 | 静态分析 | 分析目录结构和文件分布 |
| `-s/--search` | 关键词搜索 | 静态分析 | 在代码中搜索特定关键词 |
| `-p/--prolix` | 冗长文件检测 | 静态分析 | 查找行数过多的文件 |
| `-u/--ustalony` | 敏感信息检测 | AI分析 | 检测硬编码的密钥和敏感信息 |
| `-f/--function` | 函数质量分析 | AI分析 | 分析函数长度和参数复杂度 |
| `-r/--readability` | 可读性分析 | AI分析 | 检测影响代码可读性的问题 |
| `-o/--overlap` | 重复代码检测 | AI分析 | 检测违反DRY原则的重复代码 |
| `-n/--name` | 命名规范检测 | AI分析 | 检测命名相关问题和规范违反 |
| `-l/--logo` | 显示Logo | 工具 | 显示VIBOT字符画Logo |
| `-v/--version` | 版本信息 | 工具 | 显示版本号 |

## 🔍 详细命令说明

### 1. 文件检测 (`-d/--detect`)

**功能**：分析目录结构，统计文件类型分布，生成文件树视图

**检测问题**：
- 项目结构是否合理
- 文件类型分布情况
- 目录层级深度
- 文件数量统计

**使用方法**：
```bash
vibot -d --path ./src                    # 检测src目录
vibot -d                                 # 检测当前目录
```

**输出信息**：
- 彩色文件树结构
- 按文件扩展名统计
- 总文件数和目录数
- 文件大小分布

---

### 2. 关键词搜索 (`-s/--search`)

**功能**：在代码文件中搜索指定关键词，显示匹配位置和上下文

**检测问题**：
- 查找特定函数或变量的使用
- 定位TODO、FIXME等标记
- 搜索特定的API调用
- 查找代码注释中的关键信息

**使用方法**：
```bash
vibot -s --key "function" --path ./src   # 搜索"function"关键词
vibot -s --key "TODO"                    # 搜索TODO标记
vibot -s --key "password" --path ./      # 搜索可能的密码相关代码
```

**输出信息**：
- 匹配文件路径
- 行号和匹配内容
- 上下文代码片段
- 匹配总数统计

---

### 3. 冗长文件检测 (`-p/--prolix`)

**功能**：查找行数超过指定阈值的文件，识别可能需要重构的大文件

**检测问题**：
- 文件过长，难以维护
- 单一职责原则违反
- 需要拆分的模块
- 代码组织结构问题

**使用方法**：
```bash
vibot -p --path ./src                    # 使用默认阈值200行
vibot -p --max 150 --path ./src          # 自定义阈值150行
vibot -p --max 500                       # 查找超过500行的文件
```

**配置参数**：
- `--max`: 行数阈值（默认：200）

**输出信息**：
- 超长文件列表
- 每个文件的确切行数
- 按行数排序显示
- 重构建议

---

### 4. 敏感信息检测 (`-u/--ustalony`) 🤖 AI驱动

**功能**：使用AI检测代码中硬编码的密钥、密码和其他敏感信息

**检测问题**：
- 硬编码的API密钥
- 数据库连接字符串
- 密码和令牌
- 私钥和证书
- 敏感的URL和端点
- 个人身份信息(PII)

**使用方法**：
```bash
vibot -u --path ./src                    # 检测src目录
vibot -u                                 # 检测当前目录
```

**AI检测类型**：
- **API Keys**: AWS、Google、GitHub等API密钥
- **Database**: 数据库连接字符串和凭据
- **Passwords**: 硬编码密码
- **Tokens**: JWT、OAuth令牌
- **Certificates**: SSL证书和私钥
- **Personal Info**: 邮箱、电话等个人信息

**输出信息**：
- 敏感信息类型和位置
- 风险等级评估
- 具体的代码片段
- 安全修复建议
- AI Token使用统计

---

### 5. 函数质量分析 (`-f/--function`) 🤖 AI驱动

**功能**：使用AI分析函数的长度和参数复杂度，识别需要重构的函数

**检测问题**：
- 函数过长（违反单一职责原则）
- 参数过多（接口复杂）
- 函数职责不清晰
- 代码可维护性问题
- 函数设计缺陷

**使用方法**：
```bash
vibot -f --path ./src                    # 使用默认阈值
vibot -f --max-lines 30 --path ./src     # 自定义函数长度阈值
vibot -f --max-params 3 --path ./src     # 自定义参数数量阈值
```

**配置参数**：
- `--max-lines`: 函数最大行数阈值（默认：50）
- `--max-params`: 函数最大参数数量阈值（默认：5）

**AI分析内容**：
- 函数长度合理性
- 参数数量适当性
- 函数职责单一性
- 代码复杂度评估
- 重构建议

**输出信息**：
- 问题函数列表
- 具体问题描述
- 重构建议
- 代码质量评分
- AI Token使用统计

---

### 6. 可读性分析 (`-r/--readability`) 🤖 AI驱动

**功能**：使用AI分析代码可读性，检测影响代码理解的各种问题

**检测问题**：
- 行长度过长
- 复杂的三元运算符
- 魔法数字和字符串
- 无意义的注释
- 变量命名问题
- 代码格式问题

**使用方法**：
```bash
vibot -r --path ./src                    # 使用默认行长度80
vibot -r --max-line-length 120 --path ./src  # 自定义行长度阈值
```

**配置参数**：
- `--max-line-length`: 最大行长度阈值（默认：80）

**AI检测类型**：
- **Long Lines**: 超长代码行
- **Complex Ternary**: 复杂的三元运算符
- **Magic Numbers**: 魔法数字
- **Magic Strings**: 魔法字符串
- **Meaningless Comments**: 无意义注释
- **Poor Naming**: 变量命名问题
- **Formatting Issues**: 格式问题

**输出信息**：
- 可读性问题分类
- 具体问题位置和代码
- 改进建议
- 最佳实践推荐
- AI Token使用统计

---

### 7. 重复代码检测 (`-o/--overlap`) 🤖 AI驱动

**功能**：使用AI检测代码中的重复和重叠逻辑，识别违反DRY原则的代码段

**检测问题**：
- 完全相同的代码块
- 逻辑相似的不同实现
- 重复的代码模式
- 可以抽象化的相似结构
- 复制粘贴后的小幅修改

**使用方法**：
```bash
vibot -o --path ./src                    # 使用默认最小重复行数3
vibot -o --min-duplicate-lines 5 --path ./src  # 自定义最小重复行数
```

**配置参数**：
- `--min-duplicate-lines`: 最小重复行数阈值（默认：3）

**AI检测类型**：
- **Exact Duplicate**: 完全相同或几乎相同的代码块
- **Similar Logic**: 不同实现但相同逻辑目的的代码
- **Repeated Pattern**: 可以抽象化的相似代码结构

**严重程度分级**：
- **High**: 大块相同代码（>10行）
- **Medium**: 相似逻辑块（5-10行）
- **Low**: 小的重复模式（>=3行）

**输出信息**：
- 重复代码组详情
- 每个重复的具体位置
- 代码片段对比
- 重构建议
- 统计信息和AI Token使用

---

### 8. 命名规范检测 (`-n/--name`) 🤖 AI驱动

**功能**：使用AI检测代码中的命名相关问题，识别不符合命名规范的代码

**检测问题**：
- 过分简化的变量名（如`a, b, c`作为非循环变量）
- 晦涩的缩写（如`calcTotPrc`代替`calculateTotalPrice`）
- 不一致的命名风格（混用`snake_case`和`camelCase`）
- 无意义的命名（如`data`, `temp`, `foo`作为变量名）
- 常量命名规范违反（如`max_retries`而非`MAX_RETRIES`）
- 类名和函数名不符合规范
- 变量作用域与命名不匹配

**使用方法**：
```bash
vibot -n --path ./src                    # 检测src目录
vibot -n                                 # 检测当前目录
```

**AI检测类型**：
- **Oversimplified Names**: 过分简化的变量名
- **Obscure Abbreviations**: 晦涩难懂的缩写
- **Inconsistent Style**: 不一致的命名风格
- **Meaningless Names**: 无意义的命名
- **Constant Naming**: 常量命名规范问题
- **Poor Class Names**: 不合适的类名
- **Function Naming**: 函数命名问题
- **Variable Scope**: 变量作用域命名问题

**严重程度分级**：
- **High**: 严重影响代码可读性和可维护性的命名问题
- **Medium**: 可能造成混淆的中等命名问题
- **Low**: 轻微的命名不一致或风格问题

**输出信息**：
- 命名问题分类和位置
- 当前问题命名和建议改进
- 具体的代码上下文
- 命名最佳实践建议
- AI Token使用统计

---

### 9. 显示Logo (`-l/--logo`)

**功能**：显示VIBOT的ASCII艺术Logo

**使用方法**：
```bash
vibot -l                                 # 显示Logo
```

---

### 10. 版本信息 (`-v/--version`)

**功能**：显示VIBOT的版本信息

**使用方法**：
```bash
vibot -v                                 # 显示版本
vibot --version                          # 显示版本
```

## 🛠️ 通用参数

### 路径参数
- `--path PATH`: 指定要分析的目录路径（默认：当前目录）

### 搜索参数
- `--key KEY`: 搜索关键词（`-s/--search`命令必需）

### 阈值参数
- `--max MAX`: 冗长文件的最大行数阈值（默认：200）
- `--max-lines MAX_LINES`: 函数最大行数阈值（默认：50）
- `--max-params MAX_PARAMS`: 函数最大参数数量阈值（默认：5）
- `--max-line-length MAX_LINE_LENGTH`: 最大行长度阈值（默认：80）
- `--min-duplicate-lines MIN_DUPLICATE_LINES`: 重复检测最小行数阈值（默认：3）

## 🤖 AI功能配置

AI驱动的功能（`-u`, `-f`, `-r`, `-o`）需要配置API访问：

```bash
# 必需的环境变量
export VIBOT_API_KEY='your-api-key'
export VIBOT_API_PROXY='https://api.deepseek.com'

# 可选的环境变量
export VIBOT_API_MODEL='deepseek-v3'    # 默认模型
```

### 支持的文件类型
AI分析支持以下编程语言：
- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- Java (.java)
- C++ (.cpp)
- C (.c)
- C# (.cs)
- PHP (.php)
- Ruby (.rb)
- Go (.go)
- Kotlin (.kt)
- Swift (.swift)
- Rust (.rs)

## 📁 项目结构

```
vibot/
├── __init__.py              # 包初始化文件
├── cli.py                  # 主命令行入口
├── utils.py                # 公共工具函数和颜色定义
├── commands/               # 命令实现模块
│   ├── __init__.py         # 命令包初始化
│   ├── detect.py           # -d/--detect 文件检测
│   ├── search.py           # -s/--search 关键词搜索
│   ├── prolix.py           # -p/--prolix 冗长文件检测
│   ├── ustalony.py         # -u/--ustalony 敏感信息检测
│   ├── function.py         # -f/--function 函数质量分析
│   ├── readability.py      # -r/--readability 可读性分析
│   ├── overlap.py          # -o/--overlap 重复代码检测
│   └── naming.py           # -n/--name 命名规范检测
└── README.md               # 项目说明文档
```

## 💡 使用示例

### 基础代码分析工作流
```bash
# 1. 了解项目结构
vibot -d --path ./my-project

# 2. 查找冗长文件
vibot -p --max 200 --path ./my-project

# 3. 检测敏感信息
vibot -u --path ./my-project

# 4. 分析函数质量
vibot -f --path ./my-project

# 5. 检查代码可读性
vibot -r --path ./my-project

# 6. 检测重复代码
vibot -o --path ./my-project

# 7. 检查命名规范
vibot -n --path ./my-project
```

### 特定问题排查
```bash
# 查找所有TODO标记
vibot -s --key "TODO" --path ./src

# 查找可能的密码相关代码
vibot -s --key "password" --path ./

# 检测超过100行的函数
vibot -f --max-lines 100 --path ./src

# 检测超过120字符的长行
vibot -r --max-line-length 120 --path ./src

# 检查命名规范问题
vibot -n --path ./src
```

## 🎯 最佳实践

1. **定期运行全面检查**：建议在代码提交前运行所有AI分析命令
2. **设置合理阈值**：根据项目特点调整各种阈值参数
3. **关注高优先级问题**：优先解决AI标记为高风险的问题
4. **结合代码审查**：将VIBOT分析结果纳入代码审查流程
5. **持续改进**：定期使用VIBOT监控代码质量趋势

## 🔧 开发说明

### 模块化架构优势
1. **职责分离**：每个命令有独立的实现文件
2. **易于维护**：修改某个功能不影响其他功能
3. **可扩展性**：添加新命令只需创建新的模块文件
4. **代码复用**：公共函数统一管理
5. **测试友好**：每个模块可以独立测试

### 添加新命令
1. 在`commands/`目录创建新的模块文件
2. 在`commands/__init__.py`中导入新函数
3. 在`cli.py`中添加参数解析和调用逻辑
4. 更新README.md文档

## 📊 性能说明

- **静态分析命令**（`-d`, `-s`, `-p`）：快速执行，无需网络连接
- **AI分析命令**（`-u`, `-f`, `-r`, `-o`）：需要API调用，执行时间取决于网络和文件数量
- **Token消耗**：AI命令会显示Token使用统计和预估成本
- **文件过滤**：自动跳过二进制文件、图片等非代码文件，提高分析效率

---

**VIBOT** - 让代码质量分析变得简单而智能！ 🚀