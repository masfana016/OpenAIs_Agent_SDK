# Fields of RunConfig

Each field in the `RunConfig` dataclass configures a specific aspect of the agent run. Below is an explanation of each field, its default value, and its role, with emphasis on how it applies to your code.

- **`model: str | Model | None = None`**
    **Purpose**: Specifies the AI model to use for the entire agent run (e.g., "gemini-2.0-flash" or a Model object). If set, it overrides the model specified in individual agents.
    - **Details**: The model name or object must be resolvable by the model_provider. If None, the agent’s own model is used.
    - **In code**:
        model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
        config = RunConfig(model=model, ...)
        You set model to an OpenAIChatCompletionsModel instance with "gemini-2.0-flash", ensuring the agent uses this model for processing the input ("Kal ka weather kya hai?").
    - **Impact**: Ensures the Gemini model processes all AI invocations, overriding any agent-specific model settings.
- **`model_provider: ModelProvider = field(default_factory=MultiProvider)`**  
  **Purpose**: Defines the provider (e.g., OpenAI, Gemini) used to resolve the model name and handle API interactions. It’s the service that connects the agent to the AI model.  
  **Details**:  
  - Defined as an instance attribute using `dataclasses.field` with a `default_factory` that creates a new `MultiProvider` instance for each `RunConfig` object.  
  - `MultiProvider` defaults to OpenAI (per documentation), but can support multiple providers.  
  - As an instance attribute, each `RunConfig` instance has its own `model_provider`, allowing customization per run.  
  **In Your Code**:  
  ```python
  client = AsyncOpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
  config = RunConfig(model_provider=client, ...)
  ```  
  You override the default `MultiProvider` with a custom `AsyncOpenAI` client configured for the Gemini API. This ensures API calls go to Gemini’s endpoint, not OpenAI.  
  **Impact**: Critical for routing model requests to the correct API. Without your custom client, the default `MultiProvider` might try to use OpenAI, causing errors with "gemini-2.0-flash".

- **`model_settings: ModelSettings | None = None`**  
  **Purpose**: Configures global model settings (e.g., temperature, max tokens) that override agent-specific settings if non-null.  
  **Details**: Allows fine-tuning model behavior across the run. If `None`, agent-specific settings are used.  
  **In Your Code**: Not specified (`None` by default), so the agent uses the default settings of the `OpenAIChatCompletionsModel`.  
  **Impact**: You didn’t need custom settings for your simple weather bot, but this field is useful for adjusting model behavior (e.g., making responses more creative or concise).

- **`handoff_input_filter: HandoffInputFilter | None = None`**  
  **Purpose**: Defines a global filter to modify inputs passed to a new agent during a handoff (when one agent transfers control to another).  
  **Details**: Agent-specific `Handoff.input_filter` takes precedence if set. Useful for editing or sanitizing inputs during handoffs.  
  **In Your Code**: Not used (`None` by default), as your weather bot doesn’t involve handoffs.  
  **Impact**: Irrelevant for your single-agent workflow but useful in multi-agent scenarios.

- **`input_guardrails: list[InputGuardrail[Any]] | None = None`**  
  **Purpose**: A list of guardrails to check the initial input for safety or compliance (e.g., blocking inappropriate queries).  
  **Details**: Applied only to the first agent’s input. If violated, a `GuardrailTripwireTriggered` exception is raised.  
  **In Your Code**: Not used (`None` by default).  
  **Impact**: Not needed for your simple weather query but useful for ensuring safe inputs in production systems.

- **`output_guardrails: list[OutputGuardrail[Any]] | None = None`**  
  **Purpose**: A list of guardrails to check the final output for safety or compliance (e.g., filtering offensive content).  
  **Details**: Applied to the final output of the run.  
  **In Your Code**: Not used (`None` by default).  
  **Impact**: Not needed for your weather bot but useful for ensuring safe outputs in sensitive applications.

- **`tracing_disabled: bool = False`**  
  **Purpose**: Disables tracing (logging of agent actions, inputs, and outputs) for the run if `True`.  
  **In Your Code**:  
  ```python
  config = RunConfig(tracing_disabled=True, ...)
  ```  
  You set `tracing_disabled=True`, meaning no logs or traces are recorded for the agent run.  
  **Impact**: Reduces overhead and avoids logging sensitive data (e.g., the weather query or tool output).

- **`trace_include_sensitive_data: bool = True`**  
  **Purpose**: Controls whether sensitive data (e.g., tool inputs/outputs, model generations) is included in traces.  
  **Details**: If `False`, traces include events but omit sensitive data. Irrelevant if `tracing_disabled=True`.  
  **In Your Code**: Not specified (defaults to `True`), but irrelevant since `tracing_disabled=True`.  
  **Impact**: No effect in your case due to disabled tracing.

- **`workflow_name: str = "Agent workflow"`**  
  **Purpose**: A name for the run, used in tracing to identify the workflow (e.g., "Weather bot workflow").  
  **In Your Code**: Not specified (defaults to "Agent workflow").  
  **Impact**: Irrelevant since tracing is disabled, but useful for debugging or monitoring in traced runs.

- **`trace_id: str | None = None`**  
  **Purpose**: A custom ID for the trace, used for tracking the run. If `None`, a new ID is generated.  
  **In Your Code**: Not specified (`None` by default).  
  **Impact**: Irrelevant due to `tracing_disabled=True`.

- **`group_id: str | None = None`**  
  **Purpose**: A grouping ID to link multiple traces (e.g., for a single conversation or process).  
  **In Your Code**: Not specified (`None` by default).  
  **Impact**: Irrelevant due to disabled tracing.

- **`trace_metadata: dict[str, Any] | None = None`**  
  **Purpose**: Additional metadata to include in traces (e.g., user ID, session info).  
  **In Your Code**: Not specified (`None` by default).  
  **Impact**: Irrelevant due to disabled tracing.
