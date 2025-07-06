import os
from dotenv import load_dotenv
from dataclasses import dataclass
from agents import Agent, Runner, AsyncOpenAI, ModelSettings, OpenAIChatCompletionsModel, function_tool, RunContextWrapper
from agents.run import RunConfig
from pydantic import BaseModel
import asyncio

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


client = AsyncOpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/",)

model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

config = RunConfig(model = model,
                   model_provider = client,
                   tracing_disabled = True
                   )

@function_tool
def get_weather_tool():
    return ("FAisalabad weather is sunny!")

agent = Agent(
    name = "Weather agent",
    instructions="You're a weather bot.",
    tools=[get_weather_tool],
    model = model
)

input = "What is tomorow's weather?"

# Only allow 1 turn
async def main():
    result = await Runner.run(
        starting_agent=agent,
        input=input,
        max_turns=2,  # Allow for more complex interactions
        run_config = config
    )
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())