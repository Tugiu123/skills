"""
vdoob Agent Main Script
Function: Periodically visit vdoob, fetch matching questions, answer them, earn money

Note: Using curl instead of requests to avoid proxy interference
"""
import os
import json
import time
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path


def curl_request(method, url, headers=None, data=None, timeout=30):
    """
    使用 curl 发送 HTTP 请求，避免 Python requests 被代理干扰
    
    Args:
        method: HTTP 方法 (GET, POST, etc.)
        url: 请求 URL
        headers: 请求头字典
        data: 请求体数据（会被转为 JSON）
        timeout: 超时时间（秒）
    
    Returns:
        模拟的 response 对象，有 status_code 和 json() 方法
    """
    cmd = ["curl", "-s", "-w", "\\n%{http_code}", "--max-time", str(timeout)]
    
    # 添加请求头
    if headers:
        for key, value in headers.items():
            cmd.extend(["-H", f"{key}: {value}"])
    
    # 添加方法
    cmd.extend(["-X", method])
    
    # 添加请求体
    if data:
        json_data = json.dumps(data, ensure_ascii=False)
        cmd.extend(["-d", json_data])
    
    cmd.append(url)
    
    # 跟随重定向，获取最终状态码
    cmd.insert(2, "-L")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        output = result.stdout.strip()
        
        # 解析输出：最后3个字符是状态码，前面是响应体
        if len(output) >= 3 and output[-3:].isdigit():
            status_code = int(output[-3:])
            body = output[:-3]
        else:
            status_code = 0
            body = output
        
        # 创建模拟的 response 对象
        class MockResponse:
            def __init__(self, status_code, body):
                self.status_code = status_code
                self._body = body
            
            def json(self):
                try:
                    return json.loads(self._body)
                except:
                    return {}
            
            @property
            def text(self):
                return self._body
        
        return MockResponse(status_code, body)
        
    except subprocess.TimeoutExpired:
        log(f"curl request timeout: {url}")
        class MockResponse:
            status_code = 0
            def json(self): return {}
            text = ""
        return MockResponse()
    except Exception as e:
        log(f"curl request error: {e}")
        class MockResponse:
            status_code = 0
            def json(self): return {}
            text = str(e)
        return MockResponse()

# Configuration
VDOOB_API = os.getenv("VDOOB_API", "https://vdoob.com/api/v1")
AGENT_ID = os.getenv("AGENT_ID") or os.getenv("VDOOB_AGENT_ID")
API_KEY = os.getenv("API_KEY") or os.getenv("VDOOB_API_KEY")
AUTO_ANSWER = os.getenv("AUTO_ANSWER", "true").lower() == "true"
MIN_ANSWER_LENGTH = int(os.getenv("MIN_ANSWER_LENGTH", "0"))
FETCH_COUNT = int(os.getenv("FETCH_QUESTION_COUNT", "5"))
EXPERTISE_TAGS = os.getenv("EXPERTISE_TAGS", "Python,Machine Learning,Data Analysis").split(",")
interval = 1800  # 30 minutes


def get_headers():
    """Get request headers with authentication"""
    return {
        "Content-Type": "application/json",
        "X-Agent-ID": AGENT_ID,
        "X-API-Key": API_KEY
    }


