# Max-Turns Behavior in Weather Agent

## Understanding Max-Turns

The `max_turns` parameter controls how many conversation turns the agent can take before being forced to stop.

## How Turns Work

### Turn 1: Initial Processing
- Agent receives the user input (e.g., "What is tomorrow's weather?")
- Agent processes the request and decides what action to take
- If tools are available, agent decides to use them

### Turn 2: Tool Execution (if needed)
- Agent executes the weather tool
- Tool returns: "FAisalabad weather is sunny!"
- Agent processes the tool result

### Turn 3: Final Response (if available)
- Agent provides the final answer to the user
- Conversation ends

## Configuration Examples

```python
# Agent with tools - needs 2 turns
max_turns=2  # Turn 1: Decide to use tool, Turn 2: Execute tool & respond

# Agent without tools - needs 1 turn  
max_turns=1  # Turn 1: Process input and respond directly

# Agent with complex logic - needs 3+ turns
max_turns=3  # Allows for multi-step reasoning or multiple tool calls
```

## Common Issues

### `MaxTurnsExceeded Error`
```
agents.exceptions.MaxTurnsExceeded: Max turns (1) exceeded
```

**Cause**: Agent needs more turns than allowed
**Solution**: Increase `max_turns` value

### When to Use Different Values

- **max_turns=1**: Simple responses without tools
- **max_turns=2**: Single tool usage (recommended for this weather agent)
- **max_turns=3+**: Complex multi-step operations

## Current Configuration

```python
result = await Runner.run(
    starting_agent=agent,
    input=input,
    max_turns=2,  # Perfect for weather tool usage
    run_config = config
)
```

This allows the agent to use the weather tool and provide a response in exactly 2 turns.