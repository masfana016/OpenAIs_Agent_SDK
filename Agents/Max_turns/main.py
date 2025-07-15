import os
from dotenv import load_dotenv
from dataclasses import dataclass
from agents import Agent, Runner, AsyncOpenAI, ModelSettings, OpenAIChatCompletionsModel, function_tool, RunContextWrapper, RunHooks, trace
from agents.run import RunConfig
from pydantic import BaseModel
import asyncio

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


client = AsyncOpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/",)

model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

config = RunConfig(model = model,
                   model_provider = client,
                   tracing_disabled = False,
                   workflow_name = "Max Turns Test",
                   trace_metadata = {"test_type": "max_turns_behavior"}
                   )

@function_tool
def get_weather_tool():
    return ("FAisalabad weather is sunny!")

@function_tool
def get_time_tool():
    return ("Current time is 3:45 PM!")

@function_tool
def get_date_tool():
    return ("Today's date is December 15, 2024!")

@function_tool
def get_user_id():
    return ("User ID is 1234")

class TracingHooks(RunHooks):
    def __init__(self):
        self.turn_count = 0
        self.current_turn = 0
        
    async def on_agent_start(self, context, agent):
        self.current_turn += 1
        print(f"🔄 Turn {self.current_turn}: Agent '{agent.name}' started")
        
    async def on_tool_start(self, context, agent, tool):
        print(f"🔧 Turn {self.current_turn}: Tool '{tool.name}' started")
        
    async def on_tool_end(self, context, agent, tool, result):
        print(f"✅ Turn {self.current_turn}: Tool '{tool.name}' completed with result: {result}")
        
    async def on_agent_end(self, context, agent, output):
        print(f"🏁 Turn {self.current_turn}: Agent '{agent.name}' ended with output: {output}")
        self.turn_count = self.current_turn

hooks = TracingHooks()

agent = Agent(
    name = "Multi-tool agent",
    instructions="You are a helpful assistant that can provide weather, time, date, and user information. When asked for multiple pieces of information, use tools one at a time on separate turns. Use the appropriate tool for each piece of information requested.",
    tools=[get_weather_tool, get_time_tool, get_date_tool],
    # model_settings = ModelSettings(parallel_tool_calls=True), #  'Error_message': 'Parallel tool calls are not supported.
    # model_settings = ModelSettings(parallel_tool_calls=False),
    model = model
)

input = "What is the weather, current time, today's date, and give me user details? Please use tools to get each piece of information separately."

# Test with max_turns=3 to see what happens when agent tries to use tool on turn 3
async def main():
    print("=== Starting Max Turns Test ===")
    print(f"Input: {input}")
    print(f"Max turns: 3")
    print("=" * 50)
    
    try:
        with trace(workflow_name="Max Turns Test", group_id="test_session_001"):
            result = await Runner.run(
                starting_agent=agent,
                input=input,
                max_turns=3,  # Allow exactly 3 turns - test what happens on turn 3
                run_config = config,
                hooks = hooks
            )
        print("\n=== Results ===")
        print("Final output:", result.final_output)
        print("Total turns used:", len(result.raw_responses))
        print("Raw responses count:", len(result.raw_responses))
        print("New items count:", len(result.new_items))
        print("Hooks turn count:", hooks.turn_count)
        
        # Show what happened in each turn
        print("\n=== Turn-by-Turn Analysis ===")
        for i, response in enumerate(result.raw_responses, 1):
            print(f"\n📋 Turn {i} Details:")
            print(f"  Response type: {type(response)}")
            if hasattr(response, 'content') and response.content:
                print(f"  Content: {response.content}")
            if hasattr(response, 'tool_calls') and response.tool_calls:
                print(f"  Tool calls: {len(response.tool_calls)}")
                for tool_call in response.tool_calls:
                    print(f"    - {tool_call.function.name}")
            else:
                print(f"  Tool calls: None")
                    
    except Exception as e:
        print(f"\n=== Exception Occurred ===")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {e}")
        print(f"Traceback:")
        import traceback
        traceback.print_exc()
    
if __name__ == "__main__":
    asyncio.run(main())