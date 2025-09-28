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
    system_prompt='You provide real-time cryptocurrency prices and trends.',
)

# Define a tool to fetch Bitcoin price with CoinGecko API
@agent.tool
def get_bitcoin_price(ctx: RunContext) -> str:
    """Fetches the current price of Bitcoin and recent trend."""
    try:
        # Use CoinGecko API to get Bitcoin data for the last 7 days
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=7&interval=daily"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract prices
        prices = data['prices']
        
        # Get the most recent price
        current_price = prices[-1][1]
        
        # Calculate price change percentage over the period
        first_price = prices[0][1]
        price_change = ((current_price - first_price) / first_price) * 100
        
        # Format the response
        trend = "up" if price_change > 0 else "down"
        return f"The current price of Bitcoin is ${current_price:.2f} USD. " \
               f"Over the past week, the price has gone {trend} by {abs(price_change):.2f}%."
    
    except Exception as e:
        # Fallback to mock data when API is unavailable
        return f"Unable to fetch real-time Bitcoin price (Error: {type(e).__name__}). " \
               f"Using sample data: The current price of Bitcoin is $29,876.45 USD."

# Run the Crypto Agent
response = agent.run_sync('What is the current price of Bitcoin?')
print(response.output)