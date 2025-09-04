# VIBOT 命名规范检测功能总结

## ✅ 新增功能：`-n/--name` - 命名规范检测

### 🎯 功能描述
使用AI检测代码中的命名相关问题，识别不符合命名规范和最佳实践的代码，帮助提高代码可读性和可维护性。

### 🤖 AI 驱动分析
- **完全使用 AI API** 进行分析，无静态语法分析
- **智能识别**：理解代码上下文，区分合理命名和问题命名
- **上下文理解**：AI 能理解变量作用域和使用场景
- **多语言支持**：支持13种主流编程语言的命名规范

### 🔍 检测类型

#### 1. **Oversimplified Names** - 过分简化的变量名
- ❌ 单字母变量（非简单循环）：`a, b, c, x, y, z`
- ❌ 过短的无意义名称：`i, j, k` 在复杂上下文中
- ❌ 不传达含义的简化名称

**示例**：
```python
# 问题代码
def process_data(a, b, c):
    x = a + b
    y = c * 2
    return x / y

# 建议改进
def process_data(base_value, multiplier, divisor):
    sum_result = base_value + multiplier
    doubled_divisor = divisor * 2
    return sum_result / doubled_divisor
```

#### 2. **Obscure Abbreviations** - 晦涩的缩写
- ❌ 不清楚的缩写：`calcTotPrc` 代替 `calculateTotalPrice`
- ❌ 领域特定缩写无上下文
- ❌ 不一致的缩写模式

**示例**：
```python
# 问题代码
def calcTotPrc(qty, prc, disc):
    totPrc = qty * prc
    discAmt = totPrc * disc
    return totPrc - discAmt

# 建议改进
def calculate_total_price(quantity, price, discount_rate):
    total_price = quantity * price
    discount_amount = total_price * discount_rate
    return total_price - discount_amount
```

#### 3. **Inconsistent Style** - 不一致的命名风格
- ❌ 混用 `snake_case` 和 `camelCase`
- ❌ 不一致的大小写模式
- ❌ 相似实体使用不同命名约定

**示例**：
```python
# 问题代码
def calculate_user_score(user_data):
    totalScore = 0  # camelCase
    bonus_points = 10  # snake_case
    userLevel = user_data.get('level')  # camelCase
    return totalScore + bonus_points

# 建议改进
def calculate_user_score(user_data):
    total_score = 0  # 统一使用 snake_case
    bonus_points = 10
    user_level = user_data.get('level')
    return total_score + bonus_points
```

#### 4. **Meaningless Names** - 无意义的命名
- ❌ 通用名称：`data, temp, foo, bar, stuff, thing`
- ❌ 无描述性的类名：`myclass, handler, manager`（无上下文）
- ❌ 生产代码中的占位符名称

**示例**：
```python
# 问题代码
def process_stuff(data, temp, foo):
    result = []
    thing = data.copy()
    for item in thing:
        bar = temp * 2
        if foo:
            stuff = item + bar
            result.append(stuff)
    return result

# 建议改进
def process_user_scores(user_list, bonus_multiplier, apply_bonus):
    processed_scores = []
    user_data = user_list.copy()
    for user_score in user_data:
        bonus_amount = bonus_multiplier * 2
        if apply_bonus:
            final_score = user_score + bonus_amount
            processed_scores.append(final_score)
    return processed_scores
```

#### 5. **Constant Naming** - 常量命名规范
- ❌ 常量不使用 `UPPER_CASE`：`max_retries` 而非 `MAX_RETRIES`
- ❌ 魔法数字未使用命名常量
- ❌ 配置值命名不当

**示例**：
```python
# 问题代码
max_retries = 5
default_timeout = 30
api_base_url = "https://api.example.com"

# 建议改进
MAX_RETRIES = 5
DEFAULT_TIMEOUT_SECONDS = 30
API_BASE_URL = "https://api.example.com"
```

#### 6. **Poor Class Names** - 不合适的类名
- ❌ 非名词类名
- ❌ 过于通用的类名
- ❌ 不代表实体的类名

**示例**：
```python
# 问题代码
class myclass:
    pass

class handler:
    def process(self, stuff):
        return stuff

# 建议改进
class UserAccount:
    pass

class PaymentProcessor:
    def process_payment(self, payment_data):
        return payment_data
```

#### 7. **Function Naming** - 函数命名问题
- ❌ 动作函数使用非动词名称
- ❌ 函数目的不清楚
- ❌ 不一致的函数命名模式

**示例**：
```python
# 问题代码
def user_data(user_id):  # 应该是动词
    return {"id": user_id, "name": "John"}

def calculation(x, y):  # 不描述具体计算
    return x * y + (x / y)

# 建议改进
def fetch_user_data(user_id):
    return {"id": user_id, "name": "John"}

def calculate_weighted_average(value, weight):
    return value * weight + (value / weight)
```

#### 8. **Variable Scope** - 变量作用域命名问题
- ❌ 长生命周期变量使用短名称
- ❌ 短生命周期变量使用长名称
- ❌ 作用域与命名不匹配

### 📈 严重程度分级
- **High**: 严重影响代码可读性和可维护性的命名问题
- **Medium**: 可能造成混淆的中等命名问题  
- **Low**: 轻微的命名不一致或风格问题

### 🔧 使用方法
```bash
# 基本使用
vibot -n --path /path/to/code

# 需要设置环境变量
export VIBOT_API_KEY='your-api-key'
export VIBOT_API_PROXY='https://api.deepseek.com'
export VIBOT_API_MODEL='deepseek-v3'  # 可选
```

### 📋 输出格式
- 显示命名问题的详细信息
- 列出所有问题实例的位置和代码上下文
- 提供当前命名和建议改进
- 显示具体的重构建议
- 统计问题类型和严重程度分布
- 显示 AI Token 使用情况

### 💡 AI 命名最佳实践建议
1. **使用描述性和有意义的名称**
2. **遵循一致的命名约定**（snake_case 或 camelCase）
3. **常量使用 UPPER_CASE**
4. **避免缩写，除非是众所周知的**
5. **函数使用动词，变量和类使用名词**
6. **使名称可搜索和可发音**
7. **使用意图明确的名称**
8. **避免心理映射和误导性名称**

### 🚫 智能忽略
- 标准库名称和内置函数
- 第三方库约定
- 已确立的领域特定术语
- 非常短且明显的上下文中的单字母变量（如简单数学运算）

### 🎨 支持的文件类型
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

这个功能将帮助开发者建立和维护一致的命名规范，提高代码质量和团队协作效率！