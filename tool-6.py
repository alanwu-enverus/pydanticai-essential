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
    system_prompt='You recommend restaurants based on user preferences.',
)

# Tool to suggest a type of cuisine
@agent.tool_plain
def suggest_cuisine() -> str:
    """Suggests a random cuisine to try."""
    cuisines = ["Italian", "Japanese", "Mexican", "Indian", "Thai"]
    return random.choice(cuisines)

# Tool to fetch restaurants (simulating API response)
@agent.tool_plain
def find_restaurant(cuisine: str) -> str:
    """Finds a restaurant serving the specified cuisine."""
    restaurants = {
        "Italian": ["Pasta Heaven", "Luigi's Pizza"],
        "Japanese": ["Sushi World", "Ramen House"],
        "Mexican": ["Taco Land", "Burrito King"],
        "Indian": ["Spice Bazaar", "Curry Express"],
        "Thai": ["Bangkok Bites", "Thai Delight"],
    }
    return f"Try {random.choice(restaurants.get(cuisine, ['No options available']))} for {cuisine} food!"

# Run the agent
cuisine = suggest_cuisine()  # Get a random cuisine
result = find_restaurant(cuisine)  # Find a restaurant
print(f"{cuisine} cuisine → {result}")