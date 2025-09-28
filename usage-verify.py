import asyncio
import random
from typing import Union
from unittest import result
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunUsage
from pydantic_ai.models.bedrock import BedrockConverseModel
from pydantic_ai.usage import Usage, UsageLimits
from pydantic_ai.messages import ModelMessage
import logfire

logfire.configure()  
logfire.instrument_pydantic_ai() 

model = BedrockConverseModel('anthropic.claude-3-haiku-20240307-v1:0')

class UserDetails(BaseModel):
    name: str
    age: int = Field(ge=1, le=120)
    matric_number: str


class Failed(BaseModel):
    """User failed to provide sufficient details after multiple attempts."""
    
    # Define an agent using Gemini for verification
user_verification_agent = Agent[None, Union[UserDetails, Failed]](
    model=model,
    output_type=Union[UserDetails, Failed],  # type: ignore
    system_prompt=(
        "Extract the user's name, age, and matric number for verification. "
        "If any information is missing or incomplete, request clarification up to three times."
    ),
)

usage_limits = UsageLimits(request_limit=3)  # Limit AI attempts to 3

async def verify_user(usage: RunUsage) -> Union[UserDetails, None]:
    message_history: Union[list[ModelMessage], None] = None

    for i in range(3):
        answer = input("Please provide your name, age, and matric number for verification:")
        print("User's input attempt", i+1, ":", answer)

        result = await user_verification_agent.run(
            answer,
            message_history=message_history,
            usage=usage,
            usage_limits=usage_limits,
        )

        if isinstance(result.output, UserDetails):
            return result.output
        else:
            print("Incomplete details. Please try again.")
            message_history = result.all_messages(
                output_tool_return_content="Ensure you provide your full name, age, and matric number."
            )

    print("Verification failed after multiple attempts. Process terminated.")
    return None

async def main():
    usage: RunUsage = RunUsage()
    user_details = await verify_user(usage)

    if user_details is not None:
        print(f"User verified: {user_details.name}, Age: {user_details.age}, Matric No: {user_details.matric_number}")


# Run the main function if this file is executed
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())