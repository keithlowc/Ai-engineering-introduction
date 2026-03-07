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

Example of an agent pipeline for code development (Model you could even define your local models if you want to save $$ - Read lmstudio for it)

```
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "orchestrator": {
      "description": "Project manager that delegates tasks, breaks down tickets, verifies work, and coordinates the full workflow. Does NOT write code. Only manages, coordinates, and verifies.",
      "mode": "primary",
      "prompt": "You are the project manager orchestrator of this project, your role is to break down the ticket provided, create a new git branch and delegate the work to sub agents where appropriately.",
      "tools": {
        "write": false,
        "edit": false,
        "bash": false,
        "grep": true,
        "glob": true,
        "read": true
      },
      "permission": {
        "bash": "deny",
        "edit": "deny",
        "write": "deny"
      }
    },
    "django-expert": {
      "description": "Expert in Django multi-tenant architecture, models, views, forms, and implementation. Writes implementation code ONLY, not tests.",
      "mode": "subagent",
      "prompt": "You are a Django expert specializing in this repository, your role is to follow concise instructions based on the tickets provided by the orchestrator and accomplish the task.
      "tools": {
        "write": true,
        "edit": true,
        "bash": true,
        "grep": true,
        "glob": true,
        "read": true
      }
    },
    "unit-tester": {
      "description": "Writes and runs unit tests for django-expert's changes. Independent testing to avoid bias.",
      "mode": "subagent",
      "prompt": "You are a unit testing expert for Django applications. Your role is to write units test for any of the changes the django-expert makes and only pass if they are all successful. If not you should let the orchestrator know so he can re delegate the fixes. Make sure your tests are properly written and are not just easy pass.
      "tools": {
        "write": true,
        "edit": true,
        "bash": true,
        "grep": true,
        "glob": true,
        "read": true
      }
    },
    "code-reviewer": {
      "description": "Reviews code and tests for quality, security, and Django best practices.",
      "mode": "subagent",
      "prompt": "You are a code reviewer focused on Django best practices and WorkPal patterns. Your role is to review the overall changes from the djang-expert and unit-tester agents and to make sure we follow the latest python standards within pep-8 and django best practices. If you flag a problem or any changes make sure to bring it back to the orchestrator so he can check and re delegate if necessary"
      "tools": {
        "write": false,
        "edit": false,
        "bash": false,
        "grep": true,
        "glob": true,
        "read": true
      }
    },
    "integration-tester": {
      "description": "Runs integration tests to verify the full system works correctly.",
      "mode": "subagent",
      "prompt": "You are an integration testing expert for Django applications. Your role is to write and run integration tests, and report results to the orchestrator, if any of these tests fails make sure to bring it back to the orchestrator agent.
      "tools": {
        "write": true,
        "edit": true,
        "bash": true,
        "grep": true,
        "glob": true,
        "read": true
      }
    },
    "git-agent": {
      "description": "Commits changes and pushes to remote repository. Only runs after orchestrator verifies all previous steps succeeded.",
      "mode": "subagent",
      "prompt": "You are a git operations agent. Your role is to commit the changes done with a commit message using `git commit -m "{{changes done on the codebase}}"` and then push them to our remote `git push origin {{current_branch}}` You will only push the if the orchestrator ask you to do so.
      "tools": {
        "write": false,
        "edit": false,
        "bash": true,
        "grep": true,
        "glob": true,
        "read": true
      }
    }
  }
}
```


