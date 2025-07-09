# RunResult

## Overview
The `RunResult` class is a concrete implementation of the abstract base class `RunResultBase`, defined in `src/agents/result.py`. It is designed to store and manage the results of an agent's execution, such as an AI model or chatbot, by extending the functionality of `RunResultBase`. The class uses Python's `@dataclass` decorator for simplified data management and provides a specific implementation for the required `last_agent` property, along with a custom string representation.

## Purpose
`RunResult` organizes the results of an agent's run, including the input, generated items, raw model responses, final output, guardrail results, and context. It is a concrete class that can be instantiated and used directly, unlike its abstract parent `RunResultBase`.

## Features

### Inherited Fields from `RunResultBase`
The `RunResult` class inherits the following fields from `RunResultBase`:
- **`input: str | list[TResponseInputItem]`**: The original input (e.g., a user query or structured items). May be modified by input filters.
- **`new_items: list[RunItem]`**: New items generated during the run, such as messages, tool calls, or tool outputs.
- **`raw_responses: list[ModelResponse]`**: Raw responses from the AI model.
- **`final_output: Any`**: The final result of the agent's run (e.g., a string, number, or object).
- **`input_guardrail_results: list[InputGuardrailResult]`**: Results of safety/validation checks on the input.
- **`output_guardrail_results: list[OutputGuardrailResult]`**: Results of safety/validation checks on the final output.
- **`context_wrapper: RunContextWrapper[Any]`**: Additional context or settings for the run.

### Additional Field
- **`_last_agent: Agent[Any]`**: A private field storing the last agent used during the run.

### Methods and Properties
1. **`last_agent` Property**
   - **Definition**: Returns the last agent that was run.
   - **Type**: `Agent[Any]`
   - **Description**: Implements the abstract `last_agent` property from `RunResultBase` by returning the `_last_agent` field.

2. **`__str__` Method**
   - **Definition**: Returns a human-readable string representation of the `RunResult` object.
   - **Type**: `str`
   - **Description**: Uses the `pretty_print_result` function to format the result for easy reading or debugging.

3. **Inherited Methods**
   - **`final_output_as(cls: type[T], raise_if_incorrect_type: bool = False) -> T`**:
     - Converts the `final_output` to a specified type.
     - Parameters:
       - `cls`: The type to cast to (e.g., `str`, `int`).
       - `raise_if_incorrect_type`: If `True`, raises a `TypeError` if the output isn’t of the specified type (defaults to `False`).
     - Returns: The `final_output` cast to the specified type.
   - **`to_input_list() -> list[TResponseInputItem]`**:
     - Combines the original `input` and `new_items` into a single list of input items.
     - Returns: A list of `TResponseInputItem` objects.
   - **`last_response_id` Property**:
     - Returns the ID of the last model response from `raw_responses`, or `None` if no responses exist.
     - Type: `str | None`

## Usage Example
The following example demonstrates how to use the `RunResult` class in a chatbot scenario:
```python
from dataclasses import dataclass
from typing import Any
from src.agents.result import RunResult, RunResultBase, Agent

# Example instantiation
result = RunResult(
    input="What’s 2+2?",
    new_items=[RunItem(...), RunItem(...)],  # e.g., tool call and output
    raw_responses=[ModelResponse(response_id="resp123", content="The answer is 4")],
    final_output=4,
    input_guardrail_results=[InputGuardrailResult(...)],
    output_guardrail_results=[OutputGuardrailResult(...)],
    context_wrapper=RunContextWrapper(...),
    _last_agent=ChatbotAgent()
)

# Accessing properties and methods
print(result)  # Pretty-printed result via pretty_print_result
print(result.last_agent)  # Returns ChatbotAgent object
print(result.final_output_as(int))  # Returns 4 as an integer
print(result.last_response_id)  # Returns "resp123"
input_list = result.to_input_list()  # Combines input and new items
```

## Requirements
- **Python Version**: Python 3.x
- **Dependencies**: Requires `dataclasses`, `typing`, and other modules used by `RunResultBase` and related types (`Agent`, `RunItem`, `ModelResponse`, etc.).
- **Custom Dependencies**: Assumes the existence of `ItemHelpers`, `pretty_print_result`, and other custom types/functions defined in the project.

## Notes
- **Concrete Class**: Unlike `RunResultBase`, `RunResult` can be instantiated directly.
- **Extends `RunResultBase`**: Implements the required `last_agent` property and adds a custom `__str__` method.
- **Type Safety**: The `final_output_as` method supports type casting with optional strict type checking.
- **Use Case**: Ideal for tracking and analyzing the results of AI agents, such as chatbots or tool-using models.
- **Guardrails**: Ensures input and output safety through `input_guardrail_results` and `output_guardrail_results`.

## Example Code
Below is the complete source code for the `RunResult` class as defined in `src/agents/result.py`:
```python
from dataclasses import dataclass
from typing import Any, TypeVar, cast
from src.agents.result import RunResultBase, Agent, RunItem, ModelResponse, InputGuardrailResult, OutputGuardrailResult, RunContextWrapper, ItemHelpers

T = TypeVar("T")

@dataclass
class RunResult(RunResultBase):
    _last_agent: Agent[Any]

    @property
    def last_agent(self) -> Agent[Any]:
        """The last agent that was run."""
        return self._last_agent

    def __str__(self) -> str:
        return pretty_print_result(self)
```