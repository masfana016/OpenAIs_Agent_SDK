# Usage Tracker

This library provides a `Usage` dataclass to track and aggregate metrics for interactions with a Large Language Model (LLM) API. It monitors the number of requests, input and output tokens, and detailed token information, making it useful for cost tracking, performance optimization, and quota management in agent-based systems.

## Installation

To use this library, ensure you have Python 3.7+ installed. You can include the `Usage` dataclass in your project by copying the source code from `src/agents/usage.py` or installing it via pip (if published to PyPI):

```bash
pip install usage-tracker
```

## Usage

The `Usage` dataclass tracks LLM API usage metrics, including the number of requests, input/output tokens, and detailed token breakdowns. It provides a method to aggregate metrics from multiple `Usage` instances.

### Class Overview

The `Usage` dataclass is defined in `src/agents/usage.py` and has the following attributes:

- **`requests: int = 0`**  
  Total number of requests made to the LLM API.

- **`input_tokens: int = 0`**  
  Total input tokens sent across all requests.

- **`input_tokens_details: InputTokensDetails = field(default_factory=lambda: InputTokensDetails(cached_tokens=0))`**  
  Details about input tokens, including `cached_tokens` for tokens reused from a cache.

- **`output_tokens: int = 0`**  
  Total output tokens received across all requests.

- **`output_tokens_details: OutputTokensDetails = field(default_factory=lambda: OutputTokensDetails(reasoning_tokens=0))`**  
  Details about output tokens, including `reasoning_tokens` for tokens used in reasoning steps.

- **`total_tokens: int = 0`**  
  Total tokens (input + output) sent and received across all requests.

### Methods

- **`add(self, other: "Usage") -> None`**  
  Aggregates metrics from another `Usage` instance into the current instance. Updates `requests`, `input_tokens`, `output_tokens`, `total_tokens`, and the detailed token fields (`cached_tokens` and `reasoning_tokens`).

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