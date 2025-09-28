import asyncio
import random
from unittest import result
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.bedrock import BedrockConverseModel
import logfire

logfire.configure()  
logfire.instrument_pydantic_ai() 

model = BedrockConverseModel('anthropic.claude-3-haiku-20240307-v1:0')

# Initialize the agent
agent = Agent(
    model=model,
    system_prompt='You provide exchange rate information to users.',
)

# Define a custom tool with dependency injection
@agent.tool
def get_exchange_rate(ctx: RunContext[dict], currency: str) -> str:
    """Fetch the exchange rate for a given currency."""
    exchange_rates = ctx.deps['exchange_rates']
    rate = exchange_rates.get(currency.upper(), 'unknown')
    return f"The exchange rate for {currency.upper()} is {rate}."

# Dependency data
dependencies = {
    'exchange_rates': {
        'USD': '1.00',
        'EUR': '0.85',
        'JPY': '110.00',
    }
}

# Run the agent with a user query
result = agent.run_sync('What is the exchange rate for EUR?', deps=dependencies)
print(result.output)