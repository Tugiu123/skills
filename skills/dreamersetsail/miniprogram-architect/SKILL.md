---
name: 'miniprogram-architect'
description: '提供微信小程序架构设计、项目结构优化、代码规范制定和组件库建立支持。当用户需要搭建新的微信小程序项目、重构现有项目结构或建立组件库时调用。'
---

# 微信小程序架构师

## 功能介绍

本技能专注于微信小程序的架构设计和项目管理，为用户提供以下支持：

- 微信小程序项目结构设计和优化
- 代码规范和目录分割标准制定
- 组件库建立和复用策略
- 性能优化和最佳实践
- 项目架构文档编写

## 适用场景

当用户需要：

- 新建微信小程序项目并搭建完整目录结构
- 重构现有小程序项目结构
- 制定团队开发规范和标准
- 建立可复用的组件库
- 优化小程序性能和加载速度


## 项目架构

### 目录结构

```
├── api/             # API相关文件
├── assets/          # 静态资源
│   ├── images/      # 图片资源
│   └── styles/      # 样式文件
├── pages/           # 页面文件
│   ├── index/       # 首页
│   └── tabBar/      # 底部导航栏页面
├── utils/           # 工具函数
├── app.js           # 小程序入口文件
├── app.json         # 小程序配置文件
└── app.wxss         # 全局样式文件
```

### 技术栈

- 微信小程序原生开发
- WXML + WXSS + JavaScript
- WeUI组件库
- 微信官方API

## 使用指南

### 项目初始化

1. **目录结构搭建**：创建标准的小程序目录结构
2. **配置文件设置**：配置app.json、project.config.json等文件
3. **基础文件创建**：创建app.js、app.wxss等基础文件

### 代码规范

1. **命名规范**：文件、变量、函数的命名规则
2. **代码风格**：缩进、注释、代码组织方式
3. **目录分割**：页面、组件、工具函数的目录划分标准

### 组件库建立

1. **组件设计**：设计可复用的组件结构
2. **组件规范**：组件命名、参数传递、事件处理
3. **组件文档**：编写组件使用说明和示例

### 性能优化

1. **代码体积优化**：减少小程序包大小
2. **加载性能优化**：提高页面加载速度
3. **运行性能优化**：优化小程序运行时性能

## 最佳实践

### 目录结构最佳实践

- **模块化**：按功能模块划分目录
- **组件化**：将可复用部分抽象为组件
- **工具函数**：将通用功能封装为工具函数

### 代码规范最佳实践

- **命名规范**：使用驼峰命名法，避免使用拼音
- **注释规范**：关键代码添加注释，说明功能和实现思路
- **代码组织**：逻辑清晰，结构合理

### 性能优化最佳实践

- **按需加载**：使用lazyCodeLoading和componentPlaceholder
- **图片优化**：使用合适的图片格式和大小
- **网络请求优化**：合理使用缓存，减少请求次数

## 示例

### 项目结构示例

```
├── api/             # API相关文件
│   ├── config.js    # API配置
│   ├── ecbc.js      # 函证相关API
│   └── fetch.js     # 网络请求封装
├── assets/          # 静态资源
│   ├── images/      # 图片资源
│   └── styles/      # 样式文件
├── pages/           # 页面文件
│   ├── index/       # 首页
│   └── tabBar/      # 底部导航栏页面
│       ├── home/    # 首页
│       ├── folder/  # 档案夹
│       └── mine/    # 我的
├── utils/           # 工具函数
│   ├── request.js   # 请求工具
│   ├── util.js      # 通用工具
│   └── version.js   # 版本工具
├── app.js           # 小程序入口文件
├── app.json         # 小程序配置文件
└── app.wxss         # 全局样式文件
```

### 配置文件示例

```json
{
  "pages": [
    "pages/index/index",
    "pages/tabBar/home/home",
    "pages/tabBar/folder/folder",
    "pages/tabBar/mine/mine"
  ],
  "window": {
    "backgroundTextStyle": "dark",
    "navigationBarBackgroundColor": "#FFFFFF",
    "navigationBarTitleText": "币码E函证",
    "navigationBarTextStyle": "black"
  },
  "tabBar": {
    "color": "#666666",
    "selectedColor": "#4A76F3",
    "backgroundColor": "#ffffff",
    "borderStyle": "black",
    "list": [
      {
        "pagePath": "pages/tabBar/home/home",
        "text": "首页",
        "iconPath": "assets/images/tabbar/home.png",
        "selectedIconPath": "assets/images/tabbar/home_active.png"
      },
      {
        "pagePath": "pages/tabBar/folder/folder",
        "text": "档案夹",
        "iconPath": "assets/images/tabbar/folder.png",
        "selectedIconPath": "assets/images/tabbar/folder_active.png"
      },
      {
        "pagePath": "pages/tabBar/mine/mine",
        "text": "我的",
        "iconPath": "assets/images/tabbar/mine.png",
        "selectedIconPath": "assets/images/tabbar/mine_active.png"
      }
    ]
  },
  "sitemapLocation": "sitemap.json",
  "useExtendedLib": {
    "weui": true
  },
  "lazyCodeLoading": "requiredComponents"
}
```

## 注意事项

- 遵循微信小程序开发规范
- 注意小程序代码体积限制（主包不超过2MB）
- 确保API调用的安全性
- 优化用户体验和页面性能
- 保持代码的可维护性和可扩展性