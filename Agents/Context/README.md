# Context

## Understanding Agent Context

### What Is Context?

In our app, **agents** are smart assistants powered by large language models (LLMs). A **context** is like a backpack of information you give to an agent to help it do its job. It’s a flexible object you create and pass to the agent when you run it, holding details like user data or settings that the agent, its **tools**, or other components might need.

Think of context as a way to share important info with every part of the system without hardcoding it.

Context is **generic**, meaning you can put any Python object inside it (e.g., a dictionary, a custom class, or even a simple string). This makes it super versatile for different use cases.

### How Does Context Work?

Context is a **dependency-injection tool**. This means it’s a way to give agents, tools, and other parts of your app the resources they need without hardcoding them. Here’s how it happens:

1. You create a context object (e.g., a Python dictionary or custom object) with the data or tools your app needs.
2. You pass this context to `Runner.run()`, the function that starts your agent workflow.
3. The context is automatically shared with every **agent**, **tool**, and **handoff** in the workflow, so they can all access its contents.

### Key Terms Explained

- **Context**: The toolbox (a Python object) that holds shared data or resources for your agents and tools to use.
- **Generic**: Context can be any type of Python object, like a dictionary, list, or custom class, giving you flexibility to design it as needed.
- **Dependency-Injection**: A technique where you provide dependencies (like data or tools) to components (like agents) by passing them in, rather than having the components create them internally.
- **Runner.run()**: The function in our app that kicks off the agent workflow, taking the context as an input and passing it to all components.
- **Agent**: A smart assistant powered by a large language model (LLM), configured with instructions, a model, and tools to perform tasks.
- **Tool**: An external resource or function (e.g., a calculator or web search) that an agent can use to complete its tasks.
- **Handoff**: A process where one agent or component passes control or data to another, ensuring smooth collaboration.
- **Grab Bag**: A casual term for context, meaning it’s a flexible container that can hold all sorts of dependencies and state.
- **Dependencies**: Resources or data (e.g., a database connection or API key) that agents and tools need to do their jobs.
- **State**: Information about the current situation (e.g., user inputs or task progress) that components might need to share.

### Example

Let’s say you’re building a chatbot agent that answers customer questions:

1. You create a context object, like a Python dictionary:
   ```python
   context = {
       "user_id": "123",
       "database": customer_db,
       "api_key": "xyz"
   }
