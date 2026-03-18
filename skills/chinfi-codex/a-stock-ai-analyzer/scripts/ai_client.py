#!/usr/bin/env python3
"""
AI 客户端模块 - 支持多种模型环境
适用于 OpenClaw 等各种模型环境
"""

import os
import sys
import json
from typing import Optional

# OpenClaw 兼容的 AI 调用方式
def call_ai(prompt: str, timeout: int = 120) -> str:
    """
    调用 AI 进行分析
    支持多种模型环境配置
    
    优先级：
    1. OPENCLAW_MODEL_ENDPOINT - OpenClaw 模型端点
    2. OPENAI_API_KEY - OpenAI 兼容接口
    3. 直接返回提示（让 OpenClaw 自行处理）
    """
    
    # 方式1：使用 OpenClaw 环境变量配置的模型端点
    model_endpoint = os.environ.get("OPENCLAW_MODEL_ENDPOINT", "").strip()
    if model_endpoint:
        return _call_via_http(prompt, model_endpoint, timeout)
    
    # 方式2：使用 OpenAI 兼容接口
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
    openai_base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").strip()
    if openai_key:
        return _call_openai_compatible(prompt, openai_base, openai_key, timeout)
    
    # 方式3：使用其他兼容 OpenAI 格式的 API
    api_key = os.environ.get("LLM_API_KEY", "").strip()
    api_base = os.environ.get("LLM_API_BASE", "").strip()
    if api_key and api_base:
        return _call_openai_compatible(prompt, api_base, api_key, timeout)
    
    # 方式4：OpenClaw 环境 - 返回结构化数据供上层处理
    # 在 OpenClaw 环境中，可以直接输出 prompt，由 OpenClaw 捕获并处理
    if os.environ.get("OPENCLAW_SESSION", "").strip():
        return _format_for_openclaw(prompt)
    
    # 方式5：无可用模型 - 返回提示信息
    return _format_no_model_response(prompt)


def _call_via_http(prompt: str, endpoint: str, timeout: int) -> str:
    """通过 HTTP 调用模型端点"""
    try:
        import urllib.request
        import urllib.error
        
        data = json.dumps({
            "prompt": prompt,
            "max_tokens": 2000,
            "temperature": 0.7
        }).encode('utf-8')
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'stock-ai-analyzer/2.0'
        }
        
        req = urllib.request.Request(
            endpoint,
            data=data,
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            result = json.loads(response.read().decode('utf-8'))
            # 兼容不同响应格式
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0].get('text', result['choices'][0].get('message', {}).get('content', ''))
            elif 'response' in result:
                return result['response']
            elif 'content' in result:
                return result['content']
            else:
                return str(result)
                
    except Exception as e:
        return f"[模型调用失败: {str(e)}]\n\n原始分析内容：\n{prompt[:500]}..."


def _call_openai_compatible(prompt: str, base_url: str, api_key: str, timeout: int) -> str:
    """调用 OpenAI 兼容接口"""
    try:
        import urllib.request
        import urllib.error
        
        # 确保 base_url 以 /v1 结尾
        if not base_url.endswith('/v1'):
            base_url = base_url.rstrip('/') + '/v1'
        
        endpoint = f"{base_url}/chat/completions"
        
        data = json.dumps({
            "model": os.environ.get("LLM_MODEL", "gpt-3.5-turbo"),
            "messages": [
                {"role": "system", "content": "你是一位专业的投资分析师。"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }).encode('utf-8')
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        req = urllib.request.Request(
            endpoint,
            data=data,
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            result = json.loads(response.read().decode('utf-8'))
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                return str(result)
                
    except Exception as e:
        return f"[模型调用失败: {str(e)}]\n\n原始分析内容：\n{prompt[:500]}..."


def _format_for_openclaw(prompt: str) -> str:
    """
    为 OpenClaw 环境格式化输出
    OpenClaw 会捕获这个输出并使用其内置模型处理
    """
    # 返回一个特殊标记格式，OpenClaw 可以识别并处理
    return f"""[AI_ANALYSIS_REQUEST]
{prompt}
[END_AI_ANALYSIS_REQUEST]"""


def _format_no_model_response(prompt: str) -> str:
    """无可用模型时的响应"""
    return f"""[未配置AI模型]

当前未检测到可用的AI模型。请配置以下环境变量之一：

1. OpenClaw 环境（推荐）：
   无需额外配置，OpenClaw 会自动处理

2. OpenAI 兼容接口：
   export OPENAI_API_KEY=your_api_key
   export OPENAI_BASE_URL=https://api.openai.com/v1  # 可选

3. 自定义 LLM 接口：
   export LLM_API_KEY=your_key
   export LLM_API_BASE=https://your-api-endpoint/v1
   export LLM_MODEL=your-model-name

4. HTTP 端点：
   export OPENCLAW_MODEL_ENDPOINT=http://localhost:8000/generate

---
原始分析内容（供手动复制到AI工具）：
{prompt[:800]}...
"""


def clean_ai_output(raw_result: str) -> str:
    """清理AI输出结果"""
    cleaned = raw_result
    
    # 移除 think 标签
    for prefix in ["<think>", "</thinking>", "<thinking>", "</thinking>"]:
        cleaned = cleaned.replace(prefix, "")
    
    # 提取 TextPart 内容
    import re
    text_match = re.search(r"TextPart\([^)]*text='([^']*)',?", cleaned, re.DOTALL)
    if text_match:
        cleaned = text_match.group(1)
    
    # 移除内部格式标签行
    lines = cleaned.split('\n')
    filtered_lines = []
    for line in lines:
        line_stripped = line.strip()
        if any(tag in line_stripped for tag in [
            'TurnBegin(', 'StepBegin(', 'ThinkPart(', 'TextPart(',
            'StatusUpdate(', 'TurnEnd()', 'StepEnd()', 'context_usage=',
            'token_usage=', 'message_id=', 'context_tokens=',
            "type='think'", "type='text'", 'encrypted='
        ]):
            continue
        filtered_lines.append(line)
    
    cleaned = '\n'.join(filtered_lines).strip()
    cleaned = cleaned.replace("\\n", "\n")
    cleaned = cleaned.replace("\\'", "'")
    
    return cleaned


# 兼容性：保持与原代码兼容
__all__ = ['call_ai', 'clean_ai_output']
