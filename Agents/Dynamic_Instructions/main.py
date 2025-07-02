import asyncio
import os
from dotenv import load_dotenv
import random
# from dataclasses import dataclass
from typing import Literal
from agents import Agent, Runner, AsyncOpenAI, ModelSettings, OpenAIChatCompletionsModel, RunContextWrapper
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

# @dataclass
class CustomContext:
    def __init__(self, style: Literal["haiku", "pirate", "robot", "None"]):
        self.style = style


def custom_instructions(
    run_context: RunContextWrapper[CustomContext], agent: Agent[CustomContext]
) -> str:
    context = run_context.context
    if context.style == "haiku":
        return "Only respond in haikus."
    elif context.style == "pirate":
        return "Respond as a pirate."
    elif context.style == "robot":
        return "Respond as a robot."
    else:
        return "Respond as a Normal human and say 'beep boop' a lot."


agent = Agent(
    name="Chat agent",
    instructions=custom_instructions,
    model = model
)

history = []

async def main():
    
    while True:
        choice: Literal["haiku", "pirate", "robot", "None"] = random.choice(["haiku", "pirate", "robot", "None"])
        context = CustomContext(style=choice)
        print(f"Using style: {choice}\n")

        user_message = input("Tell me what you want?: ")
        print(f"User: {user_message}")
        
        history.append({"role": "user", "content": user_message})
        result = await Runner.run(agent, history, context=context, run_config=config)

        print(f"Assistant: {result.to_input_list()[-1]['content'][0]['text'].strip()}")


if __name__ == "__main__":
    asyncio.run(main())

"""
$ python examples/basic/dynamic_system_prompt.py

Using style: haiku

User: Tell me a joke.
Assistant: Why don't eggs tell jokes?
They might crack each other's shells,
leaving yolk on face.

$ python examples/basic/dynamic_system_prompt.py
Using style: robot

User: Tell me a joke.
Assistant: Beep boop! Why was the robot so bad at soccer? Beep boop... because it kept kicking up a debug! Beep boop!

$ python examples/basic/dynamic_system_prompt.py
Using style: pirate

User: Tell me a joke.
Assistant: Why did the pirate go to school?

To improve his arrr-ticulation! Har har har! 🏴‍☠️
"""