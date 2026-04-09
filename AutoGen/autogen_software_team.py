import os
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from agent_prompt import PRODUCT_MANAGER, ENGINEER, CODE_REVIEWER, USERPROXY
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def create_openai_model_client():
    """创建并配置 OpenAI 模型客户端"""
    return OpenAIChatCompletionClient(
        model=os.getenv("LLM_MODEL_ID"),
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL"),
        # timeout=int(os.getenv("LLM_TIMEOUT", 60)),
        model_info={
            "vision": False,  # 启用视觉输入支持
            "function_calling": True,  # 启用函数调用支持，便于工具集成和自动化执行
            "json_output": True,  # 启用JSON格式输出，便于结构化解析
            "family": os.getenv("LLM_MODEL_ID"),  # 指定模型家族，便于后续替换和升级
            "structured_output": True,  # 启用结构化输出，便于智能体之间的信息传递和协作
            "multiple_system_messages": True,  # 允许多个系统消息，便于不同角色的系统指令配置
        }
    )

def create_product_manager(model_client):
    """创建产品经理智能体"""
    return AssistantAgent(
        name="ProductManager",
        model_client=model_client,
        system_message=PRODUCT_MANAGER,
    )

def create_engineer(model_client):
    """创建软件工程师智能体"""
    return AssistantAgent(
        name="Engineer",
        model_client=model_client,
        system_message=ENGINEER,
    )

def create_code_reviewer(model_client):
    """创建代码审查员智能体"""
    return AssistantAgent(
        name="CodeReviewer",
        model_client=model_client,
        system_message=CODE_REVIEWER,
    )

def create_user_proxy():
    """创建用户代理智能体"""
    return UserProxyAgent(
        name="UserProxy",
        description=USERPROXY,
    )

def create_software_team_chat(product_manager, engineer, code_reviewer, user_proxy):
    """定义团队聊天和协作规则"""
    team_chat = RoundRobinGroupChat(
        participants=[
            product_manager,
            engineer,
            code_reviewer,
            user_proxy
        ],
        termination_condition=TextMentionTermination("TERMINATE"),
        max_turns=20,
    )
    return team_chat

async def run_software_development_team():
    # 初始化客户端和智能体
    llm_client = create_openai_model_client()

    product_manager = create_product_manager(llm_client)
    engineer = create_engineer(llm_client)
    code_reviewer = create_code_reviewer(llm_client)
    user_proxy = create_user_proxy()

    team_chat = create_software_team_chat(
        product_manager,
        engineer,
        code_reviewer,
        user_proxy
    )
    # 定义任务描述
    task = """我们需要开发一个比特币价格显示应用，具体要求如下：
            核心功能：
            - 实时显示比特币当前价格（USD）
            - 显示24小时价格变化趋势（涨跌幅和涨跌额）
            - 提供价格刷新功能

            技术要求：
            - 使用 Streamlit 框架创建 Web 应用
            - 界面简洁美观，用户友好
            - 添加适当的错误处理和加载状态

            请团队协作完成这个任务，从需求分析到最终实现。"""
    
    # 异步执行团队协作，并流式输出对话过程
    result = await Console(team_chat.run_stream(task=task))
    print("\n" + "=" * 60)
    print("✅ 团队协作完成！")
    return result


# 主程序入口
if __name__ == "__main__":
    try:
        # 运行异步协作流程
        result = asyncio.run(run_software_development_team())
        
        print(f"\n📋 协作结果摘要：")
        print(f"- 参与智能体数量：4个")
        print(f"- 任务完成状态：{'成功' if result else '需要进一步处理'}")
        
    except ValueError as e:
        print(f"❌ 配置错误：{e}")
        print("请检查 .env 文件中的配置是否正确")
    except Exception as e:
        print(f"❌ 运行错误：{e}")
        import traceback
        traceback.print_exc()
