# Agent Response Handling Module

This module provides a robust framework for managing responses and interactions with an AI model, specifically designed to integrate with the OpenAI SDK. It offers a structured approach to handling agent-generated items such as messages, tool calls, handoffs, reasoning steps, and MCP (custom platform/server) interactions. The module emphasizes type safety using Python’s advanced typing system, including generics, type aliases, and Pydantic models for data validation. It is ideal for developers building applications that require complex agent-based interactions with AI models.

## Table of Contents
- [Overview](#overview)
- [Key Components](#key-components)
  - [Type Aliases](#type-aliases)
  - [RunItemBase Class](#runitembase-class)
  - [Specific Item Classes](#specific-item-classes)
  - [ModelResponse Class](#modelresponse-class)
  - [ItemHelpers Class](#itemhelpers-class)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Overview

The module is designed to handle the lifecycle of agent interactions with an AI model, including processing model outputs, converting them to inputs for further interactions, and managing specialized tasks like tool calls and agent handoffs. It abstracts the complexity of the OpenAI SDK’s response types, providing a clean, type-safe interface for developers. Key features include:

- **Type Safety**: Uses Python’s `typing` and `typing_extensions` modules for robust type checking.
- **Data Classes**: Leverages `dataclasses` for structured, readable representations of response items.
- **Pydantic Integration**: Utilizes Pydantic models for validation and serialization of OpenAI SDK types.
- **Utility Methods**: Provides helper methods for extracting and manipulating response data.
- **Extensibility**: Supports a variety of item types, including messages, tool calls, and custom MCP interactions.

The module assumes the presence of an `Agent` class (not shown) that represents an entity interacting with the model, and a `Usage` class for tracking API usage metrics.

## Key Components

### Type Aliases
The module defines several type aliases to simplify references to complex OpenAI SDK types and ensure type safety across the codebase.

- **`TResponse`**: Alias for `openai.types.responses.Response`, representing the complete response from the model.
- **`TResponseInputItem`**: Alias for `ResponseInputItemParam`, representing input items sent to the model (e.g., user messages, tool call outputs). These are typically dictionaries with fields like `content` and `role`.
- **`TResponseOutputItem`**: Alias for `ResponseOutputItem`, representing model outputs (e.g., messages, tool calls). These are typically Pydantic models.
- **`TResponseStreamEvent`**: Alias for `ResponseStreamEvent`, used for handling streaming responses from the model.
- **`T`**: A generic `TypeVar` constrained to `Union[TResponseOutputItem, TResponseInputItem]`, used in the `RunItemBase` class for type-safe item handling.
- **`ToolCallItemTypes`**: A union of supported tool call types, including:
  - `ResponseFunctionToolCall`: Function calls.
  - `ResponseComputerToolCall`: Computer action calls.
  - `ResponseFileSearchToolCall`: File search calls.
  - `ResponseFunctionWebSearch`: Web search calls.
  - `ResponseCodeInterpreterToolCall`: Code interpreter calls.
  - `ImageGenerationCall`: Image generation calls.
  - `LocalShellCall`: Local shell command calls.
  - `McpCall`: Custom MCP server calls.
- **`RunItem`**: A union of all possible agent-generated item types (e.g., `MessageOutputItem`, `ToolCallItem`, etc.), used for handling collections of items.

### RunItemBase Class
```python
@dataclass
class RunItemBase(Generic[T], abc.ABC):
    agent: Agent[Any]
    raw_item: T
    def to_input_item(self) -> TResponseInputItem: ...
```

- **Purpose**: An abstract base class for all items generated during an agent’s run, providing a common structure and behavior.
- **Fields**:
  - `agent`: The `Agent` instance responsible for generating the item. The `Agent` class is assumed to manage interactions with the model.
  - `raw_item`: The raw item from the OpenAI SDK, either a `TResponseOutputItem` (Pydantic model) or `TResponseInputItem` (dictionary).
- **Method**:
  - `to_input_item()`: Converts the item to a `TResponseInputItem` for passing back to the model.
    - If `raw_item` is a dictionary (input item), it is returned directly.
    - If `raw_item` is a Pydantic model (output item), it is serialized to a dictionary using `model_dump(exclude_unset=True)`.
    - Raises `AgentsException` for unexpected item types.
- **Generic Type**: Uses `T` to ensure `raw_item` is either a `TResponseOutputItem` or `TResponseInputItem`.

### Specific Item Classes
These data classes inherit from `RunItemBase` and represent specific types of items generated during an agent’s run. Each includes a `type` field with a `Literal` string for identification.

- **`MessageOutputItem`**
  ```python
  @dataclass
  class MessageOutputItem(RunItemBase[ResponseOutputMessage]):
      raw_item: ResponseOutputMessage
      type: Literal["message_output_item"] = "message_output_item"
  ```
  - **Purpose**: Represents a text-based message output from the LLM, such as a response to a user query.
  - **Fields**:
    - `raw_item`: A `ResponseOutputMessage` containing the message content (e.g., a list of `ResponseOutputText` or `ResponseOutputRefusal`).
    - `type`: Identifies the item as a message output.

- **`HandoffCallItem`**
  ```python
  @dataclass
  class HandoffCallItem(RunItemBase[ResponseFunctionToolCall]):
      raw_item: ResponseFunctionToolCall
      type: Literal["handoff_call_item"] = "handoff_call_item"
  ```
  - **Purpose**: Represents a tool call that initiates a handoff from one agent to another, typically using a function call.
  - **Fields**:
    - `raw_item`: A `ResponseFunctionToolCall` specifying the handoff action.
    - `type`: Identifies the item as a handoff call.

- **`HandoffOutputItem`**
  ```python
  @dataclass
  class HandoffOutputItem(RunItemBase[TResponseInputItem]):
      raw_item: TResponseInputItem
      source_agent: Agent[Any]
      target_agent: Agent[Any]
      type: Literal["handoff_output_item"] = "handoff_output_item"
  ```
  - **Purpose**: Represents the result of a handoff, capturing the transition between agents.
  - **Fields**:
    - `raw_item`: The input item (dictionary) representing the handoff.
    - `source_agent`: The agent initiating the handoff.
    - `target_agent`: The agent receiving the handoff.
    - `type`: Identifies the item as a handoff output.

- **`ToolCallItem`**
  ```python
  ToolCallItemTypes: TypeAlias = Union[...]
  @dataclass
  class ToolCallItem(RunItemBase[ToolCallItemTypes]):
      raw_item: ToolCallItemTypes
      type: Literal["tool_call_item"] = "tool_call_item"
  ```
  - **Purpose**: Represents a tool call, such as a function call, computer action, file search, or web search.
  - **Fields**:
    - `raw_item`: The specific tool call (e.g., `ResponseFunctionToolCall`, `ResponseComputerToolCall`).
    - `type`: Identifies the item as a tool call.
  - **Type Alias**: `ToolCallItemTypes` includes a variety of tool call types for flexibility.

- **`ToolCallOutputItem`**
  ```python
  @dataclass
  class ToolCallOutputItem(
      RunItemBase[Union[FunctionCallOutput, ComputerCallOutput, LocalShellCallOutput]]
  ):
      raw_item: FunctionCallOutput | ComputerCallOutput | LocalShellCallOutput
      output: Any
      type: Literal["tool_call_output_item"] = "tool_call_output_item"
  ```
  - **Purpose**: Represents the output of a tool call, such as the result of a function or shell command.
  - **Fields**:
    - `raw_item`: The raw output (e.g., `FunctionCallOutput`, `ComputerCallOutput`).
    - `output`: The actual result of the tool call (any type, typically a string or structured data).
    - `type`: Identifies the item as a tool call output.

- **`ReasoningItem`**
  ```python
  @dataclass
  class ReasoningItem(RunItemBase[ResponseReasoningItem]):
      raw_item: ResponseReasoningItem
      type: Literal["reasoning_item"] = "reasoning_item"
  ```
  - **Purpose**: Represents a reasoning step or thought process generated by the model, useful for understanding the model’s decision-making.
  - **Fields**:
    - `raw_item`: A `ResponseReasoningItem` containing the reasoning data.
    - `type`: Identifies the item as a reasoning item.

- **`MCPListToolsItem`**
  ```python
  @dataclass
  class MCPListToolsItem(RunItemBase[McpListTools]):
      raw_item: McpListTools
      type: Literal["mcp_list_tools_item"] = "mcp_list_tools_item"
  ```
  - **Purpose**: Represents a call to list available tools on an MCP (custom platform/server).
  - **Fields**:
    - `raw_item`: The `McpListTools` call.
    - `type`: Identifies the item as an MCP list tools request.

- **`MCPApprovalRequestItem`**
  ```python
  @dataclass
  class MCPApprovalRequestItem(RunItemBase[McpApprovalRequest]):
      raw_item: McpApprovalRequest
      type: Literal["mcp_approval_request_item"] = "mcp_approval_request_item"
  ```
  - **Purpose**: Represents a request for approval from an MCP server, likely for authorizing actions.
  - **Fields**:
    - `raw_item`: The `McpApprovalRequest` object.
    - `type`: Identifies the item as an MCP approval request.

- **`MCPApprovalResponseItem`**
  ```python
  @dataclass
  class MCPApprovalResponseItem(RunItemBase[McpApprovalResponse]):
      raw_item: McpApprovalResponse
      type: Literal["mcp_approval_response_item"] = "mcp_approval_response_item"
  ```
  - **Purpose**: Represents the response to an MCP approval request, indicating approval or denial.
  - **Fields**:
    - `raw_item`: The `McpApprovalResponse` object.
    - `type`: Identifies the item as an MCP approval response.

- **`RunItem` Type Alias**
  ```python
  RunItem: TypeAlias = Union[
      MessageOutputItem,
      HandoffCallItem,
      HandoffOutputItem,
      ToolCallItem,
      ToolCallOutputItem,
      ReasoningItem,
      MCPListToolsItem,
      MCPApprovalRequestItem,
      MCPApprovalResponseItem,
  ]
  ```
  - **Purpose**: A union type encompassing all possible agent-generated items, used for type-safe handling of collections.

### ModelResponse Class
```python
@dataclass
class ModelResponse:
    output: list[TResponseOutputItem]
    usage: Usage
    response_id: str | None
    def to_input_items(self) -> list[TResponseInputItem]: ...
```

- **Purpose**: Encapsulates a complete response from the model, aggregating outputs, usage metrics, and an optional response ID.
- **Fields**:
  - `output`: A list of `TResponseOutputItem` objects (e.g., messages, tool calls).
  - `usage`: A `Usage` object tracking API usage (e.g., token counts).
  - `response_id`: An optional string ID for referencing the response in subsequent calls (not supported by all model providers).
- **Method**:
  - `to_input_items()`: Converts the `output` list to a list of `TResponseInputItem` by serializing Pydantic models to dictionaries using `model_dump(exclude_unset=True)`.

### ItemHelpers Class
```python
class ItemHelpers:
    @classmethod
    def extract_last_content(cls, message: TResponseOutputItem) -> str: ...
    @classmethod
    def extract_last_text(cls, message: TResponseOutputItem) -> str | None: ...
    @classmethod
    def input_to_new_input_list(cls, input: str | list[TResponseInputItem]) -> list[TResponseInputItem]: ...
    @classmethod
    def text_message_outputs(cls, items: list[RunItem]) -> str: ...
    @classmethod
    def text_message_output(cls, message: MessageOutputItem) -> str: ...
    @classmethod
    def tool_call_output_item(cls, tool_call: ResponseFunctionToolCall, output: str) -> FunctionCallOutput: ...
```

- **Purpose**: A utility class providing class methods to manipulate and extract data from response items.
- **Methods**:
  - **`extract_last_content`**:
    - Extracts the last text or refusal content from a `ResponseOutputMessage`.
    - Returns an empty string for non-message items.
    - Raises `ModelBehaviorError` for unexpected content types (e.g., neither `ResponseOutputText` nor `ResponseOutputRefusal`).
  - **`extract_last_text`**:
    - Extracts the last text content (ignoring refusals) from a `ResponseOutputMessage`.
    - Returns `None` if the item is not a message or the last content is not text.
  - **`input_to_new_input_list`**:
    - Converts a string or list of `TResponseInputItem` to a list of `TResponseInputItem`.
    - For a string, creates a single user message with `role: "user"`.
    - For a list, returns a deep copy to avoid modifying the original.
  - **`text_message_outputs`**:
    - Concatenates text content from all `MessageOutputItem` objects in a list of `RunItem`.
    - Ignores non-message items.
  - **`text_message_output`**:
    - Extracts all text content from a single `MessageOutputItem`, concatenating multiple `ResponseOutputText` items.
  - **`tool_call_output_item`**:
    - Creates a `FunctionCallOutput` dictionary from a `ResponseFunctionToolCall` and its output string, including the `call_id` and `type`.

## Installation
This module is part of a larger framework. Install the required dependencies using pip:
```bash
pip install openai pydantic typing_extensions
```

Ensure the parent project includes the `Agent` and `Usage` classes, as well as any custom MCP-related dependencies.

## Usage Examples

### Example 1: Handling a Model Response
```python
from .agent import Agent
from .usage import Usage
from openai.types.responses import ResponseOutputMessage, ResponseOutputText

# Initialize an agent
agent = Agent()

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
```

### Example 2: Processing a Tool Call
```python
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
```

### Example 3: Handling Multiple Items
```python
from . import MessageOutputItem, ItemHelpers

# Mock a list of items
items = [
    MessageOutputItem(agent=agent, raw_item=ResponseOutputMessage(content=[ResponseOutputText(text="Step 1")])),
    MessageOutputItem(agent=agent, raw_item=ResponseOutputMessage(content=[ResponseOutputText(text="Step 2")])),
]

# Extract all text content
all_text = ItemHelpers.text_message_outputs(items)
print(all_text)  # "Step 1Step 2"
```

## Dependencies
- **Python 3.8+**: Required for type annotations and dataclasses.
- **`openai` SDK**: Provides the response types and API integration.
- **`pydantic`**: Used for data validation and serialization of OpenAI SDK models.
- **`typing_extensions`**: Provides advanced type hints like `TypeAlias` and `Literal`.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/my-feature`).
3. Commit your changes (`git commit -m "Add my feature"`).
4. Push to the branch (`git push origin feature/my-feature`).
5. Open a pull request.

Please include tests and update documentation as needed.

## License
MIT License