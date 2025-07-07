# Agent Runner

A Python library for running AI agents with flexible control over asynchronous, synchronous, and streaming execution, using large language models (LLMs).

## Overview

The Agent Runner Library enables you to run AI agents that process inputs, call LLMs, execute tools, and handle handoffs between agents. It supports single-turn and multi-turn conversations with customizable configurations.

## Usage

### Running an Agent

Use the `Runner` class to execute agents with one of three methods:

- **`Runner.run()`**: Asynchronous, returns a `RunResult` with inputs, guardrail results, and final output. Ideal for async environments like FastAPI.
- **`Runner.run_sync()`**: Synchronous, wraps around an asynchronous `run()` method (but waits for it to finish) — and it starts a new event loop internally.  it will not work if there's already an event loop (e.g. inside an async function, or in a Jupyter notebook or async context like FastAPI).
- **`Runner.run_streamed()`**: Asynchronous, streams events (e.g., partial outputs) and returns a `RunResultStreaming`object  with a `.stream_events()` method to recieve sementic events for real-time applications.

> ***Semantic events*** are meaningful updates or actions (e.g., partial outputs, tool calls, or handoffs) generated during an agent's execution, which can be streamed in real-time using `Runner.run_streamed()` to track the workflow's progress.

Example:
```python
from agents import Agent, Runner

async def main():
    agent = Agent(name="Assistant", instructions="You are a helpful assistant")
    result = await Runner.run(agent, "Write a haiku about recursion.")
    print(result.final_output)
    # Code within the code,
    # Functions calling themselves,
    # Infinite loop's dance.
```

### Agent Loop

All run methods follow the same loop:
1. The agent processes the input using the LLM (The agent is invoked with the given input.).
2. If a final output (text matching `agent.output_type`, no tool calls) is produced, the loop stops (terminates).
3. If a handoff occurs, the loop continues with the new agent (next turn) and updated input.
4. If tools are called, they run, results are appended, and the loop continues (next turn).
5. The loop stops (or raise an exception) if:
   - A final output is produced.
   - The `max_turns` limit is exceeded (raises `MaxTurnsExceeded`).
   - A guardrail is triggered (raises `GuardrailTripwireTriggered`).

Only the first agent’s input guardrails are applied.

### Parameters

- `starting_agent`: The initial agent to run.
- `input`: A string (user message) or list of messages (e.g., OpenAI Responses API format).
- `context`: Optional context for the agent.
- `max_turns`: Limits loop iterations (default: `DEFAULT_MAX_TURNS`).
- `hooks`: Callbacks for lifecycle events (e.g., start/end of run).
- `run_config`: Global settings (see below).
- `previous_response_id`: Optional ID for OpenAI Responses API to skip prior inputs.

### Streaming

Stream events as the LLM processes:
```python
async def main():
    agent = Agent(name="Assistant", instructions="Reply concisely.")
    result = await Runner.run_streamed(agent, "What's 2+2?")
    async for event in result.stream_events():
        print(event)
```

### Run Configuration

Customize runs with the `RunConfig` dataclass:
- `model`: The model to use for the entire agent run. If set, will override the model set on every agent.
- `model_provider`: Specifies the provider (defaults to OpenAI).
- `model_settings`: Overrides agent-specific settings (e.g., temperature, top_p).
- `handoff_input_filter`: Filters inputs during handoffs (unless specified by the handoff).
- `input_guardrails`: Filters initial input.
- `output_guardrails`: Filters final output.
- `tracing_disabled`: Disables tracing if `True` (default: `False`).
- `trace_include_sensitive_data`: Includes sensitive data in traces if `True` (default: `True`).
- `workflow_name`: Names the run for tracing (e.g., “Customer support agent”).
- `trace_id`: Custom trace ID (auto-generated if unset).
- `group_id`: Links multiple runs (e.g., chat thread ID).
- `trace_metadata`: Extra metadata for traces.

### Conversations

Each run represents one conversation turn. Use `RunResultBase.to_input_list()` to continue a conversation:
```python
async def main():
    agent = Agent(name="Assistant", instructions="Reply concisely.")
    with trace(workflow_name="Conversation", group_id="thread_123"):
        # First turn
        result = await Runner.run(agent, "Golden Gate Bridge city?")
        print(result.final_output)  # San Francisco
        # Second turn
        new_input = result.to_input_list() + [{"role": "user", "content": "What state?"}]
        result = await Runner.run(agent, new_input)
        print(result.final_output)  # California
```

### Analogy

Think of the `Runner` as a chef cooking a dish:
- The **agent** is the chef, following a recipe (instructions).
- The **input** is the ingredients (a single item or list).
- The **loop** is the cooking process: mix, taste, adjust, or pass to another chef (handoff).
- **Tools** are kitchen gadgets used by the chef.
- **`RunConfig`** sets kitchen rules (e.g., oven type, safety checks).
- **Streaming** is like watching the chef cook live, seeing each step.

The `run`, `run_sync`, and `run_streamed` methods offer different ways to wait for or watch the dish being prepared.


## Documentation

- [Results Guide](./docs/results.md): Learn about `RunResult` and `RunResultStreaming`.
- [Streaming Guide](./docs/streaming.md): Details on streaming events.
- [Handoffs](./docs/handoffs.md): Information on agent handoffs and input filters.

## Contributing

Contributions are welcome! Please submit issues or pull requests to the [GitHub repository](https://github.com/example/agent-runner).

## License

MIT License. See [LICENSE](./LICENSE) for details.