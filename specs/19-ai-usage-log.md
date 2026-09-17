# AI 使用记录

## 第 1 次使用

- **使用工具**：Claude Code
- **使用阶段**：需求分析 + UML 建模 + 架构设计 + 详细设计
- **使用任务**：生成全部 specs 文档（00–19）与 PlantUML 图
- **输入 Prompt 摘要**：按顺序阅读实验概述/实验一/实验二/提示词手册，产出 Spec-Driven 图书管理系统的完整规格。
- **Agent 修改文件**：specs/00–19、constitution.md、4 张 .puml
- **输出摘要**：需求规格（FR-001~016 + BR-001~013）、用例、领域模型、架构、数据库、API、测试计划、任务拆解、风险与审查清单。
- **人工审查结果**：经核对与课程要求一致，借阅/罚款规则数值已人工确认。
- **测试结果**：不适用（文档阶段）。
- **Git 提交**：baseline experiment 1 & 2 specs

## 第 2 次使用

- **使用工具**：Claude Code
- **使用阶段**：代码实现 + 测试生成
- **使用任务**：按 TASK-001~013 实现分层代码与 pytest 测试
- **输入 Prompt 摘要**：依据冻结后的 specs 实现 FastAPI 分层图书管理系统。
- **Agent 修改文件**：app/**、tests/**
- **人工审查结果**：核对分层架构、策略模式（BorrowPolicy/FineRule）、权限隔离（X-Role）均符合 specs；借书前检查借阅证/数量/超期未还/副本可借，还书超期生成罚单，均与用例一致。
- **测试结果**：25 个测试全部通过（借还/预约/权限/策略）。
- **Git 提交**：implement library management system

## 第 3 次使用

- **使用工具**：Claude Code
- **使用阶段**：对照《实验指导书》审查与补齐
- **使用任务**：重读《AI时代软件设计实验工具链使用说明书》与《软件设计与体系结构实验指导书2026》，逐条对照已交付物，补齐缺口。
- **输入 Prompt 摘要**：再仔细阅读这两个文档，检查是否还有功能或要求未完成/完成不对，给出审查列表。
- **Agent 修改文件**：app/domain/enums.py、app/seed.py、tests/test_policy.py、specs/00/01/05/06/13、README.md、.gitignore，新增 specs/20-design-class-diagram.puml
- **输出摘要**：识别并修复 3 处缺口——①补齐读者类型「专科生 JUNIOR_COLLEGE（3 本/30 天）」；②新增分层「设计类图」以覆盖指导书实验一·步骤4「设计各层类/接口及交互（类图）」；③`.gitignore` 补 `.env`。
- **人工审查结果**：专科生借阅规则取 3 本/30 天（指导书未给具体数值，人工确认）；还书采用「更新借阅信息为已还」而非「删除」，符合实验概述「删除或更新」表述。
- **测试结果**：25 个测试全部通过（在 test_policy 中新增 2 条专科生策略断言）。
- **Git 提交**：review against guidebook: add junior-college type, design class diagram, .env

## 第 4 次使用

- **使用工具**：Claude Code
- **使用阶段**：接口体验增强
- **使用任务**：①借阅证内联读者姓名/院系；②为 /docs 增加 Authorize 登录按钮。
- **输入 Prompt 摘要**：借阅证需包含姓名/院系/证号；采用 HTTPBearer/OAuth2 方案把角色挂到 /docs 右上角 Authorize。
- **Agent 修改文件**：app/domain/models.py、app/schemas/reader.py、app/services/reader_service.py、app/deps.py、app/routers/readers.py、tests/test_reader.py、tests/test_permission.py、README.md
- **输出摘要**：BorrowCard 增加 reader_name/department 属性并内联到 BorrowCardOut；deps.py 增加 HTTPBearer 方案与 get_identity，Bearer 令牌即角色（如 admin:1），优先于 X-Role 头，向后兼容。
- **人工审查结果**：借阅证三字段（证号/姓名/院系）现于 API 返回中直接体现；Authorize 登录一次全局生效，且保留 X-Role 头兼容。
- **测试结果**：29 个测试全部通过（新增 4 条：借阅证内联字段 + 3 条 Bearer 权限）。
- **Git 提交**：5005a73

## 第 5 次使用

- **使用工具**：Claude Code
- **使用阶段**：演示数据准备
- **使用任务**：写入演示书籍/馆藏副本/读者/借阅证，便于直接测试借还书。
- **输入 Prompt 摘要**：给系统加入一些书籍信息，便于测试借书还书。
- **Agent 修改文件**：app/seed.py、README.md
- **输出摘要**：seed.py 新增 seed_demo_data（5 书目 + 9 馆藏副本 + 3 读者 + 3 借阅证，幂等），覆盖 5 种借出物类型；README 增补演示数据表。
- **人工审查结果**：演示卡号 CARD-001/002/003 与条码 BC-xxxx 与借还接口字段一致，端到端借书(201)/还书(200)/查询(200)验证通过。
- **测试结果**：29 个测试全部通过（不受演示数据影响，测试库独立）。
- **Git 提交**：（待提交）
