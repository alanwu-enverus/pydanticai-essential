import asyncio
from unittest import result
from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel

model = BedrockConverseModel('anthropic.claude-3-haiku-20240307-v1:0')

def stateless_call():
    agent = Agent(
        model,
        system_prompt='You are an assistant that provides general information.')
    user_query = 'What is the capital of France?'
    result = agent.run_sync(user_query)
    print("Bedrock Response:")
    print(result.output)
    
def stateful_call():
    stateful_agent = Agent(
    model,
    system_prompt='You are a conversational assistant.',
    )

    # Initial user query
    initial_query = 'Tell me about the Eiffel Tower in a short response.'

    # Run the agent synchronously
    initial_response = stateful_agent.run_sync(initial_query)
    print(initial_response.output)
    # Output: 'The Eiffel Tower is a wrought-iron lattice tower in Paris, France.'

    # Follow-up query
    follow_up_query = 'How tall is it?'

    # Run the agent with the follow-up query
    follow_up_response = stateful_agent.run_sync(follow_up_query, message_history=initial_response.new_messages())
    print(follow_up_response.output)    
    
if __name__ == "__main__":
    stateful_call()    