#!/bin/bash

# 录屏并提取关键帧脚本

set -e

# 配置
INPUT_FILE="input.mp4"
OUTPUT_FILE="output.mp4"
KEYFRAME_PREFIX="keyframes"
KEYFRAME_INTERVAL=${KEYFRAME_INTERVAL:-10}
OUTPUT_DIR=${OUTPUT_DIR:-.}

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查工具是否安装
check_tools() {
    log_info "检查必要工具..."
    
    local missing_tools=()
    
    # 检查adb
    if ! command -v adb &> /dev/null; then
        log_warning "adb 未安装"
        missing_tools+=("adb")
    else
        log_success "adb 已安装: $(adb --version | head -1)"
    fi
    
    # 检查scrcpy
    if ! command -v scrcpy &> /dev/null; then
        log_error "scrcpy 未安装"
        missing_tools+=("scrcpy")
    else
        log_success "scrcpy 已安装: $(scrcpy --version | head -1)"
    fi
    
    # 检查ffmpeg
    if ! command -v ffmpeg &> /dev/null; then
        log_error "ffmpeg 未安装"
        missing_tools+=("ffmpeg")
    else
        log_success "ffmpeg 已安装: $(ffmpeg -version | head -1)"
    fi
    
    # 检查设备连接
    if [[ " ${missing_tools[@]} " =~ " adb " ]]; then
        log_warning "跳过设备检查（adb未安装）"
    else
        log_info "检查设备连接..."
        if adb devices | grep -q "device$"; then
            log_success "设备已连接"
            log_info "设备信息: $(adb shell getprop ro.product.model 2>/dev/null || echo '未知')"
        else
            log_warning "未检测到已连接的Android设备"
            log_info "请确保："
            log_info "1. USB调试已启用"
            log_info "2. 设备已通过USB连接"
            log_info "3. 在设备上授权调试"
        fi
    fi
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        log_error "缺少必要工具: ${missing_tools[*]}"
        log_info "安装建议："
        log_info "  macOS: brew install android-platform-tools scrcpy ffmpeg"
        log_info "  Ubuntu: sudo apt install adb scrcpy ffmpeg"
        return 1
    fi
    
    return 0
}

# 录屏
record_screen() {
    log_info "开始录屏..."
    log_info "按 Ctrl+C 停止录制"
    log_info "视频将保存为: $INPUT_FILE"
    
    # 创建输出目录
    mkdir -p "$OUTPUT_DIR"
    
    # 切换到输出目录
    cd "$OUTPUT_DIR"
    
    # 开始录屏
    scrcpy -t -r "$INPUT_FILE"
    
    if [ -f "$INPUT_FILE" ]; then
        local file_size=$(du -h "$INPUT_FILE" | cut -f1)
        log_success "录屏完成: $INPUT_FILE (大小: $file_size)"
    else
        log_error "录屏失败，文件未生成"
        return 1
    fi
}

# 动态计算关键帧间隔
calculate_keyint() {
    local input_file="$1"
    
    # 获取视频信息
    local duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$input_file" 2>/dev/null || echo "0")
    local fps=$(ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=1 "$input_file" 2>/dev/null | head -1 || echo "30")
    
    # 计算帧率（处理分数格式如 30000/1001）
    if [[ "$fps" == *"/"* ]]; then
        fps=$(echo "scale=2; $fps" | bc 2>/dev/null || echo "30")
    fi
    
    # 计算总帧数
    local total_frames=$(echo "$duration * $fps" | bc 2>/dev/null | cut -d. -f1 || echo "0")
    
    log_info "视频信息: 时长=${duration}s, 帧率=${fps}, 总帧数≈${total_frames}"
    
    # 动态计算关键帧间隔
    if [ "$total_frames" -gt 0 ]; then
        # 目标：提取大约20-50个关键帧
        local target_frames=30
        local calculated_keyint=$((total_frames / target_frames))
        
        # 限制范围：最小5帧，最大50帧
        if [ "$calculated_keyint" -lt 5 ]; then
            calculated_keyint=5
        elif [ "$calculated_keyint" -gt 50 ]; then
            calculated_keyint=50
        fi
        
        log_info "动态计算关键帧间隔: $calculated_keyint (基于约$target_frames个关键帧的目标)"
        echo "$calculated_keyint"
    else
        log_warning "无法获取视频信息，使用默认间隔: $KEYFRAME_INTERVAL"
        echo "$KEYFRAME_INTERVAL"
    fi
}

