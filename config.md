# OpenAI Agents SDK Debug Logging Guide

This README explains how to configure, enable, and customize logging in the **OpenAI Agents SDK** for better debugging and development insights.

---

## ⚙️ SDK Configuration (API Keys, Clients, Tracing)

The SDK auto-loads the `OPENAI_API_KEY` environment variable when imported. If you cannot set it beforehand, use:

```python
from agents import set_default_openai_key
set_default_openai_key("sk-...")
```

### ✅ Custom OpenAI Client
You can override the default `AsyncOpenAI` instance:

```python
from openai import AsyncOpenAI
from agents import set_default_openai_client

custom_client = AsyncOpenAI(base_url="...", api_key="...")
set_default_openai_client(custom_client)
```

### 🔁 Use Chat Completions API Instead of Default
```python
from agents import set_default_openai_api
set_default_openai_api("chat_completions")
```

### 🔎 Tracing Control
Tracing is enabled by default and uses the same API key. To set a separate key:

```python
from agents import set_tracing_export_api_key
set_tracing_export_api_key("sk-...")
```

To disable tracing entirely:
```python
from agents import set_tracing_disabled
set_tracing_disabled(True)
```

---

## 🔍 Default Logging Behavior

The SDK provides two built-in Python loggers:

- `openai.agents`
- `openai.agents.tracing`

By default:

- Only **warnings** and **errors** are shown in the console (`stdout`).
- **Debug** and **info-level logs** are **suppressed** (not shown).

---

## ✅ Enable Verbose Logging (Show All Logs)

To quickly enable full debug-level logging (recommended during development), use:

```python
from agents import enable_verbose_stdout_logging

enable_verbose_stdout_logging()
```

This will print all logs, including debug information, directly to the console.

---

## 🛠️ Customize Logging Manually

For more control over logging behavior (such as output formatting or writing to a file), use Python’s built-in `logging` module.

```python
import logging

# Create logger for OpenAI Agents
logger = logging.getLogger("openai.agents")  # or use "openai.agents.tracing"

# Set the desired log level
logger.setLevel(logging.DEBUG)     # Show all logs
# logger.setLevel(logging.INFO)    # Show info and above
# logger.setLevel(logging.WARNING) # Show warnings and errors only

# Add a handler (by default, logs go to stderr)
logger.addHandler(logging.StreamHandler())
```

You can also attach file handlers, formatters, or filters as needed for advanced logging setups.

---

## 🔒 Hide Sensitive Data in Logs

To protect sensitive data (e.g., user input, model responses), you can disable specific log contents using **environment variables**.

### Disable logging of LLM inputs and outputs:

```bash
export OPENAI_AGENTS_DONT_LOG_MODEL_DATA=1
```

### Disable logging of tool inputs and outputs:

```bash
export OPENAI_AGENTS_DONT_LOG_TOOL_DATA=1
```

You can place these in your shell configuration or a `.env` file depending on your environment.

---

## 💡 Summary

| Purpose                        | Method                                    | Result                                       |
| ------------------------------ | ----------------------------------------- | -------------------------------------------- |
| Enable full debug logs         | `enable_verbose_stdout_logging()`         | Shows all logs in console                    |
| Custom logging setup           | `logging.getLogger(...)`, `setLevel(...)` | Full control over format/output/level        |
| Hide LLM input/output in logs  | `OPENAI_AGENTS_DONT_LOG_MODEL_DATA=1`     | Prevents model data from being logged        |
| Hide tool input/output in logs | `OPENAI_AGENTS_DONT_LOG_TOOL_DATA=1`      | Prevents tool input/output from being logged |

---

## 📌 Example Logging Configuration

```python
import logging

logger = logging.getLogger("openai.agents")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
```

This setup logs all messages with timestamps, logger name, log level, and message content.

