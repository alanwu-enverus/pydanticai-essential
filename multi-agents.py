import asyncio
import random
from unittest import result
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.bedrock import BedrockConverseModel
import logfire
import requests

logfire.configure()  
logfire.instrument_pydantic_ai() 

model = BedrockConverseModel('anthropic.claude-3-haiku-20240307-v1:0')

ceo_agent = Agent(
    model=model,
    # The system prompt is so important for this kind of multi-agent collaboration. You need to specify what are the tools available to the agents and what are the constraints.
    system_prompt="You are the CEO of a tech startup. Based on user input, decide whether the Marketing, Finance, or Tech Lead should handle the task. then call to the `assign_task` tool to delegate the task."
)

# Marketing Agent - Creates ad campaigns
marketing_agent = Agent(
    model=model,
    system_prompt="You are a marketing expert. Generate creative ad campaigns."
)

# Finance Agent - Manages budgets
finance_agent = Agent(
    model=model,
    system_prompt="You are a financial expert. Handle budgets and financial planning."
)

# Tech Lead Agent - Handles product development
tech_agent = Agent(
    model=model,
    system_prompt="You are the tech lead. Guide product development and fix technical issues."
)

# CEO assigns tasks
@ceo_agent.tool
async def assign_task(ctx: RunContext, task: str, assignee: str = None) -> str:
    """Delegates tasks to the appropriate agent and returns their response in a detailed format.
    
    Args:
        task: The task to be completed
        assignee: Optional - The team member to assign (Marketing, Finance, or Tech)
    """
    # Determine which agent to use based on assignee or task content
    if assignee and "market" in assignee.lower() or "marketing" in task.lower():
        r = await marketing_agent.run(task)
        print("Marketing Agent's response:", r.output)
        return r.output
    elif assignee and "finance" in assignee.lower() or "budget" in task.lower() or "finance" in task.lower():
        r = await finance_agent.run(task)
        print("Finance Agent's response:", r.output)
        return r.output
    elif assignee and "tech" in assignee.lower() or "tech" in task.lower() or "product" in task.lower():
        r = await tech_agent.run(task)
        print("Tech Lead Agent's response:", r.output)
        return r.output
    else:
        return "I don't recognize this task or assignee."

response =  ceo_agent.run_sync("Create a marketing campaign for our new AI app.")
print("CEO's response:", response.output)
# async def main():
#     # Test the Marketing Campaign
#     # response = await ceo_agent.run("Create a marketing campaign for our new AI app.")
#     response = await ceo_agent.run("Create a marketing campaign for our new AI app.")
    

# #     # Test the Financial Plan
# #     # response = await ceo_agent.run("Create a marketing campaign for our new AI app.")
# #     response = await ceo_agent.run("Create a financial plan for our new AI app.")
# #     print("CEO's response:", response.output)

# #     # Test the Tech Lead Task
# #     # response = await ceo_agent.run("Create a marketing campaign for our new AI app.")
# #     response = await ceo_agent.run("Develop a prototype for our new AI app.")
# #     print("CEO's response:", response.output)
# # # Test the AI Startup Team
# # # response = await ceo_agent.run("Create a marketing campaign for our new AI app.")
# #     response = await ceo_agent.run("Create a financial plan for our new AI app.")
# #     print("CEO's response:", response.output)
# if __name__ == "__main__":
#     asyncio.run(main())
#     print("CEO's response:", response.output)