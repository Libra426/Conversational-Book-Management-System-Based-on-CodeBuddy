# 任务拆解

> 实现阶段不得修改 baseline specs。每个任务适合 Agent 一次完成。

| 任务 | 目标 | 允许修改 | 禁止修改 | 验收标准 |
|---|---|---|---|---|
| TASK-001 | 初始化项目结构与启动类 | app/main.py、database.py、依赖文件 | specs/** | 应用可启动 |
| TASK-002 | 领域实体与枚举 | app/domain/** | specs/** | 实体字段与枚举完整 |
| TASK-003 | Repository 层 | app/repositories/** | specs/** | 读写接口可用 |
| TASK-004 | 借阅规则策略 BorrowPolicy | app/services/policy_service.py | specs/** | 各类型数量/天数正确 |
| TASK-005 | 罚款规则策略 FineRule | app/services/fine_service.py | specs/** | 罚款计算正确 |
| TASK-006 | 读者与借阅证管理 | app/services/reader_service.py、routers | specs/** | 注册/办证/注销可用 |
| TASK-007 | 图书标题与馆藏管理 | app/services/catalog_service.py | specs/** | 增删标题/副本可用 |
| TASK-008 | 办理借书 | circulation 相关 | specs/** | 借书成功 + 各失败分支 |
| TASK-009 | 办理还书 | circulation 相关 | specs/** | 还书 + 超期罚款 |
| TASK-010 | 预约图书 | reservation 相关 | specs/** | 预约 + 重复预约拒绝 |
| TASK-011 | 查询借阅信息与权限 | circulation/权限 | specs/** | 本人可查、越权拒绝 |
| TASK-012 | 管理员权限与规则维护 | admin 路由、deps | specs/** | 权限隔离、规则增改 |
| TASK-013 | 完善测试覆盖 | tests/** | specs/** | 测试计划全部通过 |
