import asyncio
import random
from unittest import result
from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel
import logfire
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool

logfire.configure()  
logfire.instrument_pydantic_ai() 

model = BedrockConverseModel('anthropic.claude-3-haiku-20240307-v1:0')

agent = Agent(
    model=model,
    tools=[duckduckgo_search_tool()],
    system_prompt="Search DuckDuckGo for the given query and return the results.",
)

# Run the agent with a query
result = agent.run_sync('What is the current President of Malaysia?')
print(result.output)