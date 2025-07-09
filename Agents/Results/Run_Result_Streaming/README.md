# RunResultStreaming

## Overview
The `RunResultStreaming` class is a concrete implementation of the abstract base class `RunResultBase`, defined in `src/agents/result.py`. It is designed to manage the results of an agent (e.g., an AI model or chatbot) operating in streaming mode, where outputs are generated and delivered incrementally. The class supports asynchronous event streaming, turn management, and task cancellation, making it suitable for real-time applications.

## Purpose
`RunResultStreaming` organizes the results of a streaming agent run, including inputs, generated items, raw responses, and guardrail results. It provides methods to stream events as they occur, cancel the run, and handle errors like exceeding maximum turns or triggering guardrails. The class is defined as a `@dataclass` for simplified data management.

## Features

### Inherited Fields from `RunResultBase`
- **`input: str | list[TResponseInputItem]`**: Original input (e.g., a user query), possibly modified by input filters.
- **`new_items: list[RunItem]`**: New items generated during the run (e.g., messages, tool outputs).
- **`raw_responses: list[ModelResponse]`**: Raw AI model responses.
- **`final_output: Any`**: Final result (starts as `None`, updated when the run completes).
- **`input_guardrail_results: list[InputGuardrailResult]`**: Safety/validation results for the input.
- **`output_guardrail_results: list[OutputGuardrailResult]`**: Safety/validation results for the output.
- **`context_wrapper: RunContextWrapper[Any]`**: Context/settings for the run.

### Additional Fields
- **`current_agent: Agent[Any]`**: The currently active agent.
- **`current_turn: int`**: Current turn number in the agent’s execution.
- **`max_turns: int`**: Maximum allowed turns before raising an error.
- **`_current_agent_output_schema: AgentOutputSchemaBase | None`**: Output schema for the current agent (private, not shown in string representation).
- **`trace: Trace | None`**: Tracing/log information (private, not shown in string representation).
- **`is_complete: bool`**: Whether the run is complete (defaults to `False`).
- **`_event_queue: asyncio.Queue[StreamEvent | QueueCompleteSentinel]`**: Queue for streaming events.
- **`_input_guardrail_queue: asyncio.Queue[InputGuardrailResult]`**: Queue for input guardrail results.
- **`_run_impl_task: asyncio.Task[Any] | None`**: Main task for the agent’s logic.
- **`_input_guardrails_task: asyncio.Task[Any] | None`**: Task for input guardrail checks.
- **`_output_guardrails_task: asyncio.Task[Any] | None`**: Task for output guardrail checks.
- **`_stored_exception: Exception | None`**: Stores any exception to be raised later.

### Methods and Properties
1. **`last_agent` Property**
   - **Definition**: Returns the current agent as the last agent run.
   - **Type**: `Agent[Any]`
   - **Description**: Implements the abstract `last_agent` property from `RunResultBase`. Updates dynamically until the run is complete.

2. **`cancel` Method**
   - **Definition**: Cancels the streaming run, stopping tasks and clearing queues.
   - **Description**: Marks the run as complete and cancels asynchronous tasks to free resources.

3. **`stream_events` Method**
   - **Definition**: Asynchronously streams events as they are generated.
   - **Type**: `AsyncIterator[StreamEvent]`
   - **Description**: Yields `StreamEvent` objects from the `_event_queue`, raising exceptions for errors like `MaxTurnsExceeded` or `GuardrailTripwireTriggered`.

4. **`_create_error_details` Method**
   - **Definition**: Creates a `RunErrorDetails` object with the current run state.
   - **Type**: `RunErrorDetails`
   - **Description**: Used internally to provide context for exceptions.

5. **`_check_errors` Method**
   - **Definition**: Monitors for errors like exceeding `max_turns` or guardrail violations.
   - **Description**: Stores exceptions in `_stored_exception` for later raising.

6. **`_cleanup_tasks` Method**
   - **Definition**: Cancels active asynchronous tasks.
   - **Description**: Ensures resources are freed when the run is stopped.

7. **`__str__` Method**
   - **Definition**: Returns a human-readable string representation.
   - **Type**: `str`
   - **Description**: Uses `pretty_print_run_result_streaming` to format the result.

## Usage Example
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
        current_agent=ChatbotAgent(),
        current_turn=1,
        max_turns=5,
        is_complete=False
    )

    async for event in result.stream_events():
        print(f"Received event: {event}")  # Streamed events (e.g., new messages)

    print(result.final_output)  # Final weather response
    print(result.last_agent)  # ChatbotAgent object
    result.cancel()  # Stop the run if needed

asyncio.run(main())
```

## Requirements
- **Python Version**: Python 3.x
- **Dependencies**: Requires `dataclasses`, `typing`, `asyncio`, and custom types (`Agent`, `RunItem`, `ModelResponse`, `StreamEvent`, etc.).
- **Custom Dependencies**: Assumes `pretty_print_run_result_streaming`, `ItemHelpers`, and other project-specific functions/types.

## Notes
- **Streaming Mode**: Designed for real-time applications with incremental output delivery.
- **Error Handling**: Actively monitors for `MaxTurnsExceeded` and `GuardrailTripwireTriggered` exceptions.
- **Cancellation**: Supports graceful cancellation of streaming runs.
- **Use Case**: Ideal for interactive AI systems like chatbots or real-time data processors.

## Example Code
```python
from dataclasses import dataclass
from typing import Any, AsyncIterator
from asyncio import Queue, Task
from src.agents.result import RunResultBase, Agent, StreamEvent, QueueCompleteSentinel, RunErrorDetails

@dataclass
class RunResultStreaming(RunResultBase):
    current_agent: Agent[Any]
    current_turn: int
    max_turns: int
    final_output: Any
    _current_agent_output_schema: AgentOutputSchemaBase | None = field(repr=False)
    trace: Trace | None = field(repr=False)
    is_complete: bool = False
    _event_queue: Queue[StreamEvent | QueueCompleteSentinel] = field(default_factory=Queue, repr=False)
    _input_guardrail_queue: Queue[InputGuardrailResult] = field(default_factory=Queue, repr=False)
    _run_impl_task: Task[Any] | None = field(default=None, repr=False)
    _input_guardrails_task: Task[Any] | None = field(default=None, repr=False)
    _output_guardrails_task: Task[Any] | None = field(default=None, repr=False)
    _stored_exception: Exception | None = field(default=None, repr=False)

    @property
    def last_agent(self) -> Agent[Any]:
        return self.current_agent

    def cancel(self) -> None:
        self._cleanup_tasks()
        self.is_complete = True
        while not self._event_queue.empty():
            self._event_queue.get_nowait()
        while not self._input_guardrail_queue.empty():
            self._input_guardrail_queue.get_nowait()

    async def stream_events(self) -> AsyncIterator[StreamEvent]:
        while True:
            self._check_errors()
            if self._stored_exception:
                self.is_complete = True
                break
            if self.is_complete and self._event_queue.empty():
                break
            try:
                item = await self._event_queue.get()
            except asyncio.CancelledError:
                break
            if isinstance(item, QueueCompleteSentinel):
                self._event_queue.task_done()
                self._check_errors()
                break
            yield item
            self._event_queue.task_done()
        self._cleanup_tasks()
        if self._stored_exception:
            raise self._stored_exception

    # Additional methods (_create_error_details, _check_errors, _cleanup_tasks) omitted for brevity
```