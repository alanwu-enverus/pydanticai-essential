import asyncio
import random
from unittest import result
from pydantic_ai import Agent
from pydantic_ai.models.bedrock import BedrockConverseModel
import logfire

logfire.configure()  
logfire.instrument_pydantic_ai() 

model = BedrockConverseModel('anthropic.claude-3-haiku-20240307-v1:0')

# Initialize the agent
agent = Agent(
    model=model,
    system_prompt="You are a fitness coach that suggests personalized workout plans.",
)

# 1. LLM extract the goal
# 2. call the tool to get a workout suggestion
# 3. LLM from the suggestion to form a response with explanation
# it sees from comment of tool function, it can guild the LLM to do the function steps?? 
@agent.tool_plain
def suggest_workout(goal: str) -> str:
    """Suggests a workout based on the user's fitness goal."""
    workouts = {
        "strength": ["Deadlifts", "Squats", "Bench Press"],
        "cardio": ["Running", "Cycling", "Jump Rope"],
        "flexibility": ["Yoga", "Dynamic Stretching", "Pilates"],
    }
    
    # Check for partial matches in the goal
    for key in workouts:
        if key in goal.lower():
            return f"Try this workout for {key}: {random.choice(workouts[key])}"
    
    return f"Try this workout: {random.choice(['Rest Day', 'Walking', 'Light Stretching'])}"

# Run the agent
result = agent.run_sync('I want a workout for strength training.')
print(result.output)