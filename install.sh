#!/bin/bash

# 创建可执行脚本
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.local/bin"

# 创建安装目录
mkdir -p "$INSTALL_DIR"

# 创建 vibot 可执行文件
cat > "$INSTALL_DIR/vibot" << EOF
#!/bin/bash
python3 "$SCRIPT_DIR/vibot/cli.py" "\$@"
EOF

# 使其可执行
chmod +x "$INSTALL_DIR/vibot"

echo "vibot 已安装到 $INSTALL_DIR/vibot"
echo "请确保 $INSTALL_DIR 在你的 PATH 中"
echo "你可以运行以下命令添加到 PATH："
echo "echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
echo "source ~/.bashrc"