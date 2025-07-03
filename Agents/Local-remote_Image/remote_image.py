import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, ModelSettings, OpenAIChatCompletionsModel
from agents.run import RunConfig

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


client = AsyncOpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/",)

model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

config = RunConfig(model = model,
                   model_provider = client,
                   tracing_disabled = True
                   )

URL = "https://upload.wikimedia.org/wikipedia/commons/b/b6/Image_created_with_a_mobile_phone.png"


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        model = model
    )

    result = await Runner.run(
        agent,
        [
            {
                "role": "user",
                "content": [{"type": "input_image", "detail": "auto", "image_url": URL}],
            },
            {
                "role": "user",
                "content": "What do you see in this image?",
            },
        ],
        run_config = config
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())