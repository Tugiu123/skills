# OpenViking 安装配置向导

按以下步骤完成安装。每步执行后确认结果再继续。

## 第一步：检查前置条件

```bash
# 检查 Python 版本（需要 3.10+）
python3 --version

# 检查 pip
pip3 --version

# macOS 检查 cmake（编译 C++ 扩展需要）
which cmake || echo "需要安装 cmake"
# 安装 cmake（如果缺少）：brew install cmake
```

## 第二步：安装 OpenViking

```bash
pip install openviking --upgrade --force-reinstall
```

验证安装：
```bash
python3 -c "import openviking; print('安装成功 ✓')"
```

## 第三步：选择 Embedding 提供商并配置

根据用户已有的 API Key 选择方案：

### 方案 A：OpenAI（推荐，已有 OpenAI Key 的用户）

```bash
mkdir -p ~/.openviking
cat > ~/.openviking/ov.conf << 'EOF'
{
  "embedding": {
    "dense": {
      "provider": "openai",
      "api_base": "https://api.openai.com/v1",
      "api_key": "YOUR_OPENAI_API_KEY",
      "model": "text-embedding-3-large",
      "dimension": 3072
    }
  },
  "vlm": {
    "provider": "openai",
    "api_key": "YOUR_OPENAI_API_KEY",
    "model": "gpt-4o-mini"
  },
  "storage": {
    "workspace": "/Users/YOUR_USERNAME/.openviking/data",
    "agfs": { "backend": "local" },
    "vectordb": { "backend": "local" }
  }
}
EOF
```

⚠️ 替换 `YOUR_OPENAI_API_KEY` 和 `YOUR_USERNAME`。

### 方案 B：火山引擎/豆包（中国用户推荐，成本更低）

```bash
mkdir -p ~/.openviking
cat > ~/.openviking/ov.conf << 'EOF'
{
  "embedding": {
    "dense": {
      "provider": "volcengine",
      "api_base": "https://ark.cn-beijing.volces.com/api/v3",
      "api_key": "YOUR_ARK_API_KEY",
      "model": "doubao-embedding-vision-250615",
      "dimension": 1024,
      "input": "multimodal"
    }
  },
  "vlm": {
    "provider": "volcengine",
    "api_key": "YOUR_ARK_API_KEY",
    "api_base": "https://ark.cn-beijing.volces.com/api/v3",
    "model": "doubao-seed-2-0-pro-260215"
  },
  "storage": {
    "workspace": "/Users/YOUR_USERNAME/.openviking/data",
    "agfs": { "backend": "local" },
    "vectordb": { "backend": "local" }
  }
}
EOF
```

### 方案 C：Jina AI（免费额度最多）

```bash
# 在 https://jina.ai/ 注册获取免费 API Key
mkdir -p ~/.openviking
cat > ~/.openviking/ov.conf << 'EOF'
{
  "embedding": {
    "dense": {
      "provider": "jina",
      "api_key": "YOUR_JINA_API_KEY",
      "model": "jina-embeddings-v5-text-small",
      "dimension": 1024
    }
  },
  "storage": {
    "workspace": "/Users/YOUR_USERNAME/.openviking/data",
    "agfs": { "backend": "local" },
    "vectordb": { "backend": "local" }
  }
}
EOF
```

> 注意：Jina 方案没有 VLM，L0/L1 层将从内容直接生成（质量略低，但节省费用）。

## 第四步：安装 OpenClaw 插件（一键脚本）

```bash
curl -fsSL https://raw.githubusercontent.com/volcengine/OpenViking/main/examples/openclaw-memory-plugin/install.sh | bash
```

或手动安装：
```bash
git clone https://github.com/volcengine/OpenViking.git /tmp/OpenViking
cd /tmp/OpenViking
npx ./examples/openclaw-memory-plugin/setup-helper
```

## 第五步：配置 OpenClaw 使用 OpenViking 插件

```bash
openclaw config set plugins.slots.memory memory-openviking
openclaw config set plugins.entries.memory-openviking.config.mode "local"
openclaw config set plugins.entries.memory-openviking.config.configPath "~/.openviking/ov.conf"
openclaw config set plugins.entries.memory-openviking.config.autoCapture true --json
openclaw config set plugins.entries.memory-openviking.config.autoRecall true --json
```

## 第六步：重启 Gateway 并验证

```bash
# 重启
openclaw daemon restart

# 验证插件已加载
openclaw status
```

应看到 `memory: memory-openviking` 出现在输出中。

## 常见问题

**Q: cmake 找不到？**
```bash
brew install cmake  # macOS
sudo apt install cmake  # Ubuntu
```

**Q: 端口 1933 被占用？**
```bash
lsof -ti tcp:1933 | xargs kill -9
```

**Q: 插件显示 disabled？**
```bash
openclaw config set plugins.enabled true --json
openclaw daemon restart
```
