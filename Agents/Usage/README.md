# Usage Tracker

This library provides a `Usage` dataclass to track and aggregate metrics for interactions with a Large Language Model (LLM) API. It monitors the number of requests, input and output tokens, and detailed token information, making it useful for cost tracking, performance optimization, and quota management in agent-based systems.

## Usage

The `Usage` dataclass tracks LLM API usage metrics, including the number of requests, input/output tokens, and detailed token breakdowns. It provides a method to aggregate metrics from multiple `Usage` instances.

### Class Overview

The `Usage` class is defined using Python's `@dataclass` decorator, which automatically generates special methods like `__init__`, `__repr__`, and `__eq__` based on the class's attributes and has the following attributes:

- **`requests: int = 0`**  
  - **Description**: Tracks the total number of requests made to the LLM API.
  - **Type**: Integer.
  - **Default**: 0.
  - **Purpose**: Keeps a count of how many times the API has been called. This is useful for monitoring usage limits or costs, as many LLM APIs charge based on the number of requests.

- **`input_tokens: int = 0`**  
  - **Description**: Tracks the total number of input tokens sent to the LLM API across all requests.
  - **Type**: Integer.
  - **Default**: 0.
  - **Purpose**: Input tokens represent the text or data sent to the API (e.g., prompts or queries). This metric is critical for understanding the volume of data being processed by the API.

- **`input_tokens_details: InputTokensDetails = field(default_factory=lambda: InputTokensDetails(cached_tokens=0))`**  
  - **Description**: Provides detailed information about input tokens, such as the number of cached tokens.
  - **Type**: InputTokensDetails (a separate dataclass, not fully defined in the provided code).
  - **Default**: An instance of InputTokensDetails initialized with cached_tokens=0.
  - **Purpose**: The input_tokens_details field allows for more granular tracking of input token usage. For example, cached_tokens might represent tokens that were reused from a cache to reduce API costs or improve performance. The field(default_factory=...) ensures that a new InputTokensDetails instance is created for each Usage instance, avoiding shared state issues.

- **`output_tokens: int = 0`**  
  - **Description**: Tracks the total number of output tokens received from the LLM API across all requests.
  - **Type**: Integer.
  - **Default**: 0.
  - **Purpose**: Output tokens represent the text or data generated by the API (e.g., responses or completions). This metric helps monitor the volume of data returned by the API.

- **`output_tokens_details: OutputTokensDetails = field(default_factory=lambda: OutputTokensDetails(reasoning_tokens=0))`**  
  - **Description**: Provides detailed information about output tokens, such as the number of reasoning tokens.
  - **Type**: OutputTokensDetails (a separate dataclass, not fully defined in the provided code).
  - **Default**: An instance of OutputTokensDetails initialized with reasoning_tokens=0.
  - **Purpose**: Similar to input_tokens_details, this field allows for detailed tracking of output token usage. For example, reasoning_tokens might represent tokens used for intermediate reasoning steps in models that support such features (e.g., chain-of-thought reasoning).

- **`total_tokens: int = 0`**  
  - **Description**: Tracks the total number of tokens (input + output) sent and received across all requests.
  - **Type**: Integer.
  - **Default**: 0.
  - **Purpose**: Provides a single metric for the overall token usage, which is often used for billing or quota tracking in LLM APIs.

### Methods

`add(self, other: "Usage") -> None`
  - **Description**: Updates the current Usage instance by adding the metrics from another Usage instance.
  - **Parameters**:
       - **other: Usage**: Another Usage instance whose metrics will be added to the current instance.
  - **Returns**: None (modifies the instance in place).
  - **Behavior**:
        - Adds the `requests`, `input_tokens`, `output_tokens`, and `total_tokens`from the other instance to the current instance.
        - Updates the `input_tokens_details` by summing the `cached_tokens` from both instances.
        - Updates the `output_tokens_details` by summing the `reasoning_tokens` from both instances.
        - Includes safety checks to handle cases where the `other` instance's attributes might be `None` (using conditional expressions to default to `0`).

### **Key Features**
 1. **Type Safety**: The use of type hints (e.g., `int`, `InputTokensDetails`, `OutputTokensDetails`) ensures that the class is compatible with static type checkers like mypy, improving code reliability.
 2. **Immutability of Details**: The `input_tokens_details` and `output_tokens_details` fields are reinitialized in the `add` method to create new instances, preventing unintended side effects from shared references.
 3. **Default Factory**: The `field(default_factory=...)` approach for  `input_tokens_details` and `output_tokens_details` ensures that each instance of `Usage` gets its own instance of the detail classes, avoiding shared state issues common in dataclasses.
 3. **Null Safety**: The `add` method uses conditional expressions (e.g., `other.requests if other.requests else 0`) to handle cases where the `other` instance might have `None` values, making the code robust.
 4. **Extensibility**: The `InputTokensDetails` and `OutputTokensDetails` classes (though not fully defined in the provided code) suggest a modular design, allowing for additional fields (e.g., other types of token details) to be added in the future.

### Limitations
 **Error Handling**: The `add` method includes basic null checks, but additional validation (e.g., for negative values) might be needed in a production environment.

 ### Example

```python
from dataclasses import dataclass, field

@dataclass
class InputTokensDetails:
    cached_tokens: int = 0

@dataclass
class OutputTokensDetails:
    reasoning_tokens: int = 0

@dataclass
class Usage:
    requests: int = 0
    input_tokens: int = 0
    input_tokens_details: InputTokensDetails = field(
        default_factory=lambda: InputTokensDetails(cached_tokens=0)
    )
    output_tokens: int = 0
    output_tokens_details: OutputTokensDetails = field(
        default_factory=lambda: OutputTokensDetails(reasoning_tokens=0)
    )
    total_tokens: int = 0

    def add(self, other: "Usage") -> None:
        self.requests += other.requests if other.requests else 0
        self.input_tokens += other.input_tokens if other.input_tokens else 0
        self.output_tokens += other.output_tokens if other.output_tokens else 0
        self.total_tokens += other.total_tokens if other.total_tokens else 0
        self.input_tokens_details = InputTokensDetails(
            cached_tokens=self.input_tokens_details.cached_tokens
            + other.input_tokens_details.cached_tokens
        )
        self.output_tokens_details = OutputTokensDetails(
            reasoning_tokens=self.output_tokens_details.reasoning_tokens
            + other.output_tokens_details.reasoning_tokens
        )

# Create two Usage instances
usage1 = Usage(requests=2, input_tokens=100, output_tokens=50, total_tokens=150,
               input_tokens_details=InputTokensDetails(cached_tokens=20),
               output_tokens_details=OutputTokensDetails(reasoning_tokens=10))

usage2 = Usage(requests=1, input_tokens=50, output_tokens=25, total_tokens=75,
               input_tokens_details=InputTokensDetails(cached_tokens=10),
               output_tokens_details=OutputTokensDetails(reasoning_tokens=5))

# Aggregate usage
usage1.add(usage2)

print(usage1)
# Output: Usage(requests=3, input_tokens=150, input_tokens_details=InputTokensDetails(cached_tokens=30),
#               output_tokens=75, output_tokens_details
```

## Conclusion
The `Usage` dataclass is a lightweight, type-safe, and extensible way to track LLM API usage metrics. It supports aggregation of metrics across multiple API calls or agent runs, with detailed breakdowns for input and output tokens. Its integration with agent-based systems (e.g., via hooks) makes it particularly useful for monitoring resource usage in complex workflows. For further customization, you would need to define or extend the `InputTokensDetails` and `OutputTokensDetails` classes based on your specific requirements.