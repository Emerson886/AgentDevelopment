# 基于 YOLOv8 与 LLM Agent 的 PCB 缺陷检测系统（桌面应用 + AI 助手）

## 技术栈：Python · PySide6 · Ultralytics YOLOv8 · OpenCV · LangChain · DeepSeek API · Milvus · BGE-M3 · PyInstaller

**项目描述**：独立开发 PCB 裸板缺陷检测桌面系统，支持图片、文件夹、视频及摄像头实时四种检测模式，覆盖 6 类缺陷，内置三档模型并可热插拔自定义权重；集成大模型 AI 助手：RAG 知识问答负责缺陷知识解答，Agent 工具负责调参、检测、摄像头等系统操作，用户可用自然语言完成全流程控制。

## 主要工作：

检测引擎：基于 Ultralytics YOLOv8 封装多线程检测服务，支持置信度、最大缺陷数、JSON/TXT 标注等参数动态配置，检测统计实时展示并写入历史记录持久化；

桌面 GUI：基于 PySide6 实现检测/历史/AI 对话/参数四大模块，视频双屏播放、图片比对、历史表格管理、摄像头实时检测（独立 QThread + 定时器采集）；

AI 助手（Agent）：基于 LangChain create_agent 接入 DeepSeek，设计 8 个真实生效的工具（状态查询、参数调整、摄像头控制、检测执行等），返回结构化 JSON；集成 LangGraph 中间件（长对话摘要、工具选择裁剪、自定义状态预检）与会话检查点实现多轮记忆；

RAG 知识问答：构建 Milvus 向量数据库 + BGE-M3 嵌入（1024 维） 的检索增强链路——知识文档递归分块（200 字/80 重叠）→ 批量向量化入库 → 每轮提问实时检索 top-5 相关片段注入 Prompt，系统提示约束模型严格依据知识库作答、未命中时明确拒绝，与 Agent 操作工具形成"知识 + 操作"双通道；

架构设计：设计 ToolBridge 线程桥（Qt 信号 + threading.Event 同步 RPC），解决 Agent 工作线程与 Qt 主线程的控件安全交互；长任务采用 pending/resolve 异步结算与超时取消机制，三个工作线程并行不阻塞界面；

工程化：PyInstaller 打包（collect_all 收集 ultralytics/torch 依赖）、历史 JSON 持久化、无界面模式可调试工具与检索链路。

## RAG 知识问答子系统：

**向量化与存储**：接入 SiliconFlow 托管的 BGE-M3 嵌入模型（1024 维），使用 Milvus 向量数据库（COSINE 相似度）存储知识向量；

**文档处理**：对 PCB 缺陷知识文档使用 RecursiveCharacterTextSplitter 递归分块（chunk 200 字 / 重叠 80 字，自定义章节分隔符优先级），离线批量向量化后 upsert 入库；

**检索增强**：每轮提问将问题向量化后在 Milvus 中检索 top-5 最相关片段（含距离分数、来源、chunk 编号），拼装为上下文注入 Prompt；

**约束生成**：系统提示明确"严格遵循提供的知识库回答，知识库没有则回答不知道"，有效抑制幻觉，与 8 个操作型 Agent 工具协同——知识性问题走 RAG、操作性问题走工具，互不干扰。
