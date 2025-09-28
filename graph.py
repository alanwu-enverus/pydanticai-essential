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
from dataclasses import dataclass, field
from pydantic_graph import BaseNode, Graph, GraphRunContext, End

logfire.configure()  
logfire.instrument_pydantic_ai() 

model = BedrockConverseModel('anthropic.claude-3-haiku-20240307-v1:0')

@dataclass
class State:
    user_name: str = ""
    user_interests: list[str] = field(default_factory=list)
    recommended_articles: list[str] = field(default_factory=list)
    email_content: str = ""
    
@dataclass
class GetUserInfo(BaseNode[State]):
    async def run(self, ctx: GraphRunContext[State]) -> "ProcessUserInfo":
        name = input("Enter your name: ")
        interests = input("Enter your interests (comma-separated): ").split(",")
        
        ctx.state.user_name = name
        ctx.state.user_interests = interests
        
        return ProcessUserInfo()  # Moves to the next step    
    
@dataclass
class ProcessUserInfo(BaseNode[State]):
    async def run(self, ctx: GraphRunContext[State]) -> "GenerateEmail":
        interests = ctx.state.user_interests
        
        # Simulate AI fetching articles
        ctx.state.recommended_articles = [f"Latest news on {topic}" for topic in interests]
        
        return GenerateEmail()    

@dataclass
class GenerateEmail(BaseNode[State]):
    async def run(self, ctx: GraphRunContext[State]) -> "End":
        query = f"Generate a newsletter email content in markdown format for the user name called {ctx.state.user_name} about the following topics: {', '.join(ctx.state.user_interests)}"
        ctx.state.email_content = await article_agent.run(query)
        
        return End(ctx.state.email_content)    
    
class Article(BaseModel):
    title: str
    subtitle: str
    content: str

article_agent = Agent(
    model=model,
    system_prompt='You are a newsletter writer. You have to write a newsletter email for a user about the topics they are interested in.',
    output_type=Article  # Enforcing the structured output
)   

newsletter_graph = Graph(
    nodes=[GetUserInfo, ProcessUserInfo, GenerateEmail]
) 


async def main():
    state = State()
    ctx = GraphRunContext(state=state, deps={})
    result = await newsletter_graph.run(GetUserInfo(), state=state)
    print("Final Email Output:")
    print(result.output)
    # print("Title: ", result.output.title)
    # print("Subtitle: ", result.output.subtitle)
    # print("Content: ", result.output.content)
   

if __name__ == "__main__":
    asyncio.run(main())
    # print("Final Email Output:")
    # # article = Article(result.output)
    # print(result.output)

    