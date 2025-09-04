#!/usr/bin/env python3
"""测试文件 - 用于验证AI安全检测功能"""

# 这些是故意的硬编码敏感信息，用于测试AI检测
DATABASE_PASSWORD = "mySecretPassword123"
API_KEY = "sk-1234567890abcdef1234567890abcdef"
JWT_SECRET = "super_secret_jwt_key_12345"

# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "user": "admin", 
    "password": "admin123",
    "database": "production_db"
}

# API配置
OPENAI_API_KEY = "sk-proj-abcdef1234567890"
STRIPE_SECRET_KEY = "sk_live_1234567890abcdef"

# 这是正常的代码，不应该被标记
def get_user_password():
    return input("Enter password: ")

# 注释中的密码应该被忽略
# password = "this_is_just_a_comment"