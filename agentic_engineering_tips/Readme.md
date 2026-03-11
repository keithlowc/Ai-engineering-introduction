# Agentic Engineering Fundamentals

## What is Agentic Engineering?

Agentic engineering is the practice of building AI workflows that execute specific tasks by autonomously planning, testing, and executing. Instead of writing rigid, rules-based algorithms, you build AI agents that can:

- **Plan**: Break down complex tasks into smaller steps
- **Reason**: Make decisions based on context and available information
- **Execute**: Take actions using tools and APIs
- **Iterate**: Retry or adjust approach when initial attempts fail

Think of it as moving from "if this, then that" logic to systems that can think through problems and adapt their approach.

## Prerequisites

Before diving into agentic engineering, you should understand these core areas:

### 1. Microservices Architecture

Microservices are small, independent services that communicate to form a larger application. Key concepts:

- **Single Responsibility**: Each service does one thing well
- **Independent Deployment**: Services can be deployed and scaled separately
- **Loose Coupling**: Services communicate through well-defined interfaces

### 2. Service Communication

Services need to talk to each other. Common approaches include:

- **REST APIs**: HTTP-based request/response pattern
- **gRPC**: High-performance, protocol buffer-based communication
- **Message Queues** (RabbitMQ, Kafka): Asynchronous, event-driven communication
- **GraphQL**: Flexible query language for APIs

### 3. AI Libraries and Frameworks

Familiarize yourself with popular frameworks:

- **LangChain**: Popular framework for building LLM applications with chains, agents, and memory
- **LangGraph**: Built on LangChain for creating agent workflows as graphs
- **LlamaIndex**: Data framework for building RAG (Retrieval-Augmented Generation) systems
- **Scikit Learn**: Traditional ML algorithms
- **TensorFlow/PyTorch**: Deep learning frameworks

### 4. Understanding Different Models

Models vary in capability, cost, and use cases:

- **Anthropic (Claude)**: Strong reasoning and analysis capabilities
- **OpenAI (GPT-4, GPT-4o)**: General-purpose, strong across many tasks
- **Google (Gemini)**: Multimodal, integrated with Google ecosystem
- **Meta (Llama)**: Open-source options
- **Local Models** (Ollama, LM Studio): Run on your own hardware for privacy/control

## Model Capabilities and Selection

### Choosing the Right Model

Consider these factors:

1. **Task Requirements**: Some models excel at coding, others at reasoning or creative tasks
2. **Cost**: API-based models charge per token; local models have infrastructure costs
3. **Latency**: Local models may be faster for high-volume applications
4. **Privacy**: Some use cases require data to stay on premises
5. **Fine-tuning**: Custom models can be trained on your specific data

### Local vs Cloud Models

| Aspect | Cloud Models | Local Models |
|--------|--------------|--------------|
| Setup | Quick start | Requires hardware |
| Cost | Pay-per-use | Upfront GPU investment |
| Privacy | Data leaves your system | Data stays local |
| Customization | Fine-tuning available | Full control over model |
| Latency | Depends on network | Depends on hardware |

### Fine-tuning Local Models

When working with local models, you can improve performance through:

1. **Fine-tuning**: Train on your specific domain data
2. **Quantization**: Reduce model size for faster inference
3. **Prompt engineering**: Optimize how you instruct the model

## Deploying Agentic Systems

### Docker and Containerization

Agents are typically deployed as containerized microservices:

```dockerfile
# Example Dockerfile for an agent service
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

### Example: Phone Number Extraction Service

Let's walk through building a service that extracts phone numbers from text files:

**Problem**: Extract specific phone numbers associated with names from text files containing multiple people's information.

**Solution with LangChain**:

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel

class PhoneExtractionAgent:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(api_key=api_key, stream=True)  # Enable streaming
        self.prompt = PromptTemplate(
            template="""Extract the phone number for {name} from the following text:
            
            {text}
            
            Return only the phone number or 'Not found'.""",
            input_variables=["name", "text"]
        )
    
    def extract(self, name: str, text: str) -> str:
        chain = self.prompt | self.llm
        return chain.invoke({"name": name, "text": text}).content
    
    def extract_stream(self, name: str, text: str):
        chain = self.prompt | self.llm
        for chunk in chain.stream({"name": name, "text": text}):
            yield chunk.content
```

**Integration with FastAPI**:

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()
agent = PhoneExtractionAgent(api_key="your-key")

@app.get("/extract/{name}")
async def extract_phone(name: str, text: str):
    async def event_generator():
        async for chunk in agent.extract_stream(name, text):
            yield f"data: {chunk}\n\n"
            await asyncio.sleep(0.01)  # Small delay for readability
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

**Frontend consumer example**:

```javascript
async function extractPhone(name, text) {
    const response = await fetch(`/extract/${name}?text=${encodeURIComponent(text)}`);
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    let result = "";
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        result += decoder.decode(value);
        console.log("Received:", result);  // See progress in real-time
    }
    return result;
}
```

**Deployment**:
1. Build Docker image: `docker build -t phone-extractor .`
2. Run container: `docker run -p 8000:8000 phone-extractor`
3. Agents can now call this service via HTTP