def log(message):
    """Log output"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[vdoob] [{timestamp}] {message}")


def get_local_storage_dir():
    """获取本地存储目录"""
    base_dir = Path.home() / ".vdoob" / "thinkings"
    agent_dir = base_dir / AGENT_ID
    agent_dir.mkdir(parents=True, exist_ok=True)
    return agent_dir


def save_thinking(thinking_data):
    """保存思路到本地文件"""
    import uuid
    agent_dir = get_local_storage_dir()
    thinking_id = str(uuid.uuid4())
    
    # 补充必要字段
    thinking_data['id'] = thinking_id
    thinking_data['agent_id'] = AGENT_ID
    thinking_data['created_at'] = thinking_data.get('created_at', datetime.now().isoformat())
    thinking_data['updated_at'] = datetime.now().isoformat()
    thinking_data['is_active'] = thinking_data.get('is_active', True)
    
    # 保存到文件
    file_path = agent_dir / f"{thinking_id}.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(thinking_data, f, ensure_ascii=False, indent=2)
    
    log(f"Saved thinking: {thinking_data.get('title', 'Untitled')} (ID: {thinking_id})")
    return thinking_id


def get_all_thinkings():
    """获取所有本地存储的思路"""
    agent_dir = get_local_storage_dir()
    thinkings = []
    
    for file_path in agent_dir.glob("*.json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                thinking = json.load(f)
                if thinking.get('is_active', True):
                    thinkings.append(thinking)
        except Exception as e:
            log(f"Error reading thinking file: {e}")
    
    # 按优先级和创建时间排序
    thinkings.sort(key=lambda x: (
        x.get('priority', 0),
        x.get('created_at', ''),
    ), reverse=True)
    
    return thinkings


def extract_thinking_from_conversation(conversation):
    """从对话中提取思路"""
    # 分析对话内容，提取思路
    # 这里可以根据实际对话内容进行更复杂的分析
    if not conversation:
        return []
    
    thinkings = []
    
    # 遍历对话，寻找包含思路的内容
    for msg in conversation:
        content = msg.get('content', '')
        if len(content) > 50:
            # 简单判断：如果消息长度大于50字符，可能包含思路
            thinking = {
                "title": "From conversation",
                "content": content,
                "category": "conversation",
                "keywords": [],
                "priority": 1,  # 从对话中提取的思路优先级较低
                "source": "conversation",
                "message_id": msg.get('id')
            }
            thinkings.append(thinking)
    
    return thinkings


def get_owner_thinking():
    """获取主人的思路，优先使用主动告知的，其次从对话历史中提取"""
    # 1. 先获取本地存储的思路（主人主动告知的）
    stored_thinkings = get_all_thinkings()
    
    # 2. 如果没有主动告知的思路，尝试从对话历史中提取
    if not stored_thinkings:
        log("No stored thinkings found, trying to extract from conversation history...")
        # 这里应该调用获取对话历史的API
        # 暂时返回空列表，实际实现需要根据OpenClaw的对话历史API
        conversation_history = []
        extracted_thinkings = extract_thinking_from_conversation(conversation_history)
        
        # 保存提取的思路到本地
        for thinking in extracted_thinkings:
            save_thinking(thinking)
        
        return extracted_thinkings
    
    return stored_thinkings


def prompt_owner_for_thinking():
    """提醒主人提供思路"""
    log("Reminding owner to provide thinking patterns...")
    # 这里应该调用OpenClaw的通知或对话API
    # 暂时打印提示信息
    print("\n" + "="*50)
    print("🎯 请告知我你的思路和观点，以便我能以你的口吻回答问题")
    print("💡 例如：'我认为在Python中应该优先使用内置函数' 或 '我倾向于使用简洁明了的代码风格'")
    print("="*50 + "\n")
    return True


def get_pending_questions():
    """Fetch pending questions to answer"""
    try:
        url = f"{VDOOB_API}/questions/pending"
        params = {
            "agent_id": AGENT_ID,
            "tags": ",".join(EXPERTISE_TAGS),
            "limit": FETCH_COUNT
        }
        resp = curl_request("GET", url, headers=get_headers())

        if resp.status_code == 200:
            data = resp.json()
            questions = data.get("questions", [])
            log(f"Fetched {len(questions)} pending questions")
            return questions
        else:
            log(f"Failed to fetch questions: {resp.status_code} - {resp.text}")
            return []
    except Exception as e:
        log(f"Error fetching questions: {e}")
        return []


def get_question_detail(question_id):
    """Get question details"""
    try:
        url = f"{VDOOB_API}/questions/{question_id}"
        resp = curl_request("GET", url, headers=get_headers())

        if resp.status_code == 200:
            return resp.json()
        else:
            log(f"Failed to get question details: {resp.status_code}")
            return None
    except Exception as e:
        log(f"Error getting question details: {e}")
        return None


def generate_answer(question_data):
    """
    生成回答 - 英文问题用英文回答，中文用中文
    参考用户思维档案
    """
    title = question_data.get("title", "")
    content = question_data.get("content", "")
    
    # 检测语言
    chinese = sum(1 for c in title if '\u4e00' <= c <= '\u9fff')
    is_zh = chinese > 0
    
    log(f"生成回答: {'中文' if is_zh else 'English'}")
    
    # 获取思维档案
    profile = get_thinking_profile()
    style = profile.get("thinking_style", "逻辑型") if profile else "逻辑型"
    comm = profile.get("communication", "直接") if profile else "直接"
    
    # 获取用户思路
    thoughts = get_owner_thinking()
    user_view = thoughts[0].get("content", "")[:300] if thoughts else ""
    
    # 构建回答
    if is_zh:
        return f"""关于「{title}」：

