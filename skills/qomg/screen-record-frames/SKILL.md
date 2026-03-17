# Skill: 录屏并提取关键帧

## 描述
这个skill用于通过scrcpy录制Android设备屏幕，然后使用ffmpeg提取关键帧。支持动态计算关键帧间隔，避免提取过多帧。

## 前置条件
- Android设备已通过USB连接并启用调试模式
- 已安装必要的工具：adb, scrcpy, ffmpeg

## 工具检查
运行前会自动检查以下工具是否安装：
- `adb` (Android Debug Bridge)
- `scrcpy` (屏幕录制工具)
- `ffmpeg` (视频处理工具)

## 主要功能

### 1. 录屏
使用scrcpy录制Android设备屏幕：
```bash
scrcpy -t -r input.mp4
```
- `-t`：显示触摸操作
- `-r`：录制到文件
- 按`Ctrl+C`停止录制并保存

### 2. 设置关键帧间隔
动态计算关键帧间隔，避免提取过多帧：
```bash
ffmpeg -i input.mp4 -c:v libx264 -x264opts keyint=10 output.mp4
```
- `keyint=10`：每10帧一个关键帧（可调整）

### 3. 提取关键帧
提取所有关键帧为PNG图片：
```bash
ffmpeg -i output.mp4 -vf "select=eq(pict_type\,I)" -vsync vfr keyframes_%03d.png
```

### 4. 列出提取的帧
显示所有提取的关键帧图片：
```bash
ls -la keyframes_*.png
```

## 使用方式

### 快速开始
```bash
# 1. 检查工具
openclaw skill screen-record-frames check-tools

# 2. 开始录屏（按Ctrl+C停止）
openclaw skill screen-record-frames record

# 3. 处理视频并提取关键帧
openclaw skill screen-record-frames extract-frames

# 4. 列出提取的帧
openclaw skill screen-record-frames list-frames
```

### 完整流程
```bash
# 一次性执行完整流程
openclaw skill screen-record-frames full-process
```

## 配置选项

### 关键帧间隔
可以通过环境变量设置关键帧间隔：
```bash
export KEYFRAME_INTERVAL=20  # 每20帧一个关键帧
openclaw skill screen-record-frames extract-frames
```

### 输出目录
```bash
export OUTPUT_DIR=./recordings
openclaw skill screen-record-frames full-process
```

## 注意事项
1. 确保Android设备已连接并启用USB调试
2. 录屏过程中按`Ctrl+C`停止录制
3. 关键帧数量取决于视频长度和间隔设置
4. 提取的帧会保存为`keyframes_001.png`格式

## 故障排除
- **adb设备未找到**：检查USB连接和调试模式
- **scrcpy无法启动**：确保设备屏幕已解锁
- **ffmpeg处理失败**：检查视频文件格式
- **无关键帧提取**：调整`keyint`值或检查视频编码