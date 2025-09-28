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

# Initialize the agent
agent = Agent(
    model=model,
    system_prompt='You are a finance assistant that helps track expenses.',
)


# Define a tool with dependency injection
@agent.tool
def add_expense(ctx: RunContext[dict], category: str, amount: float) -> str:
    # """Stores a user's expense in the system if not existing."""
    """Stores a user's expense in the system """
    ctx.deps['expenses'].append({'category': category, 'amount': amount})
    return f"Added {amount} to {category} expenses."

# Initialize dependencies (storage for expenses)
dependencies = {'expenses': []}
# dependencies = {'expenses': [{'category': 'food', 'amount': 50.0}, {'category': 'transport', 'amount': 30.0}]}

def main():
# Run the agent
    agent.run_sync('Add 50 to food expenses.', deps=dependencies)
    agent.run_sync('Add 99 to water expenses.', deps=dependencies)

    # Print stored expenses
   

if __name__ == "__main__":
    main() 
    print(dependencies['expenses'])