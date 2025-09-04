#!/usr/bin/env python3
"""测试文件 - 包含一些硬编码敏感信息示例"""

# 这些是故意的硬编码敏感信息，用于测试检测功能
API_KEY = "sk-1234567890abcdef1234567890abcdef"
password = "mySecretPassword123"
database_url = "postgresql://user:pass@localhost:5432/mydb"
auth_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
secret_key = "super_secret_key_12345"

# 配置信息
config = {
    "api_key": "ak-9876543210fedcba9876543210fedcba",
    "endpoint": "https://api.example.com/v1",
    "token": "bearer_token_abcdef123456789"
}

class DatabaseConfig:
    def __init__(self):
        self.host = "https://db.example.com"
        self.password = "anotherPassword456"
        self.connection_string = "mongodb://admin:secret@cluster.example.com:27017"

# 这是正常的代码，不应该被检测
def get_user_input():
    user_password = input("Enter your password: ")
    return user_password

# 注释中的敏感信息应该被忽略
# password = "this_should_be_ignored"