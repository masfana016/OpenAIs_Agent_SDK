import asyncio
import base64
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


FILEPATH = os.path.join(os.path.dirname(__file__), "media/image_bison.jpeg")


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


async def main():
    # Print base64-encoded image
    b64_image = image_to_base64(FILEPATH)

    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        model = model
    )
    
    while True:

        result = await Runner.run(
            agent,
            [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_image",
                            "detail": "auto",
                            "image_url": f"data:image/jpeg;base64,{b64_image}",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": input("What do you see in this image? "),
                },
            ],
            run_config = config
        )
        print(result.to_input_list()[-1]['content'][0]['text'].strip())


if __name__ == "__main__":
    asyncio.run(main())