import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")



client = AsyncOpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/",)

model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

config = RunConfig(model = model,
                   model_provider = client,
                   tracing_disabled = True
                   )

agent = Agent(name="My Agent", instructions="You are a helpful assistant that can answer questions and help with tasks.", model = model)

history = []

async def main():
    while True:

        user_input = input ("How may I help you today: " )
        
        history.append({"role": "user", "content": user_input})
        
        result = await Runner.run(agent, input = history, run_config = config)
        
        print(f"Response: ", result.to_input_list()[-1]['content'][0]['text'].strip())
  
        ##### 1st Method
        # --------------------------------------------------------------------------
        # # Get the input list
        
        # inputs = result.to_input_list()

        # # Find the last assistant message
        # latest_assistant_msg = next(
        #     (item for item in reversed(inputs) if item.get('role') == 'assistant'), 
        #     None
        # )

        # # Extract and print only the assistant's latest response
        # if latest_assistant_msg:
        #     assistant_texts = [block['text'] for block in latest_assistant_msg['content'] if block['type'] == 'output_text']
        #     print("Response:", ''.join(assistant_texts).strip())
        # else:
        #     print("No assistant response found.")
        ########### 2nd Method
        # --------------------------------------------------------------------------
        # inputs = result.to_input_list()
        # assistant_msg = next((m for m in reversed(inputs) if m.get('role') == 'assistant'), None)
        # if assistant_msg:
        #     print("Response:", assistant_msg['content'][0]['text'].strip())
        # else:
        #     print("No assistant message found.")

        

if __name__ == "__main__":
    asyncio.run(main())









