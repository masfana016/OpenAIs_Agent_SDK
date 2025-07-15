### Example 1: Handling a Model Response
from agents import Agent
from .usage import Usage
from openai.types.responses import ResponseOutputMessage, ResponseOutputText

# Initialize an agent
agent = Agent()

from __future__ import annotations
import os
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Usage
from agents.run import RunConfig
import asyncio

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


client = AsyncOpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/",)

model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)

config = RunConfig(model = model,
                   model_provider = client,
                   tracing_disabled = False
                   )

# Mock a model response
response = ModelResponse(
    output=[
        ResponseOutputMessage(content=[ResponseOutputText(text="Hello, world!")])
    ],
    usage=Usage(tokens=15),
    response_id="resp_001"
)

# Convert outputs to inputs for further model calls
input_items = response.to_input_items()
print(input_items)  # [{"content": "Hello, world!", "role": "assistant"}]

# Create a message output item
message_item = MessageOutputItem(agent=agent, raw_item=response.output[0])

# Extract text content
text = ItemHelpers.text_message_output(message_item)
print(text)  # "Hello, world!"

### Example 2: Processing a Tool Call

from openai.types.responses import ResponseFunctionToolCall

# Mock a tool call
tool_call = ResponseFunctionToolCall(call_id="call_001", function="get_weather", arguments={"city": "London"})

# Create a tool call item
tool_item = ToolCallItem(agent=agent, raw_item=tool_call)

# Simulate tool execution and create output
output = "Sunny, 20°C"
tool_output = ItemHelpers.tool_call_output_item(tool_call, output)
tool_output_item = ToolCallOutputItem(agent=agent, raw_item=tool_output, output=output)

# Convert to input item for the model
input_item = tool_output_item.to_input_item()
print(input_item)  # {"call_id": "call_001", "output": "Sunny, 20°C", "type": "function_call_output"}

### Example 3: Handling Multiple Items
# ```python
from . import MessageOutputItem, ItemHelpers

# Mock a list of items
items = [
    MessageOutputItem(agent=agent, raw_item=ResponseOutputMessage(content=[ResponseOutputText(text="Step 1")])),
    MessageOutputItem(agent=agent, raw_item=ResponseOutputMessage(content=[ResponseOutputText(text="Step 2")])),
]

# Extract all text content
all_text = ItemHelpers.text_message_outputs(items)
print(all_text)  # "Step 1Step 2"