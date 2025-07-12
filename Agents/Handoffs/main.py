from __future__ import annotations
import json
import random
import os
from dotenv import load_dotenv
from agents import Agent, HandoffInputData, Runner, function_tool, handoff, trace, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.extensions import handoff_filters
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


@function_tool
def random_number_tool(max: int) -> int:
    """Return a random integer between 0 and the given maximum."""
    return random.randint(0, max)


def spanish_handoff_message_filter(handoff_message_data: HandoffInputData) -> HandoffInputData:
    # Summarize the input_history
    history = handoff_message_data.input_history
    summary = []

    # Create a summary of the conversation
    for message in history:
        if isinstance(message, dict) and "content" in message and "role" in message:
            if message["role"] == "user":
                summary.append(f"User: {message['content']}")
            elif message["role"] == "assistant":
                # Extract text from assistant's content if it's a list with 'text' field
                content = message["content"]
                if isinstance(content, list) and len(content) > 0 and "text" in content[0]:
                    summary.append(f"Assistant: {content[0]['text']}")
                elif isinstance(content, str):
                    summary.append(f"Assistant: {content}")

    # Combine summary into a single string
    summary_text = "Summary: " + " | ".join(summary) if summary else "No relevant history."

    # Replace input_history with the summary as a single message
    summarized_history = [{"role": "system", "content": summary_text}]

    # Create the new HandoffInputData object
    result = HandoffInputData(
        input_history=tuple(summarized_history),
        pre_handoff_items=tuple(handoff_message_data.pre_handoff_items),
        new_items=tuple(handoff_message_data.new_items),
    )

# Convert new_items to a JSON-serializable format for printing
    serializable_new_items = []
    for item in handoff_message_data.new_items:
        if hasattr(item, '__dict__'):  # Check if item is a custom object
            # Convert HandoffCallItem to a dictionary with relevant fields
            serializable_item = {
                "content": getattr(item, "content", None),
                "role": getattr(item, "role", None),
                # Add other relevant fields if needed
            }
            serializable_new_items.append(serializable_item)
        else:
            serializable_new_items.append(item)

    # Print the contents for debugging
    print("\n=== HandoffInputData Contents ===")
    print("input_history:", json.dumps(summarized_history, indent=2))
    print("pre_handoff_items:", json.dumps(handoff_message_data.pre_handoff_items, indent=2))
    print("new_items:", json.dumps(serializable_new_items, indent=2))

    return result


first_agent = Agent(
    name="Assistant",
    instructions="Be extremely concise.",
    tools=[random_number_tool],
    model = model
)

spanish_agent = Agent(
    name="Spanish Assistant",
    instructions="You only speak Spanish and are extremely concise.",
    handoff_description="A Spanish-speaking assistant.",
)

second_agent = Agent(
    name="Assistant",
    instructions=(
        "Be a helpful assistant. If the user speaks Spanish, handoff to the Spanish assistant."
    ),
    handoffs=[handoff(spanish_agent, input_filter=spanish_handoff_message_filter)],
    model = model
)


async def main():

    result = await Runner.run(first_agent, input="Hi, my name is Sora.", run_config = config)

    print("Step 1 done")

        # 2. Ask it to generate a number
    result = await Runner.run(
            first_agent,
            input=result.to_input_list()
            + [{"content": "Can you generate a random number between 0 and 100?", "role": "user"}],
            run_config = config
        )

    print("Step 2 done")

        # 4. Cause a handoff to occur
    result = await Runner.run(
            second_agent,
            input=result.to_input_list()
            + [
                {
                    "content": "Por favor habla en español. ¿Cuál es mi nombre y dónde vivo?",
                    "role": "user",
                }
            ],
            run_config = config
        )

    print("Step 4 done")

    print("\n===Final messages===\n")

    # 5. That should have caused spanish_handoff_message_filter to be called, which means the
    # output should be missing the first two messages, and have no tool calls.
    # Let's print the messages to see what happened
    for message in result.to_input_list():
        print(json.dumps(message, indent=2))
        # tool_calls = message.tool_calls if isinstance(message, AssistantMessage) else None

        # print(f"{message.role}: {message.content}\n  - Tool calls: {tool_calls or 'None'}")
    """
        $python examples/handoffs/message_filter.py
        Step 1 done
        Step 2 done
        Step 3 done
        Step 4 done

        ===Final messages===

        {
            "content": "Can you generate a random number between 0 and 100?",
            "role": "user"
        }
        {
        "id": "...",
        "content": [
            {
            "annotations": [],
            "text": "Sure! Here's a random number between 0 and 100: **42**.",
            "type": "output_text"
            }
        ],
        "role": "assistant",
        "status": "completed",
        "type": "message"
        }
        {
        "content": "I live in New York City. Whats the population of the city?",
        "role": "user"
        }
        {
        "id": "...",
        "content": [
            {
            "annotations": [],
            "text": "As of the most recent estimates, the population of New York City is approximately 8.6 million people. However, this number is constantly changing due to various factors such as migration and birth rates. For the latest and most accurate information, it's always a good idea to check the official data from sources like the U.S. Census Bureau.",
            "type": "output_text"
            }
        ],
        "role": "assistant",
        "status": "completed",
        "type": "message"
        }
        {
        "content": "Por favor habla en espa\u00f1ol. \u00bfCu\u00e1l es mi nombre y d\u00f3nde vivo?",
        "role": "user"
        }
        {
        "id": "...",
        "content": [
            {
            "annotations": [],
            "text": "No tengo acceso a esa informaci\u00f3n personal, solo s\u00e9 lo que me has contado: vives en Nueva York.",
            "type": "output_text"
            }
        ],
        "role": "assistant",
        "status": "completed",
        "type": "message"
        }
    """


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())