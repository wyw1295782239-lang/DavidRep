import sys
import os

# 添加当前项目根目录到 Python 搜索路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from utils.prompt_loader import load_system_prompts
from agent.tools.agent_tools import (rag_summarize, get_weather, get_user_location, get_user_id,
                                     get_current_month, fetch_external_data, fill_context_for_report)


class ReactAgent:
    def __init__(self):
        tools = [rag_summarize, get_weather, get_user_location, get_user_id,
                get_current_month, fetch_external_data, fill_context_for_report]
        
        # 加载系统提示词
        system_prompt = load_system_prompts()
        
        # 创建符合 ReAct 代理要求的提示模板
        template = f"{system_prompt}\n\nYou have access to the following tools:\n\n{{tools}}\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [{{tool_names}}]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin!\n\nQuestion: {{input}}\nThought:{{agent_scratchpad}}"
        
        prompt_template = PromptTemplate(
            input_variables=["agent_scratchpad", "tools", "tool_names", "input"],
            template=template
        )
        
        # 使用 create_react_agent 创建 ReAct 代理
        agent = create_react_agent(
            llm=chat_model,
            tools=tools,
            prompt=prompt_template
        )
        
        # 使用 AgentExecutor 包装代理
        self.agent = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=50,  # 增加迭代次数限制
            max_execution_time=60  # 增加执行时间限制（秒）
        )

    def execute_stream(self, query: str):
        input_dict = {
            "input": query
        }

        # 执行代理并获取结果
        result = self.agent.invoke(input_dict)
        if "output" in result:
            yield result["output"] + "\n"
        else:
            yield str(result) + "\n"


if __name__ == '__main__':
    agent = ReactAgent()

    for chunk in agent.execute_stream("给我生成我的使用报告"):
        print(chunk, end="", flush=True)
