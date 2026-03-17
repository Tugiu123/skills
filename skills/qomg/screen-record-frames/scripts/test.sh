#!/bin/bash

# 录屏关键帧skill测试脚本

set -e

echo "测试录屏并提取关键帧skill..."

# 测试工具检查
echo "1. 测试工具检查..."
./scripts/main.sh check-tools

if [ $? -eq 0 ]; then
    echo "✅ 工具检查通过"
else
    echo "❌ 工具检查失败"
    echo "请安装缺少的工具后重试"
    exit 1
fi

# 测试帮助功能
echo ""
echo "2. 测试帮助功能..."
./scripts/main.sh help

# 测试列表功能（应该显示无文件）
echo ""
echo "3. 测试关键帧列表功能（应显示无文件）..."
./scripts/main.sh list-frames

# 测试动态关键帧计算
echo ""
echo "4. 测试动态关键帧计算..."
echo "创建一个测试视频..."
# 使用ffmpeg创建一个简单的测试视频
ffmpeg -f lavfi -i testsrc=duration=5:size=640x480:rate=30 \
    -c:v libx264 -preset ultrafast test_input.mp4 2>/dev/null || {
    echo "❌ 创建测试视频失败"
    exit 1
}

echo "✅ 测试视频创建成功: test_input.mp4"

# 测试关键帧提取
echo ""
echo "5. 测试关键帧提取..."
export INPUT_FILE="test_input.mp4"
export KEYFRAME_INTERVAL=15
./scripts/main.sh extract-frames

if [ $? -eq 0 ]; then
    echo "✅ 关键帧提取测试通过"
    
    # 检查是否生成了关键帧
    frame_count=$(ls -1 keyframes_*.png 2>/dev/null | wc -l | tr -d ' ')
    if [ "$frame_count" -gt 0 ]; then
        echo "✅ 生成了 $frame_count 个关键帧"
        ls -la keyframes_*.png | head -3
    else
        echo "⚠️  未生成关键帧，但流程未报错"
    fi
else
    echo "❌ 关键帧提取测试失败"
fi

# 清理测试文件
echo ""
echo "6. 清理测试文件..."
rm -f test_input.mp4 output.mp4 keyframes_*.png 2>/dev/null || true
echo "✅ 测试文件已清理"

echo ""
echo "========================================"
echo "测试完成！"
echo ""
echo "下一步："
echo "1. 连接Android设备并启用USB调试"
echo "2. 运行完整流程: ./scripts/main.sh full-process"
echo "3. 或使用openclaw命令: openclaw skill screen-record-frames full-process"
echo ""
echo "注意：录屏功能需要真实的Android设备连接"