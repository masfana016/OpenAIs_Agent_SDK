# Result 

## Overview
The `RunResultBase`, `RunResult`, and `RunResultStreaming` classes are designed to manage the results of an agent's execution, such as an AI model or chatbot, in a Python-based system. These classes, defined in `src/agents/result.py`, provide structured storage for inputs, outputs, and metadata. `RunResultBase` is an abstract base class, while `RunResult` and `RunResultStreaming` are concrete implementations for non-streaming and streaming scenarios, respectively.

## Source Code Location
- **File**: `src/agents/result.py`

## Classes

### RunResultBase
- **Type**: Abstract Base Class (ABC)
- **Purpose**: Serves as a template for storing agent run results, defining common fields and methods.
- **Use Case**: Cannot be instantiated directly; used as a foundation for `RunResult` and `RunResultStreaming`.

### RunResult
- **Type**: Concrete class, inherits from `RunResultBase`
- **Purpose**: Manages results for synchronous, non-streaming agent runs where results are delivered after completion.
- **Use Case**: Ideal for one-shot tasks, like answering a single query (e.g., "What's 2+2?").

### RunResultStreaming
- **Type**: Concrete class, inherits from `RunResultBase`
- **Purpose**: Manages results for asynchronous, streaming agent runs, delivering results incrementally in real-time.
- **Use Case**: Suitable for interactive applications, like chatbots streaming responses as they are generated.

## Comparison Table

| **Aspect**                | **RunResultBase**                                                                 | **RunResult**                                                                 | **RunResultStreaming**                                                                 |
|---------------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| **Type**                  | Abstract base class (cannot be instantiated)                                      | Concrete class (can be instantiated)                                          | Concrete class (can be instantiated)                                                 |
| **Purpose**               | Defines common structure and methods for agent run results                       | Manages results for non-streaming, synchronous agent runs                     | Manages results for streaming, asynchronous agent runs with real-time event delivery |
| **Inheritance**           | Base class (parent)                                                              | Inherits from `RunResultBase`                                                | Inherits from `RunResultBase`                                                       |
| **Streaming Support**     | None (abstract, no execution logic)                                              | None (synchronous, results delivered at once)                                 | Yes (asynchronous, streams events as generated)                                      |
| **Fields**                | - `input`<br>- `new_items`<br>- `raw_responses`<br>- `final_output`<br>- `input_guardrail_results`<br>- `output_guardrail_results`<br>- `context_wrapper` | Same as `RunResultBase`, plus:<br>- `_last_agent`                            | Same as `RunResultBase`, plus:<br>- `current_agent`<br>- `current_turn`<br>- `max_turns`<br>- `_current_agent_output_schema`<br>- `trace`<br>- `is_complete`<br>- `_event_queue`<br>- `_input_guardrail_queue`<br>- `_run_impl_task`<br>- `_input_guardrails_task`<br>- `_output_guardrails_task`<br>- `_stored_exception` |
| **last_agent Property**   | Abstract (must be implemented by subclasses)                                      | Returns `_last_agent` (fixed agent)                                          | Returns `current_agent` (updates dynamically)                                        |
| **Methods**               | - `final_output_as`<br>- `to_input_list`<br>- `last_response_id`                 | Same as `RunResultBase`, plus:<br>- `__str__` (uses `pretty_print_result`)   | Same as `RunResultBase`, plus:<br>- `cancel`<br>- `stream_events`<br>- `_create_error_details`<br>- `_check_errors`<br>- `_cleanup_tasks`<br>- `__str__` (uses `pretty_print_run_result_streaming`) |
| **Error Handling**        | None (abstract, no runtime logic)                                                | Basic (type checking in `final_output_as`)                                   | Advanced (monitors `max_turns`, guardrail violations, async task errors)             |
| **String Representation** | None (abstract)                                                                 | Custom `__str__` with `pretty_print_result`                                  | Custom `__str__` with `pretty_print_run_result_streaming`                           |
| **Use Case Example**      | N/A (template only)                                                             | Chatbot answering "What’s 2+2?" with results returned at once                | Chatbot streaming weather updates in real-time                                      |

## Detailed Features

