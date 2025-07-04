# 🔄 Agent Lifecycle Hooks: `RunHooks` vs `AgentHooks`

This document explains the lifecycle hook system used for monitoring and responding to events during agent execution in an agent-based framework. Two main classes are used:

- `RunHooks`: For tracking events across the **entire run**, including multiple agents.
- `AgentHooks`: For tracking events for a **specific agent**.

---

## 📦 Class: `RunHooks`

`RunHooks` is a base class that lets you hook into key events during the **entire lifecycle of an agent run**.  
It is useful when multiple agents are used in a single run, and you want to observe or log global events.

### 🛠 Inherit and Override

```python
from agents import RunHooks

class CustomRunHooks(RunHooks):
    async def on_agent_start(...): pass
    async def on_agent_end(...): pass
