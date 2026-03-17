#!/bin/bash

# 录屏关键帧skill安装脚本

set -e

echo "安装录屏并提取关键帧skill..."

# 检查操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
else
    echo "不支持的操作系统: $OSTYPE"
    exit 1
fi

echo "检测到操作系统: $OS"

# 安装依赖
install_dependencies() {
    echo "安装必要依赖..."
    
    if [ "$OS" = "macos" ]; then
        # 检查Homebrew
        if ! command -v brew &> /dev/null; then
            echo "错误: Homebrew未安装"
            echo "请先安装Homebrew: https://brew.sh/"
            exit 1
        fi
        
        # 安装工具
        echo "通过Homebrew安装工具..."
        brew install android-platform-tools scrcpy ffmpeg
        
    elif [ "$OS" = "linux" ]; then
        # 检查apt
        if ! command -v apt &> /dev/null; then
            echo "错误: apt未找到，请使用其他包管理器"
            exit 1
        fi
        
        # 安装工具
        echo "通过apt安装工具..."
        sudo apt update
        sudo apt install -y adb scrcpy ffmpeg
    fi
    
    echo "依赖安装完成"
}

# 检查工具
check_tools() {
    echo "检查工具安装情况..."
    
    local missing=()
    
    for tool in adb scrcpy ffmpeg; do
        if ! command -v "$tool" &> /dev/null; then
            missing+=("$tool")
            echo "  ❌ $tool 未安装"
        else
            echo "  ✅ $tool 已安装"
        fi
    done
    
    if [ ${#missing[@]} -gt 0 ]; then
        echo "以下工具未安装: ${missing[*]}"
        read -p "是否立即安装？(y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            install_dependencies
        else
            echo "请手动安装缺少的工具后重试"
            exit 1
        fi
    else
        echo "所有必要工具已安装"
    fi
}

# 配置adb
setup_adb() {
    echo "配置adb..."
    
    # 创建adb规则文件（Linux）
    if [ "$OS" = "linux" ]; then
        echo "设置USB设备权限..."
        sudo groupadd plugdev 2>/dev/null || true
        sudo usermod -aG plugdev $USER
        
        # 创建udev规则
        RULES_FILE="/etc/udev/rules.d/51-android.rules"
        if [ ! -f "$RULES_FILE" ]; then
            echo "创建udev规则..."
            sudo tee "$RULES_FILE" > /dev/null << 'EOF'
# Android devices
SUBSYSTEM=="usb", ATTR{idVendor}=="0bb4", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0e79", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0502", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0b05", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="413c", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0489", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="091e", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="18d1", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0fce", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="19d2", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="1bbb", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="04e8", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="04dd", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="054c", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0fca", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="2340", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="0930", MODE="0666", GROUP="plugdev"
SUBSYSTEM=="usb", ATTR{idVendor}=="22b8", MODE="0666", GROUP="plugdev"
EOF
            
            sudo udevadm control --reload-rules
            sudo udevadm trigger
            echo "udev规则已配置"
        fi
    fi
    
    echo "adb配置完成"
}

# 测试连接
test_connection() {
    echo "测试设备连接..."
    
    # 启动adb服务
    adb start-server
    
    # 检查设备
    echo "连接的设备:"
    adb devices
    
    if adb devices | grep -q "device$"; then
        echo "✅ 设备连接正常"
        echo "设备型号: $(adb shell getprop ro.product.model 2>/dev/null || echo '未知')"
    else
        echo "⚠️  未检测到设备"
        echo "请确保："
        echo "1. Android设备已通过USB连接"
        echo "2. USB调试已启用（设置 > 开发者选项 > USB调试）"
        echo "3. 在设备上授权调试连接"
        echo ""
        echo "连接后重新运行此脚本测试"
    fi
}

# 显示使用说明
show_usage() {
    echo ""
    echo "🎉 安装完成！"
    echo ""
    echo "使用方式:"
    echo "1. 确保Android设备已连接并启用调试"
    echo "2. 运行录屏skill:"
    echo "   openclaw skill screen-record-frames check-tools"
    echo "   openclaw skill screen-record-frames full-process"
    echo ""
    echo "更多信息请查看:"
    echo "  screen-record-frames/README.md"
    echo ""
}

# 主安装流程
main() {
    echo "========================================"
    echo "  录屏并提取关键帧 Skill 安装程序"
    echo "========================================"
    echo ""
    
    # 检查工具
    check_tools
    
    # 配置adb（Linux）
    if [ "$OS" = "linux" ]; then
        setup_adb
    fi
    
    # 测试连接
    test_connection
    
    # 显示使用说明
    show_usage
    
    echo "安装完成！"
}

# 运行主函数
main "$@"