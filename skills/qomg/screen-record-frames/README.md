# 录屏并提取关键帧 Skill

这个skill用于录制Android设备屏幕并提取关键帧，特别适合需要分析屏幕操作或创建教程的场景。

## 功能特点

1. **智能工具检查**：自动检查adb、scrcpy、ffmpeg是否安装
2. **动态关键帧计算**：根据视频长度自动计算合适的关键帧间隔，避免提取过多帧
3. **完整工作流**：从录屏到关键帧提取的一站式解决方案
4. **灵活配置**：支持自定义关键帧间隔和输出目录

## 快速开始

### 1. 安装依赖
```bash
# macOS
brew install android-platform-tools scrcpy ffmpeg

# Ubuntu/Debian
sudo apt install adb scrcpy ffmpeg
```

### 2. 启用Android设备调试
1. 在Android设备上启用"开发者选项"
2. 启用"USB调试"
3. 通过USB连接电脑
4. 在设备上授权调试连接

### 3. 使用skill
```bash
# 检查工具
openclaw skill screen-record-frames check-tools

# 完整流程（推荐）
openclaw skill screen-record-frames full-process
```

## 详细使用

### 分步执行
```bash
# 1. 检查工具和设备
openclaw skill screen-record-frames check-tools

# 2. 开始录屏（按Ctrl+C停止）
openclaw skill screen-record-frames record

# 3. 提取关键帧
openclaw skill screen-record-frames extract-frames

# 4. 查看结果
openclaw skill screen-record-frames list-frames
```

### 自定义配置
```bash
# 设置关键帧间隔（默认10）
export KEYFRAME_INTERVAL=20
openclaw skill screen-record-frames full-process

# 设置输出目录
export OUTPUT_DIR=./my_recordings
openclaw skill screen-record-frames full-process
```

## 输出文件

流程完成后会生成以下文件：
- `input.mp4` - 原始录屏文件
- `output.mp4` - 处理后的视频文件（带关键帧标记）
- `keyframes_001.png` - 提取的关键帧图片
- `keyframes_002.png` - 第二个关键帧
- ...（依此类推）

## 动态关键帧计算

skill会自动分析视频信息并计算合适的关键帧间隔：
- 视频较短 → 较小的间隔（更多关键帧）
- 视频较长 → 较大的间隔（较少关键帧）
- 目标：提取约20-50个关键帧，避免过多或过少

## 故障排除

### 常见问题

1. **adb设备未找到**
   - 检查USB连接
   - 确认调试模式已启用
   - 在设备上授权调试

2. **scrcpy无法启动**
   - 确保设备屏幕已解锁
   - 尝试重新连接USB

3. **无关键帧提取**
   - 视频可能太短
   - 尝试减小KEYFRAME_INTERVAL值
   - 检查视频编码格式

4. **工具未安装**
   - 按照"安装依赖"部分安装必要工具

### 调试模式
```bash
# 查看详细输出
bash -x screen-record-frames/scripts/main.sh check-tools
```

## 技术细节

### 使用的工具
- **adb**: Android设备通信
- **scrcpy**: 高性能屏幕录制和镜像
- **ffmpeg**: 视频处理和关键帧提取

### 关键帧算法
1. 分析视频时长和帧率
2. 计算总帧数
3. 根据目标关键帧数量（20-50）计算间隔
4. 应用限制：最小5帧，最大50帧间隔

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个skill。