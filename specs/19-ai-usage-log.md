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

## 第 6 次使用

- **使用工具**：Claude Code
- **使用阶段**：前端重构 + 后端最小增强 + 合规性审查与修正
- **使用任务**：①重做前端（按每种身份的 main 业务流程顺序组织工作台，前后端可拆分）；②后端最小增强以支撑前端展示；③对照 specs 逐项核查并修复规范违例。
- **输入 Prompt 摘要**：详细阅读实验指导书与四个实验文档，检查代码是否按规范完成；调用 frontend-design / ui-ux-pro-max 重做前端，重点保证每种身份下不同功能之间的流程顺序、体验舒适便捷；随后按「一切按照文档中所给的规范要求来」补齐合规缺口。
- **Agent 修改文件**：static/index.html、static/css/app.css、static/js/api.js、static/js/app.js；app/domain/models.py、app/schemas/{circulation,reservation,catalog,admin}.py、app/repositories/{reader,circulation,reservation,catalog}_repo.py、app/services/{reader,policy,fine,admin}_service.py、app/routers/{readers,admin}.py、app/seed.py；tests/{test_reader,test_permission,test_policy}.py；README.md
- **输出摘要**：①前端三文件分离（api.js 以 `API_BASE` 为唯一拆分点），读者/馆员/管理员三种身份分别按「查询图书→我的借阅→我的预约→注册账号」「办理借书→办理还书→读者借阅查询」「借阅证管理→图书与馆藏→人员管理→规则管理」编号导航；②后端纯增量新增读者/借阅证/馆员/系统管理员/借阅规则/罚款规则列表端点，借阅/预约/书目 DTO 内联书名/作者/条码/馆藏数；③修复 3 处规范违例：BR-002 借阅证号改为 `CARD+4位年份+6位序号`、GET /api/readers/{id} 增加「读者仅查本人」权限校验、借阅/罚款规则增加非负校验（负数返回 422）。
- **人工审查结果**：证号格式现为 CARD2026xxxxxx 全局唯一；读者越权查他人信息返回 403；规则参数非负校验生效；前端流程顺序与 UC-001~004 / 101~103 / 201~209 对应；现有 library.db 已就地迁移为新证号。
- **测试结果**：33 个测试全部通过（原 29 + 新增 4：证号格式、本人信息权限 ×2、负数规则校验）。
- **Git 提交**：（待提交）

## 第 7 次使用

- **使用工具**：Claude Code
- **使用阶段**：读者身份模型调整（借阅证号对外、读者 ID 内部）
- **使用任务**：让读者登录、查询借阅、预约、借书统一使用借阅证号，读者 ID 仅作数据库主键，废弃对外暴露读者 ID。
- **输入 Prompt 摘要**：现在整个系统借阅证号和读者 ID 是否一致？可以在登录或借书均使用借阅证号、废弃读者 ID 吗？（用户选择「证号对外、ID 留内部」）
- **Agent 修改文件**：app/services/reader_service.py、app/routers/readers.py、tests/test_reader.py、static/js/app.js、README.md、specs/19-ai-usage-log.md
- **输出摘要**：后端新增 `GET /api/readers/by-card/{card_no}`（借阅证号 → 读者，仅有效证），ReaderService 增加 `get_reader_by_card`；前端读者工作台把「读者 ID 输入框」改为「借阅证号输入框」，输入证号后调 by-card 解析出内部读者 id 并缓存证号/姓名，注册成功提示改为「到馆员处领取借阅证」，其余「读者ID」文案统一改为「借阅证号」。
- **人工审查结果**：证号对外、id 内部的主键/身份边界清晰；借阅证号全局唯一且 1:1 映射读者 id；前端登录态用 localStorage 持久化证号，刷新后可自动恢复登录。
- **测试结果**：35 个测试全部通过（原 33 + 新增 2：证号解析成功 / 证号不存在返回 404）。
- **Git 提交**：（待提交）
