
import asyncio
from unittest import result
from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel

model = BedrockConverseModel('anthropic.claude-3-haiku-20240307-v1:0')
    #     model = BedrockConverseModel('anthropic.claude-3-haiku-20240307-v1:0',
    #                               provider= BedrockProvider(
    #     region_name='us-east-1',
    #     aws_access_key_id='ASIAYZBRV5VUTJ53GIRO',
    #     aws_secret_access_key='uL41WXI73KYDDIGESDfAnJcO9aNeVRY6EX+JHtGk',
    # ),)

async def test_async_agent():
    agent = Agent(
        model,
        system_prompt='You are a helpful assistant specialized in Python programming.')
    result = await agent.run('What are the key features of Pydantic AI in a short response.')
    print("Bedrock Response:")
    print(result.output)



# Stream the story
async def stream_story():
    story_agent = Agent(
    model,
    system_prompt="You are an AI storyteller. Generate engaging, real-time sci-fi adventures."
)
    user_prompt = "Tell me a sci-fi story about a lost spaceship in a short response."
    async with story_agent.run_stream(user_prompt) as response:
        async for part in response.stream_text():
            print(part, end='', flush=True)

if __name__ == "__main__":
    asyncio.run(stream_story())
