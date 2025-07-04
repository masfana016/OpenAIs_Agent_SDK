# 🔄 Agent Lifecycle Hooks: `RunHooks` vs `AgentHooks`

This document explains the lifecycle hook system used for monitoring and responding to events during agent execution in an agent-based framework. Two main classes are used:

- `RunHooks`: For tracking events across the **entire run**, including multiple agents.
- `AgentHooks`: For tracking events for a **specific agent**.

---

# Agent Lifecycle Hooks

This library provides two generic classes, `RunHooks` and `AgentHooks`, for handling lifecycle event callbacks in agent-based systems. These classes allow you to define custom behavior at various stages of an agent's execution, such as agent start/end, tool invocation, and handoff between agents. Both classes are designed to work with a generic context type `TContext` for flexibility.

## Usage

Both `RunHooks` and `AgentHooks` are generic classes that you can subclass to override specific lifecycle methods. Below is an overview of each class and their methods.

### RunHooks

The `RunHooks` class is used to receive callbacks for lifecycle events across all agents in a run. Subclass it and override the methods you need (AgentHooks se ek nayi class banao (***subclass***), aur jo methods zaroori hon unko apni marzi se likho (***override*** karo)).

> It is useful when multiple agents are used in a single run, and you want to observe or log global events.

#### Methods

- **`on_agent_start(context: RunContextWrapper[TContext], agent: Agent[TContext]) -> None`**  
  Called before an agent is invoked. Triggered each time the current agent changes.  
  - `context`: The wrapped context object for the current run.  
  - `agent`: The agent being invoked.

- **`on_agent_end(context: RunContextWrapper[TContext], agent: Agent[TContext], output: Any) -> None`**  
  Called when an agent produces its final output.  
  - `context`: The wrapped context object for the current run.  
  - `agent`: The agent that produced the output.  
  - `output`: The final output produced by the agent.

- **`on_handoff(context: RunContextWrapper[TContext], from_agent: Agent[TContext], to_agent: Agent[TContext]) -> None`**  
  Called when a handoff occurs between agents.  
  - `context`: The wrapped context object for the current run.  
  - `from_agent`: The agent handing off control.  
  - `to_agent`: The agent receiving control.

- **`on_tool_start(context: RunContextWrapper[TContext], agent: Agent[TContext], tool: Tool) -> None`**  
  Called before a tool is invoked by an agent.  
  - `context`: The wrapped context object for the current run.  
  - `agent`: The agent invoking the tool.  
  - `tool`: The tool being invoked.

- **`on_tool_end(context: RunContextWrapper[TContext], agent: Agent[TContext], tool: Tool, result: str) -> None`**  
  Called after a tool is invoked by an agent.  
  - `context`: The wrapped context object for the current run.  
  - `agent`: The agent that invoked the tool.  
  - `tool`: The tool that was invoked.  
  - `result`: The result produced by the tool (as a string).

#### Example

```python
from agent_lifecycle_hooks import RunHooks, RunContextWrapper, Agent, Tool

class MyRunHooks(RunHooks):
    async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
        print(f"Agent {agent.name} is starting.")

    async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str) -> None:
        print(f"Tool {tool.name} finished with result: {result}")
```

### AgentHooks

The `AgentHooks` class is used to receive callbacks for lifecycle events specific to a single agent. You can assign an instance of this class to `agent.hooks` to receive events for that agent.

#### Methods

- **`on_start(context: RunContextWrapper[TContext], agent: Agent[TContext]) -> None`**  
  Called before the agent is invoked. Triggered each time the agent becomes the active agent.  
  - `context`: The wrapped context object for the current run.  
  - `agent`: The agent being invoked.

- **`on_end(context: RunContextWrapper[TContext], agent: Agent[TContext], output: Any) -> None`**  
  Called when the agent produces its final output.  
  - `context`: The wrapped context object for the current run.  
  - `agent`: The agent that produced the output.  
  - `output`: The final output produced by the agent.

- **`on_handoff(context: RunContextWrapper[TContext], agent: Agent[TContext], source: Agent[TContext]) -> None`**  
  Called when the agent is being handed off to from another agent.  
  - `context`: The wrapped context object for the current run.  
  - `agent`: The agent receiving control.  
  - `source`: The agent that is handing off control.

- **`on_tool_start(context: RunContextWrapper[TContext], agent: Agent[TContext], tool: Tool) -> None`**  
  Called before a tool is invoked by the agent.  
  - `context`: The wrapped context object for the current run.  
  - `agent`: The agent invoking the tool.  
  - `tool`: The tool being invoked.

- **`on_tool_end(context: RunContextWrapper[TContext], agent: Agent[TContext], tool: Tool, result: str) -> None`**  
  Called after a tool is invoked by the agent.  
  - `context`: The wrapped context object for the current run.  
  - `agent`: The agent that invoked the tool.  
  - `tool`: The tool that was invoked.  
  - `result`: The result produced by the tool (as a string).

#### Example

```python
from agent_lifecycle_hooks import AgentHooks, RunContextWrapper, Agent, Tool

class MyAgentHooks(AgentHooks):
    async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
        print(f"Agent {agent.name} is now active.")

    async def on_handoff(self, context: RunContextWrapper, agent: Agent, source: Agent) -> None:
        print(f"Agent {agent.name} received handoff from {source.name}.")

# Assign hooks to an agent
agent.hooks = MyAgentHooks()
```

## Notes

- Both `RunHooks` and `AgentHooks` are designed to be asynchronous. Ensure that your overridden methods are defined with the `async` keyword and use `await` where necessary.
- The `RunContextWrapper[TContext]` provides access to the context of the current run, which can include configuration, state, or other relevant data.
- The `Agent[TContext]` and `Tool` classes are assumed to be defined elsewhere in your system. Ensure they are compatible with the context type `TContext`.
- You only need to override the methods relevant to your use case. Unimplemented methods will have no effect.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue on the project's repository to suggest improvements or report bugs.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.