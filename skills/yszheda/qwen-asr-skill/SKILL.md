# Qwen 方言语音识别 Skill

基于通义千问 Qwen3-ASR-0.6B 模型的语音转文字服务，支持 22 种中文方言和 30 种语言识别。

## 功能特性

- 🎤 支持 22 种中文方言识别
- 🌐 支持 30 种国际语言
- 💻 CPU 端运行，无需 GPU
- 🔍 自动语言检测
- ⚡ 低延迟，高准确率

## 安装

在 OpenClaw 中搜索「Qwen 方言语音识别」，点击一键安装即可。

### 手动安装

```bash
# 克隆项目
git clone <repository-url>
cd qwen-asr-skill

# 安装依赖
npm install
pip install -r requirements.txt

# 启动服务
npm start
```

### 环境变量配置

```bash
cp .env.example .env
# 编辑 .env 文件，根据需要调整配置
```

## 🔧 使用方式

安装并启用后，直接在 OpenClaw 中发送语音消息即可，系统会自动：
1. 接收语音输入
2. 调用本 Skill 进行语音转文字
3. 将识别后的文字传给大模型
4. 返回语音回答给用户

你可以直接说方言，系统会自动识别，无需手动切换语言。

## 📡 API 接口

### POST /transcribe

音频转文字接口

**请求参数：**
- `audio`：音频文件或 base64 编码的音频数据（必需）
- `language`：指定语言/方言（可选，如："四川话"、"粤语"等）
- `timestamps`：是否返回时间戳（可选，默认 false）

**响应示例：**
```json
{
  "success": true,
  "data": {
    "text": "识别结果文本",
    "language": "Sichuan",
    "confidence": 0.98,
    "duration": 1.23
  }
}
```

## 📊 性能指标

- 推理速度：实时音频的 1.5-2 倍速（8 核 CPU）
- 内存占用：6-8GB 运行时
- 支持音频时长：最长 5 分钟
- 方言识别 WER：<16%（平均）

## 🔒 隐私保护

- 所有语音处理在本地完成
- 模型权重在首次运行时自动从 Hugging Face 下载（约 6GB）
- 处理完的音频文件会自动删除，不会存储
- 不收集任何用户语音数据和识别内容

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个 Skill！

## 📄 许可证

Apache-2.0