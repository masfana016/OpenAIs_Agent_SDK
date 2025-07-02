# Dynamic Instructions Agent

## Overview
This project provides a simple implementation of an Agent with dynamic instructions in a Python-based framework. The agent uses a function to generate runtime instructions based on user context, enabling personalized and flexible behavior.

## Features
- **Dynamic Instructions**: Instructions are generated at runtime using a function, allowing customization based on user data (e.g., name).
- **Type-Safe Context**: Uses generic types (`RunContextWrapper[UserContext]`, `Agent[UserContext]`) for structured context handling.
- **Synchronous/Asynchronous Support**: Supports both regular and async instruction functions for flexibility.

## Code
```python
def dynamic_instructions(
    context: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    return f"The user's name is {context.context.name}. Help them with their questions."

agent = Agent[UserContext](
    name="Triage agent",
    instructions=dynamic_instructions,
)
```

## Usage
- **Define UserContext**: Create a UserContext class with attributes like name to hold user-specific data.
- **Configure Agent**: Instantiate an Agent with a name and the dynamic_instructions function.
- **Run Agent**: The framework calls dynamic_instructions at runtime, passing the context and agent, to generate a prompt (e.g., "The user's name is Alice. Help them with their questions.").
- **Integrate**: Use the agent in a chatbot, workflow automation, or AI system to handle user queries with personalized instructions.

## Example
For a user with context.context.name = "Bob", the agent generates:
"The user's name is Bob. Help them with their questions."

The agent then responds, e.g., "Hello Bob, how can I assist you?"

## Requirements
- Python 3.8+
- A framework supporting typed agents and context wrappers (e.g., a custom AI or automation framework).
- UserContext class with at least a name attribute.

## Installation
- Ensure the framework for Agent and RunContextWrapper is installed.
- Copy the code into your project.
- Define or import UserContext and required dependencies.

## Extending
- **Rich Context**: Add fields to UserContext (e.g., language, role) for more complex instructions.
  ```python
  def dynamic_instructions(context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
    user = context.context
    return f"Greet {user.name} in {user.language}. Focus on {user.interests}."
  ```
- **Async Instructions**: Use an async function for fetching external data:
  ```python
  async def dynamic_instructions(context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
      user_data = await fetch_user_data(context.context.user_id)
      return f"The user's name is {user_data.name}. Help them with their questions."
  ```
- **Conditional Logic**: Customize instructions based on user roles or other conditions.
  ```python
  def dynamic_instructions(context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
    user = context.context
    if user.role == "admin":
        return f"Provide technical details to {user.name} for system administration queries."
    return f"Help {user.name} with basic user questions."
  ```

## Notes
- Ensure context.context.name is defined to avoid errors.
- The agent’s behavior depends on the underlying framework (e.g., AI model or rule-based system).
- For xAI integration, see [xAI API](https://x.ai/api) for API-based agent configuration.

## License
MIT License