### RunResultBase
- **Fields**:
  - `input: str | list[TResponseInputItem]`: Original input, possibly modified by filters.
  - `new_items: list[RunItem]`: Generated items (e.g., messages, tool outputs).
  - `raw_responses: list[ModelResponse]`: Raw AI model responses.
  - `final_output: Any`: Final result of the agent.
  - `input_guardrail_results: list[InputGuardrailResult]`: Input safety/validation results.
  - `output_guardrail_results: list[OutputGuardrailResult]`: Output safety/validation results.
  - `context_wrapper: RunContextWrapper[Any]`: Run context/settings.
- **Methods**:
  - `final_output_as(cls: type[T], raise_if_incorrect_type: bool = False) -> T`: Casts `final_output` to a specified type.
  - `to_input_list() -> list[TResponseInputItem]`: Combines input and new items into a list.
  - `last_response_id: str | None`: Gets the ID of the last model response.
- **Abstract Property**:
  - `last_agent`: Must be implemented by subclasses.

### RunResult
- **Additional Field**:
  - `_last_agent: Agent[Any]`: Stores the agent used for the run.
- **Methods**:
  - `last_agent`: Returns `_last_agent`.
  - `__str__`: Formats the result using `pretty_print_result`.
- **Use Case**: Non-streaming tasks where results are collected and returned after completion.

### RunResultStreaming
- **Additional Fields**:
  - `current_agent: Agent[Any]`: The active agent.
  - `current_turn: int`: Current turn number.
  - `max_turns: int`: Maximum allowed turns.
  - `_current_agent_output_schema: AgentOutputSchemaBase | None`: Output schema (private).
  - `trace: Trace | None`: Tracing info (private).
  - `is_complete: bool`: Whether the run is complete.
  - `_event_queue: asyncio.Queue[StreamEvent | QueueCompleteSentinel]`: Queue for streaming events.
  - `_input_guardrail_queue: asyncio.Queue[InputGuardrailResult]`: Queue for input guardrail results.
  - `_run_impl_task`, `_input_guardrails_task`, `_output_guardrails_task: asyncio.Task[Any] | None`: Async tasks.
  - `_stored_exception: Exception | None`: Stores exceptions for later raising.
- **Methods**:
  - `last_agent`: Returns `current_agent`.
  - `cancel`: Stops the run and cleans up tasks.
  - `stream_events`: Asynchronously yields streaming events.
  - `_create_error_details`, `_check_errors`, `_cleanup_tasks`: Support error handling and task management.
  - `__str__`: Formats the result using `pretty_print_run_result_streaming`.
- **Use Case**: Real-time applications requiring incremental result delivery.

## Usage Examples

### RunResult
```python
from src.agents.result import RunResult, Agent

result = RunResult(
    input="What’s 2+2?",
    new_items=[RunItem(...), RunItem(...)],
    raw_responses=[ModelResponse(response_id="resp123", content="The answer is 4")],
    final_output=4,
    input_guardrail_results=[InputGuardrailResult(...)],
    output_guardrail_results=[OutputGuardrailResult(...)],
    context_wrapper=RunContextWrapper(...),
    _last_agent=CalculatorAgent()
)
print(result)  # Pretty-printed result
print(result.final_output_as(int))  # 4
```

### RunResultStreaming
```python
import asyncio
from src.agents.result import RunResultStreaming, Agent, StreamEvent

async def main():
    result = RunResultStreaming(
        input="What’s the weather like?",
        new_items=[],
        raw_responses=[],
        final_output=None,
        input_guardrail_results=[],
        output_guardrail_results=[],
        context_wrapper=RunContextWrapper(...),
        current_agent=WeatherAgent(),
        current_turn=1,
        max_turns=5,
        is_complete=False
    )
    async for event in result.stream_events():
        print(f"Event: {event}")
    result.cancel()  # Stop if needed

asyncio.run(main())
```

## Requirements
- **Python Version**: Python 3.x
- **Dependencies**: Requires `dataclasses`, `typing`, `asyncio` (for `RunResultStreaming`), and custom types (`Agent`, `RunItem`, `ModelResponse`, `StreamEvent`, etc.).
- **Custom Dependencies**: Assumes `pretty_print_result`, `pretty_print_run_result_streaming`, `ItemHelpers`, and other project-specific functions/types.

## Notes
- **RunResultBase**: Abstract template ensuring consistency across subclasses.
- **RunResult**: Simple, synchronous, for one-shot tasks.
- **RunResultStreaming**: Complex, asynchronous, for real-time streaming with turn and error management.
- **Error Handling**: `RunResultStreaming` actively monitors `max_turns` and guardrail violations, unlike the simpler `RunResult`.