## Core Agent Concepts

### Tool Calling

Agents can use tools to interact with external systems:

```python
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool

def search_database(query: str) -> str:
    # Your database logic here
    return "results"

tools = [
    Tool(
        name="SearchDatabase",
        func=search_database,
        description="Search the company database for information"
    )
]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)
```

### Error Handling and Retries

Agentic systems need robust error handling:

- **Retry logic**: Automatically retry failed API calls
- **Fallback models**: Switch to backup if primary fails
- **Graceful degradation**: Return partial results when possible
- **Logging**: Track failures for debugging

### Memory and Context

Agents can maintain state across interactions:

- **Short-term memory**: Conversation history within a session
- **Long-term memory**: Persistent storage of learned information
- **Vector stores**: Semantic search over documents

## Evaluation and Monitoring

### Measuring Agent Performance

Track these metrics:

- **Task completion rate**: How often the agent succeeds
- **Latency**: Time from request to response
- **Cost**: Token usage and API costs
- **Accuracy**: Quality of outputs (may need human evaluation)

### Iterative Improvement

1. **Collect feedback**: User ratings, correction signals
2. **Analyze failures**: Identify patterns in unsuccessful runs
3. **Refine prompts**: Improve instructions based on errors
4. **Add tools**: Give agents new capabilities as needed
5. **Fine-tune**: Train on your specific failure cases

## Getting Started

1. Start with a simple agent (one tool, straightforward task)
2. Add complexity gradually
3. Always have human oversight for critical decisions
4. Monitor everything in production
5. Iterate based on real-world performance

## Code Quality and Guardrails

Maintaining high code quality is essential for agentic systems that will be used in production. Here's how to establish consistent standards:

### Pre-commit Hooks

Pre-commit hooks automatically check and fix code before each commit. This catches issues early and enforces standards across your team.

**Installation**:
```bash
pip install pre-commit
pre-commit install
```

**`.pre-commit-config.yaml`**:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

**Run manually**:
```bash
pre-commit run --all-files
```

### Code Style (PEP 8)

Follow PEP 8 guidelines for consistent, readable Python code:

**Naming Conventions**:
```python
# Variables and functions: snake_case
def extract_phone_number(text: str) -> str:
    user_name = "john"

# Classes: PascalCase
class PhoneExtractionAgent:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Private variables: _leading_underscore
def _internal_helper():
    _cache = {}
```

**Imports** (use isort to organize automatically):
```python
# Standard library
import os
import json
from typing import Optional

# Third-party packages
from fastapi import FastAPI
from langchain_openai import ChatOpenAI

# Local application
from agent import PhoneExtractionAgent
```

**Line length and formatting**:
- Maximum 88 characters per line (ruff default, matches black)
- Use blank lines to separate logical sections
- Keep functions focused (ideally under 50 lines)

### Type Hints

Always use type hints for better code clarity and tooling support:

```python
from typing import Optional, Generator

def extract_phone(
    name: str,
    text: str,
    timeout: Optional[int] = 30
) -> str:
    """Extract phone number for a specific name.
    
    Args:
        name: The person to look up
        text: Text containing phone information
        timeout: Request timeout in seconds
        
    Returns:
        The phone number or 'Not found'
    """
    ...

def extract_stream(name: str, text: str) -> Generator[str, None, None]:
    """Yield phone numbers as they're extracted."""
    for chunk in _extract_chunks(name, text):
        yield chunk
```

### Documentation Standards

**Docstrings** (Google style):
```python
def process_document(
    document: str,
    mode: str = "extract",
    options: Optional[dict] = None
) -> dict:
    """Process a document using the configured agent.

    Args:
        document: The text content to process
        mode: Processing mode - "extract", "summarize", or "analyze"
        options: Optional configuration overrides

    Returns:
        Dict containing the processed results with keys:
        - result: The processed output
        - confidence: Confidence score (0-1)
        - metadata: Processing metadata

    Raises:
        ValueError: If mode is not recognized
        TimeoutError: If processing exceeds timeout

    Example:
        >>> result = process_document("John: 555-1234", mode="extract")
        >>> print(result["result"])
        "555-1234"
    """
```

### Linting Configuration

**`pyproject.toml`**:
```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by formatter)
]

[tool.ruff.lint.isort]
known-first-party = ["agent", "api"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
```

### CI/CD Integration

Add linting to your GitHub Actions workflow:

```yaml
name: CI

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      
      - name: Install dependencies
        run: pip install pre-commit
      
      - name: Run pre-commit
        run: pre-commit run --all-files
      
      - name: Run tests
        run: pytest
```

### Why These Guardrails Matter

For agentic systems specifically:

1. **Consistency**: Agents are complex - code style consistency reduces cognitive load
2. **Type safety**: Catch bugs early when connecting agents to tools/APIs
3. **Documentation**: Future you (and teammates) will thank you
4. **Automated checks**: Remove manual code review friction
5. **Refactoring confidence**: Safe to improve code when tests and types catch regressions