# 处理视频并提取关键帧
extract_keyframes() {
    local input_file="$INPUT_FILE"
    local output_file="$OUTPUT_FILE"
    
    if [ ! -f "$input_file" ]; then
        log_error "输入文件不存在: $input_file"
        log_info "请先运行录屏功能"
        return 1
    fi
    
    log_info "处理视频文件: $input_file"
    
    # 动态计算关键帧间隔
    local keyint=$(calculate_keyint "$input_file")
    log_info "使用关键帧间隔: keyint=$keyint"
    
    # 重新编码视频，设置关键帧间隔
    log_info "重新编码视频并设置关键帧间隔..."
    ffmpeg -i "$input_file" -c:v libx264 -x264opts "keyint=$keyint" -preset fast -crf 23 "$output_file" 2>/dev/null
    
    if [ ! -f "$output_file" ]; then
        log_error "视频处理失败"
        return 1
    fi
    
    local input_size=$(du -h "$input_file" | cut -f1)
    local output_size=$(du -h "$output_file" | cut -f1)
    log_success "视频处理完成: $output_file (输入: $input_size, 输出: $output_size)"
    
    # 提取关键帧
    log_info "提取关键帧..."
    ffmpeg -i "$output_file" -vf "select=eq(pict_type\,I)" -vsync vfr "${KEYFRAME_PREFIX}_%03d.png" 2>/dev/null
    
    local frame_count=$(ls -1 "${KEYFRAME_PREFIX}"_*.png 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$frame_count" -gt 0 ]; then
        log_success "提取了 $frame_count 个关键帧"
        
        # 显示前几个帧的文件信息
        log_info "关键帧文件:"
        ls -la "${KEYFRAME_PREFIX}"_*.png | head -5
        if [ "$frame_count" -gt 5 ]; then
            log_info "... 还有 $((frame_count - 5)) 个文件"
        fi
    else
        log_warning "未提取到关键帧"
        log_info "可能的原因："
        log_info "1. 视频太短"
        log_info "2. 关键帧间隔设置过大"
        log_info "3. 视频编码问题"
    fi
}

# 列出关键帧
list_frames() {
    local frame_count=$(ls -1 "${KEYFRAME_PREFIX}"_*.png 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$frame_count" -gt 0 ]; then
        log_success "找到 $frame_count 个关键帧文件:"
        ls -la "${KEYFRAME_PREFIX}"_*.png
    else
        log_warning "未找到关键帧文件"
        log_info "请先运行提取关键帧功能"
    fi
}

# 完整流程
full_process() {
    log_info "开始完整录屏提取流程..."
    
    # 检查工具
    check_tools || return 1
    
    # 录屏
    record_screen || return 1
    
    # 提取关键帧
    extract_keyframes || return 1
    
    # 列出帧
    list_frames
    
    log_success "流程完成！"
}

# 显示帮助
show_help() {
    echo "录屏并提取关键帧工具"
    echo ""
    echo "使用方法: $0 <命令>"
    echo ""
    echo "命令:"
    echo "  check-tools    检查必要工具是否安装"
    echo "  record         开始录屏（按Ctrl+C停止）"
    echo "  extract-frames 处理视频并提取关键帧"
    echo "  list-frames    列出提取的关键帧"
    echo "  full-process   完整流程：检查工具 → 录屏 → 提取关键帧 → 列出帧"
    echo "  help           显示此帮助信息"
    echo ""
    echo "环境变量:"
    echo "  KEYFRAME_INTERVAL  关键帧间隔（默认: 10）"
    echo "  OUTPUT_DIR         输出目录（默认: 当前目录）"
    echo ""
    echo "示例:"
    echo "  $0 check-tools"
    echo "  KEYFRAME_INTERVAL=20 $0 full-process"
    echo "  OUTPUT_DIR=./my_recordings $0 full-process"
}

# 主函数
main() {
    local command="${1:-help}"
    
    case "$command" in
        check-tools)
            check_tools
            ;;
        record)
            record_screen
            ;;
        extract-frames)
            extract_keyframes
            ;;
        list-frames)
            list_frames
            ;;
        full-process)
            full_process
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "未知命令: $command"
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"