---
name: dev-skill
description: 根据PRD文档自动生成SwiftUI iOS工程代码。当接收到prd-skill的输出时自动触发，生成可运行的iOS应用代码。
---

# Dev Skill - 自动代码生成器

## 🎯 功能概述

本skill根据PRD文档自动生成完整的SwiftUI iOS工程代码。作为"一人公司自动开发流水线"的第二环节，负责将产品需求转化为可运行的代码。

## 🔄 触发条件

自动触发条件：
1. prd-skill生成PRD文档后自动触发
2. 接收到包含PRD文档路径的消息
3. 检测到`/Users/tangchao/.openclaw/workspace/prd-output/`目录中有新PRD

## 📋 输入输出规范

### 输入
- PRD文档（Markdown格式）
- 项目元数据（JSON格式）
- 技术栈配置

### 输出
完整的SwiftUI iOS工程，包含：
- 项目结构文件
- SwiftUI视图代码
- 数据模型
- 业务逻辑
- 资源文件
- 配置文件

## 🚀 处理流程

### 步骤1：PRD解析
1. 读取PRD文档
2. 提取功能需求和技术要求
3. 分析页面设计和业务流程

### 步骤2：架构设计
1. 设计应用架构（MVVM）
2. 规划文件结构
3. 确定数据流方案

### 步骤3：代码生成
1. 生成项目配置文件（Package.swift）
2. 创建SwiftUI视图组件
3. 实现业务逻辑和数据模型
4. 添加资源文件和图标

### 步骤4：工程构建
1. 创建完整的Xcode项目结构
2. 配置依赖和编译选项
3. 生成可运行的工程

### 步骤5：流水线传递
1. 自动触发qa-skill
2. 传递代码仓库路径
3. 记录构建状态

## 📁 项目结构

生成的iOS工程结构：
```
{项目名称}/
├── Package.swift
├── Sources/
│   ├── {项目名称}App.swift
│   ├── Views/
│   │   ├── ContentView.swift
│   │   ├── {功能视图1}.swift
│   │   └── {功能视图2}.swift
│   ├── Models/
│   │   ├── {数据模型1}.swift
│   │   └── {数据模型2}.swift
│   ├── ViewModels/
│   │   ├── {视图模型1}.swift
│   │   └── {视图模型2}.swift
│   └── Services/
│       ├── {服务1}.swift
│       └── {服务2}.swift
├── Resources/
│   ├── Assets.xcassets
│   └── Preview Content/
└── Tests/
    └── {项目名称}Tests.swift
```

## 🔧 技术栈配置

### 默认技术栈
- **平台**: iOS 15.0+
- **UI框架**: SwiftUI
- **架构模式**: MVVM
- **数据存储**: UserDefaults（简单）/ CoreData（复杂）
- **网络请求**: URLSession
- **依赖管理**: Swift Package Manager

### 代码规范
- 遵循Swift API设计指南
- 使用Swift Concurrency（async/await）
- 实现错误处理机制
- 添加代码注释和文档

## 🔗 与其他Skill的集成

### 上游依赖
- 从prd-skill接收PRD文档
- 验证PRD完整性和可行性

### 向下游传递
- 自动调用qa-skill进行测试
- 传递代码仓库路径
- 传递构建配置信息

### 状态同步
- 更新流水线状态
- 记录代码生成进度
- 报告错误和警告

## ⚙️ 配置参数

### 代码生成选项
```yaml
architecture: mvvm
min_ios_version: "15.0"
use_combine: true
use_coredata: false
include_tests: true
code_style: apple
```

### 项目配置
- `project_name`: 项目名称
- `bundle_id`: 包标识符
- `team_id`: 开发团队ID（可选）
- `version`: 初始版本号

## 📊 质量保证

### 代码验证
1. 语法检查（Swift语法）
2. 编译测试（模拟编译）
3. 架构验证（模式一致性）
4. 依赖检查（包兼容性）

### 错误处理
- PRD不完整时请求补充
- 技术不可行时调整方案
- 生成失败时回滚操作

## 🎨 代码生成模板

### SwiftUI视图模板
```swift
import SwiftUI

struct {视图名称}: View {
    @StateObject private var viewModel = {视图模型}()
    
    var body: some View {
        VStack {
            // 视图内容
            Text("Hello, World!")
                .font(.title)
                .foregroundColor(.primary)
        }
        .padding()
        .onAppear {
            viewModel.loadData()
        }
    }
}

struct {视图名称}_Previews: PreviewProvider {
    static var previews: some View {
        {视图名称}()
    }
}
```

### 视图模型模板
```swift
import SwiftUI
import Combine

class {视图模型}: ObservableObject {
    @Published var data: [String] = []
    
    func loadData() {
        // 加载数据逻辑
    }
}
```

## 📈 性能指标

### 生成时间
- 小型项目（<5个页面）: < 3分钟
- 中型项目（5-10个页面）: < 8分钟
- 大型项目（>10个页面）: < 15分钟

### 代码质量
- 编译通过率: > 98%
- 架构一致性: > 95%
- 代码规范符合度: > 90%

## 🔄 持续改进

### 模板优化
1. 收集运行时反馈
2. 分析代码质量
3. 优化生成模板

### 技术更新
- 跟踪SwiftUI新特性
- 更新最佳实践
- 添加新架构模式支持

---

**注意**: 本skill是"一人公司自动开发流水线"的第二环节，生成代码后会自动触发qa-skill进行测试，确保代码质量。