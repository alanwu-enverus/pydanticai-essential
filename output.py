import asyncio
from unittest import result
from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel

from pydantic import BaseModel
from typing import List

# Define a Pydantic model for a single dictionary tip
class DictionaryTip(BaseModel):
    title: str
    description: str
    code_example: str

# Define a Pydantic model for multiple dictionary tips
class DictionaryTips(BaseModel):
    tips: List[DictionaryTip]

model = BedrockConverseModel('anthropic.claude-3-haiku-20240307-v1:0')

agent = Agent(
    model=model,
    system_prompt='You are a Python expert providing tips on dictionary usage.',
    output_type=DictionaryTips  # Enforcing the structured output
)

# User query
query = 'Provide three tips for using Python dictionaries effectively.'

# Run the agent synchronously
response = agent.run_sync(query)

# Access the structured data
for tip in response.output.tips:
    print(f"Title: {tip.title}")
    print(f"Description: {tip.description}")
    print(f"Code Example:\n{tip.code_example}\n")