---
name: xhs-parser
description: 小红书（XHS/RedNote）链接解析工具。解析小红书短链接或作品链接，获取作品信息（标题、作者、正文、标签、下载地址）。当用户发送小红书链接（xhslink.com 或 xiaohongshu.com）并要求解析、下载、分析内容时触发。
---

# XHS Parser - 小红书链接解析

基于 **XHS-Downloader** 实现小红书链接解析和下载。

## 环境要求

- Python 3.12+
- XHS-Downloader 安装在 `~/projects/xhs-downloader`

## 安装依赖

```bash
# 如果还没有 Python 3.12
brew install python@3.12

# 创建虚拟环境并安装依赖
cd ~/projects/xhs-downloader
/opt/homebrew/bin/python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 使用方式

### 方式1：API 模式（推荐）

```bash
cd ~/projects/xhs-downloader
source venv/bin/activate
python main.py api --port 5556
```

然后调用：
```bash
curl -X POST "http://127.0.0.1:5556/xhs/detail" \
  -H "Content-Type: application/json" \
  -d '{"url": "xhslink链接", "download": false}'
```

### 方式2：命令行直接下载

```bash
cd ~/projects/xhs-downloader
source venv/bin/activate
python main.py -u "小红书链接" \
  --work_path ~/Desktop/ \
  --folder_name "下载文件夹名"
```

## 支持的链接格式

- `http://xhslink.com/o/xxx` （短链接）
- `https://www.xiaohongshu.com/explore/作品ID`
- `https://www.xiaohongshu.com/discovery/item/作品ID`

## 返回字段说明

| 字段 | 含义 |
|------|------|
| 作品标题 | 笔记标题 |
| 作品描述 | 笔记正文内容 |
| 作者昵称 | 发布者名字 |
| 点赞数量 | 点赞数 |
| 收藏数量 | 收藏数 |
| 评论数量 | 评论数 |
| 作品类型 | 图文/视频 |
| 下载地址 | 媒体文件直链 |

## 注意事项

- 不设置 Cookie 时视频只能下载低分辨率
- 链接有日期限制，建议使用最新获取的链接
