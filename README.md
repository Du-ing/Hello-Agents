# Hello-Agents

一个用于学习和实验多种 Agent 模式与本地/远程 LLM 联动示例的示范项目。

本仓库收集了若干示例智能体实现（ReAct、Plan-and-Solve、城市旅游助手、本地模型对话等），便于学习智能体设计、工具调用与 prompt 组织方式。

**主要特性**
- 多种智能体范式示例：Planning+Execution（`my_agent`）、ReAct（`my_agent`）、任务导向代理（`city_travel_agent`）等。
- 集成远程兼容 OpenAI 接口的客户端示例（`city_travel_agent/llm_client.py`、`my_agent/llm_client.py`）。
- 本地模型演示（`local_llm/chat.py`）：使用 transformers 加载本地权重并进行简单对话。
- 多个子目录示例：AutoGen、CAMEL、LangGraph 等用于不同实验场景。

**仓库结构（简要）**
- `AutoGen/`：自动化代理示例，包含 `agent_prompt.py`、`autogen_software_team.py` 等。
- `CAMEL/`：基于 CAMEL 思路的写作/多轮示例（`book_writing.py`）。
- `city_travel_agent/`：城市旅游场景示例，带有系统 prompt、工具（景点检索、天气）和示例入口 `main.py`。
- `LangGraph/`：对话系统相关示例（`dialog_system.py`）。
- `local_llm/`：本地模型加载与交互示例（`chat.py`、`download.py`）。
- `my_agent/`：核心学习示例，包含 `plan_and_solve_agent.py`（规划+执行）、`react_agent.py`（ReAct）、工具与 client 示例。

安装与依赖
---------------

建议使用 Python 3.8+ 创建虚拟环境并按需要安装子模块依赖。

示例（在 macOS / Linux 环境）：

```bash
python3 -m venv .venv
source .venv/bin/activate
# 每个子目录通常含有自己的 requirements.txt，请根据需要安装，例如：
pip install -r my_agent/requirements.txt
pip install -r city_travel_agent/requirements.txt
pip install -r local_llm/requirements.txt
```

注意：仓库中并非每个子目录都必须安装其依赖；仅运行对应示例时再安装相应依赖即可。

运行示例
-----------

1) 城市旅游助手（远程 LLM 示例）

- 编辑 `city_travel_agent/main.py` 中的 `API_KEY` / `BASE_URL` 或将凭证通过环境变量注入（示例文件内有 TODO 注记）。
- 运行：

```bash
python3 city_travel_agent/main.py
```

该脚本展示了如何把工具（天气、景点检索）作为调用项交给 LLM，由 LLM 选择并调用工具完成任务。

2) Planning + Execute 智能体（`my_agent/plan_and_solve_agent.py`）

- 运行：

```bash
python3 my_agent/plan_and_solve_agent.py
```

该示例展示了如何用一个 Planner 生成分步骤计划，并用 Executor 逐步调用 LLM 完成每一步。注意该模块依赖仓内 `my_agent/llm_client.py` 的实现和本地/远程模型凭证配置。

3) ReAct 智能体（`my_agent/react_agent.py`）

- 运行：

```bash
python3 my_agent/react_agent.py
```

脚本内示例演示如何注册工具（例如 `Search`），并在循环中解析 LLM 输出的 Thought/Action，执行工具并将 Observation 返回给 LLM。

4) 本地 LLM 对话（`local_llm/chat.py`）

- 在脚本内设置 `model_id` 为本地模型路径（例如 Qwen 权重目录），确保 `transformers` 支持该模型并安装好所需依赖。运行：

```bash
python3 local_llm/chat.py
```

安全与凭证
-------------

- 仓库中示例文件可能包含占位的 API_KEY 或示例值，请勿提交真实凭证到版本控制。建议使用环境变量或密钥管理方案。
- 本地模型示例需要较大磁盘与内存资源，请先确认硬件与 CUDA 环境（如使用 GPU）。

如何贡献
-----------

- 欢迎提交 PR：增加新 agent 模式、改进现有 prompt、补充更多使用说明或测试用例。
- 请在 PR 中描述复现步骤与依赖，避免将模型权重或私密凭证提交到仓库。

常见问题
-----------
- 如果运行示例时报错找不到依赖，先确认已激活虚拟环境并安装对应 `requirements.txt`。
- 本地模型加载若出现 CUDA/显存问题，可切换 `local_llm/chat.py` 中 `device` 为 `cpu`（性能会下降但更节省显存）。

更多
-----
如果你希望我为某个子模块生成更详细的文档（例如 `AutoGen` 的使用示例，或把所有子模块的 `requirements.txt` 汇总为一个整体安装脚本），请告诉我想要优先完善的部分。

---
更新自：代码静态分析（提取自项目中 `my_agent/`, `city_travel_agent/`, `local_llm/`, `AutoGen/`, `CAMEL/` 等示例脚本）。