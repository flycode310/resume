# Agent 开发工程师技术栈关键词库

按 2025-2026 主流招聘市场整理,用于简历技术栈匹配和关键词命中。

## 一、LLM 与基础模型

### 商业模型
- **Anthropic Claude**(Opus 4.7 / Sonnet 4.6 / Haiku 4.5):最强 Agent 模型,擅长工具调用、长上下文、Computer Use
- **OpenAI GPT**(GPT-4o / o1 / o3):函数调用、Assistants API、Structured Output
- **Google Gemini**(2.0 Pro / Flash):多模态、Function Calling
- **国内**:通义千问(Qwen)、DeepSeek、智谱 GLM、百川、Kimi、豆包

### 开源模型
- Llama 3 / 4 系列、Qwen 系列、DeepSeek-R1、Mistral
- 推理加速:vLLM、SGLang、TensorRT-LLM
- 微调:LoRA、QLoRA、PEFT、Unsloth、ms-swift

## 二、Agent 框架

### 主流框架(2025-2026)
- **Anthropic Agent SDK** - 官方 Agent 框架,内置 MCP、记忆、子 Agent
- **LangGraph** - LangChain 出品的状态机式 Agent 编排,支持 Human-in-the-loop
- **OpenAI Swarm / Agents SDK** - 轻量级多 Agent 编排
- **LlamaIndex Agents** - 偏 RAG 的 Agent 框架
- **AutoGen v0.4** - 微软多 Agent 框架,异步事件驱动
- **CrewAI** - 角色扮演式多 Agent
- **Pydantic AI** - 类型安全的 Agent 框架

### 国产框架
- **Dify / Coze / FastGPT** - 低代码 Agent 平台
- **MetaGPT** - 多 Agent 软件开发
- **AgentScope** - 阿里达摩院

## 三、Agent 核心能力

### 工具使用(Tool Use / Function Calling)
- Function Calling 协议设计
- 工具描述编写(JSON Schema)、参数校验
- 工具调用错误处理与重试
- 工具结果的二次理解

### MCP(Model Context Protocol)
- Anthropic 提出,2024 年开源,已成跨厂商标准
- MCP Server 开发(stdio / SSE / HTTP transports)
- MCP Client 集成
- 资源(Resources)、提示(Prompts)、工具(Tools)三大原语

### RAG(检索增强生成)
- **向量数据库**:Pinecone、Weaviate、Milvus、Qdrant、Chroma、PGVector
- **Embedding 模型**:OpenAI text-embedding-3、BGE、Cohere Embed、Voyage
- **Rerank 模型**:Cohere Rerank、BGE Reranker
- **进阶**:HyDE、RAG-Fusion、GraphRAG、Self-RAG、CRAG、Agentic RAG
- **文档处理**:Unstructured、LlamaParse、Docling

### 记忆系统
- 短期记忆(对话历史压缩 / 滑动窗口)
- 长期记忆(向量检索 / 知识图谱 / Mem0)
- 情景记忆 vs 语义记忆

### 多模态
- 视觉理解(GPT-4V、Claude Vision、Qwen-VL)
- 语音(Whisper、TTS)
- Computer Use / Browser Use(Anthropic、Playwright MCP)

## 四、Prompt 工程

- Few-shot / Chain-of-Thought / Tree-of-Thought / ReAct
- Prompt 模板管理:LangSmith、PromptLayer、Helicone
- Structured Output(JSON Mode、XML、Pydantic)
- Prompt Caching(降本利器,Claude / Gemini 已支持)
- Jailbreak 防护、Prompt Injection 防御

## 五、Agent 工程化

### 评估(Evaluation)
- **框架**:Ragas、DeepEval、Promptfoo、Inspect AI、LangSmith Eval
- **指标**:Faithfulness、Context Relevance、Answer Relevance、Hallucination Rate
- **方法**:LLM-as-Judge、人工标注、A/B Testing

### 可观测性(Observability)
- LangSmith、LangFuse、Helicone、Phoenix(Arize)、Weights & Biases
- OpenTelemetry for LLM(OpenLLMetry)
- Token 消耗、延迟、错误率、链路追踪

### 部署与运维
- **推理服务**:FastAPI、LiteLLM、OpenRouter
- **网关**:Portkey、Kong AI Gateway
- **流式输出**:SSE、WebSocket
- **并发控制**:速率限制、队列、降级

### 安全与合规
- PII 脱敏、内容安全(Llama Guard、Azure Content Safety)
- 红队测试(Garak、PyRIT)
- 数据合规(等保、GDPR)

## 六、编程语言与基础

### 必备
- **Python 3.10+**(主力语言)
- 异步编程(asyncio)
- 类型系统(Pydantic、TypedDict)
- 测试(pytest、pytest-asyncio)

### 加分
- **TypeScript / Node.js**(前端 Agent / Anthropic SDK / Vercel AI SDK)
- **Go / Rust**(高性能推理服务、网关)

## 七、基础设施

- **容器**:Docker、Kubernetes
- **消息队列**:Kafka、RabbitMQ、Redis Streams
- **数据库**:PostgreSQL(+ pgvector)、Redis、MongoDB
- **云**:AWS Bedrock、Azure OpenAI、Google Vertex AI、阿里云百炼

## 八、技能等级建议描述

简历中按熟悉程度分级,**不要超过 3-4 个"精通"**:

- **精通**:能讲原理、读过源码、生产落地超过 6 个月、解决过疑难问题
- **熟悉**:用过 3 个月以上、了解核心原理、能独立开发
- **了解**:做过 demo、看过文档、能在指导下使用

## 九、岗位 JD 关键词命中策略

针对不同公司类型,JD 侧重不同:

| 公司类型 | 高频关键词 | 简历策略 |
|---------|-----------|---------|
| 大厂(字节/阿里/腾讯/百度) | 多 Agent、规模化、高并发、Prompt 工程、评估体系 | 突出工程化、规模数字 |
| AI 初创(MiniMax/智谱/月之暗面) | 论文、SOTA、模型微调、Agent 范式创新 | 突出技术深度、开源贡献 |
| 外企(微软/Google/Anthropic) | English、System Design、OSS contribution | 全英文、强调 ownership |
| 应用公司(SaaS/电商) | 业务场景、ROI、客户案例 | 突出业务价值、降本数字 |

## 十、当前(2026)热门方向(加分项)

- **Computer Use / Browser Agent** - Claude Computer Use、Playwright MCP
- **Coding Agent** - Cursor、Cline、Aider、Claude Code、Devin 类
- **Agent 协议** - MCP、A2A(Google Agent2Agent)、AGNTCY
- **强化学习对齐** - RLHF、DPO、Constitutional AI
- **Long Context** - 1M+ token、Context Caching
- **Edge Agent** - 端侧推理(ONNX、CoreML、MLX)
