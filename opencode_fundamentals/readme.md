# Opencode Fundamentals

## What is Opencode?

Opencode is a CLI-based AI orchestration tool that allows you to:

- Connect to cloud AI providers (OpenAI, Anthropic, etc.)
- Connect to open-source and local models
- Define structured AI agents
- Build repeatable agentic workflows
- Automate reasoning and tool usage directly from the terminal

It is model-agnostic and works with both remote APIs and local OpenAI-compatible servers (such as LM Studio).

---

# Core Concepts

## Agents

Agents are defined inside `opencode.json`.

An agent includes:

- A model
- A system prompt
- Tool permissions
- Parameters (temperature, token limits, etc.)
- Mode (`primary` or `subagent`)

Agents are the foundation of agentic engineering in Opencode.

Example:

```json
{
  "agent": {
    "General": {
      "mode": "primary",
      "model": "openai/gpt-4o",
      "temperature": 0.2,
      "tools": {
        "write": true,
        "edit": true,
        "bash": true
      }
    }
  }
}
```


## Commands

Define basic command sto each of your agents to perform specific actions.

```
"command": {
  "extract": {
    "description": "Start extraction pipeline",
    "agent": "data_extractor",
    "template": "Process output files incrementally."
  }
}
```

Allows you to run inside the opecode cli `/extract` to start the command you want to perform.


