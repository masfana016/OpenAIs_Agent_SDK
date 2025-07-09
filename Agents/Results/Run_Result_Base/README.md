# RunResultBase

## Overview
`RunResultBase` is an abstract base class (ABC) designed to encapsulate the results of an agent's execution, such as an AI model or process. It provides a structured way to store and access data related to the agent's input, outputs, responses, guardrail results, and context. This class is intended to be subclassed to provide specific implementations for the `last_agent` property.

## Purpose
The `RunResultBase` class serves as a standardized container for tracking the outcomes of an agent's run, including:
- The original input provided to the agent.
- New items generated during the run (e.g., messages, tool calls, or outputs).
- Raw responses from the AI model.
- The final output of the agent.
- Guardrail results for input and output validation.
- Contextual information about the run.

## Usage
To use `RunResultBase`, you need to create a subclass that implements the abstract `last_agent` property. Below is an example of how to define and use a subclass:

```python
from dataclasses import dataclass
from typing import Any, List, TypeVar, cast
import abc

T = TypeVar('T')

@dataclass
class RunResultBase(abc.ABC):
    input: str | List[TResponseInputItem]
    new_items: List[RunItem]
    raw_responses: List[ModelResponse]
    final_output: Any
    input_guardrail_results: List[InputGuardrailResult]
    output_guardrail_results: List[OutputGuardrailResult]
    context_wrapper: RunContextWrapper[Any]

    @property
    @abc.abstractmethod
    def last_agent(self) -> Agent[Any]:
        pass

    def final_output_as(self, cls: type[T], raise_if_incorrect_type: bool = False) -> T:
        if raise_if_incorrect_type and not isinstance(self.final_output, cls):
            raise TypeError(f"Final output is not of type {cls.__name__}")
        return cast(T, self.final_output)

    def to_input_list(self) -> List[TResponseInputItem]:
        original_items = ItemHelpers.input_to_new_input_list(self.input)
        new_items = [item.to_input_item() for item in self.new_items]
        return original_items + new_items

    @property
    def last_response_id(self) -> str | None:
        if not self.raw_responses:
            return None
        return self.raw_responses[-1].response_id

@dataclass
class MyRunResult(RunResultBase):
    @property
    def last_agent(self) -> Agent[Any]:
        return MyAgent()  # Replace with your agent implementation

# Example usage
result = MyRunResult(
    input="What is 2+2?",
    new_items=[RunItem(...)],  # Replace with actual RunItem instances
    raw_responses=[ModelResponse(response_id="resp_001", ...)],  # Replace with actual ModelResponse
    final_output=4,
    input_guardrail_results=[InputGuardrailResult(...)],  # Replace with actual guardrail results
    output_guardrail_results=[OutputGuardrailResult(...)],
    context_wrapper=RunContextWrapper(...)
)

# Access final output as a specific type
output = result.final_output_as(int, raise_if_incorrect_type=True)  # Returns 4
print(output)  # Output: 4

# Get combined input and new items
input_list = result.to_input_list()
print(input_list)  # Prints combined list of input and new items

# Get last response ID
print(result.last_response_id)  # Prints "resp_001"
```

## Fields
- **`input: str | List[TResponseInputItem]`**: The original input to the agent, which could be a string or a list of structured input items. Note that input filters may modify this input.
- **`new_items: List[RunItem]`**: New items generated during the agent's run, such as messages, tool calls, or tool outputs.
- **`raw_responses: List[ModelResponse]`**: Raw responses from the AI model.
- **`final_output: Any`**: The final output produced by the agent.
- **`input_guardrail_results: List[InputGuardrailResult]`**: Results from guardrails applied to the input.
- **`output_guardrail_results: List[OutputGuardrailResult]`**: Results from guardrails applied to the final output.
- **`context_wrapper: RunContextWrapper[Any]`**: Contextual information about the agent's run.

## Methods
- **`last_agent` (Abstract Property)**: Must be implemented by subclasses to return the last agent used in the run.
- **`final_output_as(cls: type[T], raise_if_incorrect_type: bool = False) -> T`**: Casts the final output to a specified type. If `raise_if_incorrect_type` is `True`, it raises a `TypeError` if the output is not of the specified (given) type. By default, the cast is only for the typechecker.
```python
def final_output_as(self, cls: type[T], raise_if_incorrect_type: bool = False) -> T:
    """A convenience method to cast the final output to a specific type. By default, the cast
    is only for the typechecker. If you set `raise_if_incorrect_type` to True, we'll raise a
    TypeError if the final output is not of the given type.

    Args:
        cls: The type to cast the final output to.
        raise_if_incorrect_type: If True, we'll raise a TypeError if the final output is not of
            the given type.

    Returns:
        The final output casted to the given type.
    """
    if raise_if_incorrect_type and not isinstance(self.final_output, cls):
        raise TypeError(f"Final output is not of type {cls.__name__}")

    return cast(T, self.final_output)
```
- **`to_input_list() -> List[TResponseInputItem]`**: Combines the original input and new items into a single list of input items.
``` python
def to_input_list(self) -> list[TResponseInputItem]:
    """Creates a new input list, merging the original input with all the new items generated."""
    original_items: list[TResponseInputItem] = ItemHelpers.input_to_new_input_list(self.input)
    new_items = [item.to_input_item() for item in self.new_items]

    return original_items + new_items
```

- **`last_response_id` (Property)**: Returns the response ID of the last model response, or `None` if no responses exist.

## Example Scenario
Imagine a chatbot that answers "What’s 2+2?":
- **Input**: `"What’s 2+2?"`
- **New Items**: A tool call to a calculator and its result.
- **Raw Responses**: The AI’s raw response (e.g., `"The answer is 4"`).
- **Final Output**: `4` (an integer).
- **Guardrails**: Checks to ensure the input and output are safe.
- **Context**: Settings like the chatbot’s language or mode.

You can use `final_output_as(int)` to ensure the output is an integer, or `to_input_list()` to get a full history of inputs and outputs.

## Contributing
Contributions are welcome! Please submit pull requests or issues to the project repository.

## License
This project is licensed under the MIT License.