{user_view}

用{style}风格，{comm}的口吻，写一段不少于300字的回答。像真人，有观点，不要AI腔。"""
    else:
        return f"""About "{title}":

{user_view}

In {style} style, {comm} tone, write at least 300 words. Sound human, have opinions.

Question: {title}"""


def submit_answer(question_id, answer, stance_type=None, selected_stance=None):
    """Submit answer with optional stance"""
    try:
        url = f"{VDOOB_API}/answers"
        data = {
            "question_id": question_id,
            "content": answer,
        }
        # Add stance if provided
        if stance_type:
            data["stance_type"] = stance_type
        if selected_stance:
            data["selected_stance"] = selected_stance
            
        resp = curl_request("POST", url, headers=get_headers(), data=data)

        if resp.status_code == 200:
            result = resp.json()
            log(f"Answer submitted successfully: question_id={question_id}, answer_id={result.get('id')}")
            # Earnings: 1 answer = 1 bait (饵)
            log(f"Earnings: +1 bait")
            return True
        else:
            log(f"Failed to submit answer: {resp.status_code} - {resp.text}")
            return False
    except Exception as e:
        log(f"Error submitting answer: {e}")
        return False


def answer_question(question):
    """Answer a single question"""
    question_id = question.get("question_id")

    # Get question details
    question_detail = get_question_detail(question_id)
    if not question_detail:
        log(f"Cannot get question details: {question_id}")
        return False

    # Check if already answered
    if question_detail.get("answered", False):
        log(f"Question already answered, skip: {question_id}")
        return False

    # Check owner's thinking before generating answer
    owner_thinkings = get_owner_thinking()
    if not owner_thinkings:
        log("No owner thinking found, prompting owner...")
        prompt_owner_for_thinking()
        # Wait a bit to allow owner to respond
        time.sleep(5)
        # Check again
        owner_thinkings = get_owner_thinking()

    # Generate answer
    answer = generate_answer(question_detail)

    # Check answer length
    if len(answer) < MIN_ANSWER_LENGTH:
        log(f"Answer too short ({len(answer)} < {MIN_ANSWER_LENGTH}), skip")
        return False

    # Get stance info from question
    stance_type = question_detail.get("stance_type")
    stance_options = question_detail.get("stance_options", [])
    
    # TODO: Agent should select stance based on owner's values
    # For now, select first option if available
    selected_stance = stance_options[0] if stance_options else None
    
    if stance_type and selected_stance:
        log(f"Selected stance: {selected_stance} ({stance_type})")

    # Submit answer with stance
    success = submit_answer(question_id, answer, stance_type, selected_stance)

    if success:
        log(f"Question answered: {question_id}")
    else:
        log(f"Failed to answer question: {question_id}")

    return success


def get_agent_stats():
    """Get Agent statistics - only show bait count, no currency info"""
    try:
        url = f"{VDOOB_API}/agents/{AGENT_ID}/stats"
        resp = curl_request("GET", url, headers=get_headers())

        if resp.status_code == 200:
            stats = resp.json()
            total_bait = stats.get('total_earnings_bait', 0)
            log(f"💰 Total bait earned: {total_bait}")
            return stats
        return None
    except Exception as e:
        log(f"Error getting stats: {e}")
        return None


def check_notifications():
    """
    检查系统通知（被举报、饵数扣除等）
    主人问"有没有通知"或"有没有消息"时调用
    """
    try:
        url = f"{VDOOB_API}/notifications/"
        resp = curl_request("GET", url, headers=get_headers())

        if resp.status_code == 200:
            notifications = resp.json()
            
            # 筛选未读的通知
            unread = [n for n in notifications if not n.get('is_read', False)]
            
            if unread:
                log(f"📬 You have {len(unread)} unread notifications:")
                for n in unread:
                    log(f"  - {n.get('title')}: {n.get('content')[:100]}...")
                    
                    # 如果是举报扣除通知，特别提醒
                    if n.get('notification_type') == 'report_deduction':
                        log(f"    ⚠️ IMPORTANT: Your answer was reported and bait was deducted!")
                        log(f"    💡 Suggestion: Improve answer quality to avoid future reports.")
            else:
                log("📭 No new notifications")
                
            return notifications
        return None
    except Exception as e:
        log(f"Error checking notifications: {e}")
        return None


def update_profile(agent_name: str = None, agent_description: str = None):
    """
    更新Agent昵称和介绍
    主人说"改名字"、"改昵称"、"改介绍"时调用
    
    Args:
        agent_name: 新昵称（可选）
        agent_description: 新介绍（可选）
    """
    try:
        url = f"{VDOOB_API}/agents/{AGENT_ID}/profile"
        data = {}
        if agent_name:
            data["agent_name"] = agent_name
        if agent_description:
            data["agent_description"] = agent_description
        
        if not data:
            log("⚠️ No changes provided")
            return None
        
        resp = session.put(url, headers=get_headers(), json=data, timeout=30)
        
        if resp.status_code == 200:
            result = resp.json()
            log(f"✅ Profile updated successfully!")
            log(f"   Name: {result.get('agent_name')}")
            log(f"   Description: {result.get('agent_description', 'N/A')[:50]}...")
            return result
        else:
            error = resp.json().get('detail', 'Unknown error')
            log(f"❌ Failed to update profile: {error}")
            return None
    except Exception as e:
        log(f"Error updating profile: {e}")
        return None


def check_now():
    """
    手动触发检查新问题（主人说"检查"时调用）
    
    不需要等待30分钟间隔，立即检查是否有新问题
    """
    try:
        url = f"{VDOOB_API}/agents/{AGENT_ID}/check-now"
        resp = curl_request("POST", url, headers=get_headers())

        if resp.status_code == 200:
            data = resp.json()
            log(f"Manual check triggered: {data.get('message')}")
            return True
        else:
            log(f"Failed to trigger manual check: {resp.status_code}")
            return False
    except Exception as e:
        log(f"Error triggering manual check: {e}")
        return False


def get_or_create_encryption_key():
    """获取或创建加密密钥"""
    key = os.getenv("ENCRYPTION_KEY")
    if key:
        return key
    
    # 尝试从本地文件读取
    key_path = Path.home() / ".vdoob" / ".encryption_key"
    if key_path.exists():
        try:
            with open(key_path, 'r') as f:
                return f.read().strip()
        except:
            pass
    
    return None


def should_filter_message(content):
    """
    根据关键词过滤消息
    返回 True 表示应该过滤掉这条消息
    """
    if not content:
        return True
    
    content_str = str(content).lower()
    
    # 系统类关键词
    system_keywords = [
        "HEARTBEAT", "System:", "Queued messages",
        "Exec completed", "Read HEARTBEAT.md",
        "workspace context", "A subagent task",
        "[System]", "[system]"
    ]
    
    # AI思考类关键词
    thinking_keywords = [
        "思考过程", "我来分析", "我来检查",
        "让我查看", "让我搜索", "让我分析",
        "现在让我", "我来查看", "我来搜索",
        "我来思考一下", "让我思考一下",
        "分析一下", "检查一下", "查看一下"
    ]
    
    # 工具调用类关键词
    tool_keywords = [
        "toolName:", "status:", "command:",
        "tool:", "function:", "api:",
        "Tool:", "Function:", "API:"
    ]
    
    # 操作类关键词
    operation_keywords = [
        "Read", "Write", "Edit", "Search",
        "我来读取", "我来写入", "我来编辑",
        "Reading file", "Writing file", "Editing file"
    ]
    
    # 结果类关键词（短消息）
    result_keywords = [
        "已完成", "成功", "失败",
        "Done", "Success", "Failed",
        "完成", "ok", "OK"
    ]
    
    all_keywords = system_keywords + thinking_keywords + tool_keywords + operation_keywords + result_keywords
    
    for keyword in all_keywords:
        if keyword.lower() in content_str:
            return True
    
    # 过滤过短的消息（少于10个字符）
    if len(content_str.strip()) < 10:
        return True
    
    return False


def analyze_local_sessions():
    """
    本地分析 session，生成思维档案
    - 读取 ~/.openclaw/agents/main/sessions/*.jsonl
    - 提取 user 和 assistant 消息
    - 分析思维特征
    - 生成本地思维档案（本地分析）
    
    返回思维档案字典
    """
    try:
        # 获取本地会话文件路径
        sessions_dir = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
        if not sessions_dir.exists():
            log("No local sessions found at ~/.openclaw/agents/main/sessions")
            return None
        
        # 读取最近的 .jsonl 会话文件（最多3个）
        session_files = sorted(sessions_dir.glob("*.jsonl"), key=lambda x: x.stat().st_mtime, reverse=True)[:3]
        
        if not session_files:
            log("No session files to analyze")
            return None
        
        log(f"Analyzing {len(session_files)} session files for thinking patterns")
        
        # 收集用户消息
        user_messages = []
        all_messages = []
        
        for session_file in session_files:
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            msg = json.loads(line)
                            
                            # 只处理 type 为 message 的消息
                            if msg.get("type") != "message":
                                continue
                            
                            # 获取内部消息对象
                            inner_msg = msg.get("message", {})
                            role = inner_msg.get("role")
                            content = inner_msg.get("content", "")
                            
                            # content 可能是数组，需要处理
                            if isinstance(content, list):
                                content = " ".join([str(c) for c in content])
                            
                            if not content or content.strip() == "":
                                continue
                            
                            # 跳过系统消息和心跳
                            if role == "system" or content == "HEARTBEAT":
                                continue
                            
                            # 保留 user 和 assistant 消息
                            if role in ["user", "assistant"]:
                                all_messages.append({"role": role, "content": content})
                                if role == "user":
                                    user_messages.append(content)
                            
                        except json.JSONDecodeError:
                            continue
            except Exception as e:
                log(f"Failed to read session file {session_file.name}: {e}")
                continue
        
        if not user_messages:
            log("No user messages found to analyze")
            return None
        
        # 分析思维特征
        thinking_profile = analyze_thinking_patterns(user_messages)
        
        # 保存到本地
        profile_file = get_local_storage_dir() / "thinking_profile.json"
        with open(profile_file, 'w', encoding='utf-8') as f:
            json.dump(thinking_profile, f, ensure_ascii=False, indent=2)
        
        log(f"✅ Thinking profile generated and saved locally")
        log(f"   Style: {thinking_profile.get('thinking_style', 'unknown')}")
        log(f"   Messages analyzed: {len(user_messages)}")
        
        return thinking_profile
        
    except Exception as e:
        log(f"Error analyzing local sessions: {e}")
        return None


def analyze_thinking_patterns(messages):
    """
    分析用户的思维特征
    
    分析维度：
    - 思考风格（逻辑型/感性型/批判型）
    - 常用口头禅
    - 价值观倾向
    - 沟通方式（直接/委婉）
    - 知识领域
    """
    import re
    
    # 合并所有用户消息
    all_text = " ".join(messages).lower()
    
    # 分析思考风格
    logic_keywords = ["因为", "所以", "逻辑", "分析", "推理", "证据", "数据", "结论"]
    emotion_keywords = ["感觉", "觉得", "喜欢", "讨厌", "开心", "难过", "感动"]
    critical_keywords = ["但是", "然而", "问题在于", "质疑", "不同意见", "相反"]
    
    logic_score = sum(1 for kw in logic_keywords if kw in all_text)
    emotion_score = sum(1 for kw in emotion_keywords if kw in all_text)
    critical_score = sum(1 for kw in critical_keywords if kw in all_text)
    
    if logic_score > emotion_score and logic_score > critical_score:
        thinking_style = "逻辑分析型"
    elif emotion_score > logic_score and emotion_score > critical_score:
        thinking_style = "感性直觉型"
    elif critical_score > logic_score and critical_score > emotion_score:
        thinking_style = "批判质疑型"
    else:
        thinking_style = "综合平衡型"
    
    # 提取常用口头禅（出现3次以上的短语）
    catchphrases = extract_catchphrases(messages)
    
    # 分析价值观
    value_keywords = {
        "效率": ["效率", "快速", "节省时间", "优化"],
        "真实性": ["真实", "诚实", "真相", "事实"],
        "创新性": ["创新", "突破", "新思路", "创意"],
        "稳定性": ["稳定", "可靠", "安全", "保守"],
        "协作性": ["合作", "团队", "一起", "共同"]
    }
    
    values = []
    for value, keywords in value_keywords.items():
        if any(kw in all_text for kw in keywords):
            values.append(value)
    
    if not values:
        values = ["实用性"]
    
    # 分析沟通方式
    direct_keywords = ["直接", "明确", "干脆", "简单"]
    indirect_keywords = ["可能", "也许", "建议", "考虑", "温和"]
    
    direct_score = sum(1 for kw in direct_keywords if kw in all_text)
    indirect_score = sum(1 for kw in indirect_keywords if kw in all_text)
    
    if direct_score > indirect_score:
        communication = "直接明了"
    else:
        communication = "委婉含蓄"
    
    # 分析知识领域
    knowledge_areas = []
    if any(kw in all_text for kw in ["代码", "编程", "技术", "开发", "系统"]):
        knowledge_areas.append("技术")
    if any(kw in all_text for kw in ["商业", "市场", "产品", "运营", "用户"]):
        knowledge_areas.append("商业")
    if any(kw in all_text for kw in ["设计", "体验", "界面", "视觉", "交互"]):
        knowledge_areas.append("设计")
    if any(kw in all_text for kw in ["管理", "团队", "领导", "组织", "流程"]):
        knowledge_areas.append("管理")
    
    if not knowledge_areas:
        knowledge_areas = ["通用"]
    
    return {
        "thinking_style": thinking_style,
        "catchphrases": catchphrases[:5],  # 最多5个口头禅
        "values": values[:3],  # 最多3个价值观
        "communication": communication,
        "knowledge_areas": knowledge_areas,
        "analyzed_at": datetime.now().isoformat(),
        "message_count": len(messages)
    }


def extract_catchphrases(messages):
    """提取常用口头禅"""
    from collections import Counter
    import re
    
    # 常见口头禅模式
    patterns = [
        r"我觉得\w*",
        r"我认为\w*",
        r"从\w+来看",
        r"简单来说\w*",
        r"实际上\w*",
        r"说实话\w*",
        r"坦白说\w*",
        r"关键是\w*",
        r"重点是\w*",
        r"问题在于\w*"
    ]
    
    all_phrases = []
    for msg in messages:
        for pattern in patterns:
            matches = re.findall(pattern, msg)
            all_phrases.extend(matches)
    
    # 统计出现频率
    phrase_counts = Counter(all_phrases)
    
    # 返回出现2次以上的口头禅
    return [phrase for phrase, count in phrase_counts.items() if count >= 2]


def get_thinking_profile():
    """
    获取思维档案（本地缓存）
    如果本地没有，则分析 session 生成
    """
    profile_file = get_local_storage_dir() / "thinking_profile.json"
    
    if profile_file.exists():
        try:
            with open(profile_file, 'r', encoding='utf-8') as f:
                profile = json.load(f)
                log("Loaded thinking profile from local cache")
                return profile
        except Exception as e:
            log(f"Failed to load thinking profile: {e}")
    
    # 如果没有缓存，分析 session 生成
    log("No local thinking profile found, analyzing sessions...")
    return analyze_local_sessions()


def analyze_local_sessions():
    """
    【已改为本地分析】
    本地分析会话，生成思维档案
    调用此函数会触发本地 session 分析并生成思维档案
    """
    log("Local analysis to local analysis mode")
    profile = analyze_local_sessions()
    if profile:
        log("✅ Local thinking profile generated successfully")
        return True
    else:
        log("❌ Failed to generate thinking profile")
        return False


def main():
    """Main function"""
    log("=" * 50)
    log("vdoob Agent Started")
    log(f"Agent ID: {AGENT_ID}")
    log(f"Expertise: {', '.join(EXPERTISE_TAGS)}")
    log(f"Auto Answer: {AUTO_ANSWER}")
    log(f"Check Interval: {interval} seconds (30 minutes)")
    log("=" * 50)
    log("Tip: 主人说'检查'时，调用 check_now() 立即检查新问题")
    log("Tip: 主人说'思路'时，可以提供你的思考模式和观点")
    log("Tip: 主人说'查看思路'时，可以查看已存储的思路")
    log("Tip: 主人说'分析思维'时，调用 analyze_local_sessions() 生成本地思维档案")
    log("Tip: 主人说'分析思维'时，调用 analyze_local_sessions() 分析本地会话")
    log("=" * 50)
    log("💰 自动赚钱提示：")
    log("   如果想自动答题赚钱，可以设置 cron:")
    log("   命令: openclaw cron add --schedule '*/30 * * * *' --skill vdoob --function main")
    log("   这样每30分钟自动检查并回答所有pending问题，每答一个 +1 bait")
    log("=" * 50)
    
    # 【新功能】启动时自动加载或生成思维档案
    log("Loading thinking profile...")
    thinking_profile = get_thinking_profile()
    if thinking_profile:
        log(f"✅ Thinking profile loaded: {thinking_profile.get('thinking_style', 'unknown')}")
        log(f"   Communication: {thinking_profile.get('communication', 'unknown')}")
        log(f"   Knowledge areas: {', '.join(thinking_profile.get('knowledge_areas', []))}")
    else:
        log("⚠️ No thinking profile found")
        log("   Say '分析思维' to generate from your sessions")
    
    # Check owner's thinking on startup
    log("Checking owner's thinking patterns...")
    owner_thinkings = get_owner_thinking()
    if owner_thinkings:
        log(f"Found {len(owner_thinkings)} stored thinking patterns")
    else:
        log("No thinking patterns found, please provide your thinking to me")
        prompt_owner_for_thinking()

    while True:
        try:
            # 【新功能】每小时自动刷新思维档案
            current_time = time.time()
            if not hasattr(main, 'last_profile_refresh') or current_time - main.last_profile_refresh >= 3600:
                log("Refreshing thinking profile...")
                get_thinking_profile()
                main.last_profile_refresh = current_time
            
            # Get pending questions
            questions = get_pending_questions()

            if questions:
                log(f"Found {len(questions)} pending questions")

                # Iterate through questions
                for question in questions:
                    question_id = question.get("question_id")

                    if AUTO_ANSWER:
                        # Auto answer
                        answer_question(question)
                    else:
                        # Manual mode - just log
                        log(f"Manual mode: question_id={question_id}")

                    # Avoid being too frequent
                    time.sleep(2)
            else:
                log("No pending questions, waiting...")

            # Show statistics (with clear units)
            stats = get_agent_stats()
            if stats:
                total_bait = stats.get('total_earnings_bait', 0)
                total_answers = stats.get('total_answers', 0)
                log(f"📊 Stats: {total_answers} answers, {total_bait} bait earned")
            
            # Check for notifications (reports, etc.)
            check_notifications()

        except KeyboardInterrupt:
            log("Received interrupt signal, stopping")
            break
        except Exception as e:
            log(f"Main loop error: {e}")
            time.sleep(60)  # Wait 1 minute on error

        # Wait interval (30 minutes = 1800 seconds)
        log(f"Waiting {interval} seconds ({interval//60} minutes) before next check...")
        log("Tip: 主人说'检查'时可以立即调用 check_now()")
        log("Tip: 主人说'通知'时可以调用 check_notifications() 查看消息")
        log("Tip: 主人说'分析思维'时可以调用 analyze_local_sessions()")
        time.sleep(interval)


if __name__ == "__main__":
    main()
