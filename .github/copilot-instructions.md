# User Story Mapper AI Agent Instructions

## Project Overview
User Story Mapper is a Python application that integrates Miro boards with Jira using AI-powered affinity grouping. The application:
- Extracts sticky notes from Miro boards
- Groups them using AI clustering
- Generates summaries using OpenAI's GPT
- Creates corresponding Jira epics

## Architecture & Components

### Core Components
- `src/connectors/` – API clients for external services
  - `miro_connector.py` – Handles Miro board data retrieval
  - `jira_connector.py` – Manages Jira epic creation
- `src/affinity_grouper/` – AI clustering and summarisation logic
- `src/util/` – Shared utilities
  - `config_helper.py` – Configuration management with AWS Secrets
  - `logger_helper.py` – Logging with sensitive data redaction
  - `http_helper.py` – Base HTTP client functionality
- `tests/unit/` – Pytest suite organised by scenario with shared fixtures in `conftest.py`

### Data Flow
1. Miro sticky notes → `MiroConnector` → raw text
2. Text → `AffinityGrouper` → clustered groups with AI summaries
3. Groups → `JiraConnector` → Jira epics

## Key Patterns & Conventions

### Configuration Management
- Config loaded from `pyproject.toml`
- Sensitive values stored in AWS Secrets Manager
- Access via the `CONFIG` global dictionary:
```python
from src.util.config_helper import CONFIG
api_key = CONFIG["credentials"]["MIRO_API_KEY"]
```
- When tests must override config values, patch `src.util.config_helper.CONFIG`

### HTTP Requests
- Extend `HTTPHelper` for API clients and call its pagination helpers:
```python
response = super().get_paginated(self, url=url, headers=headers, params=params)
```
- Keep retry, timeout, and error handling inside connector classes

### Logging
- Use `LoggerHelper` for consistent logging with redaction
- Sensitive data patterns live in `logger_helper.py`
- Always use the class logger:
```python
self.logger.debug(self._obfuscate(message))
```

### Testing & QA
- Unit tests live in `tests/unit/`; create one test module per scenario
- Shared fixtures go in `tests/unit/conftest.py` (e.g. the `miro` connector fixture)
- Run tests with:
```bash
python -m pytest tests/unit
```
- Prefer mocking external services (`boto3`, network calls) over real I/O

## Development Workflow

### Setup
1. Configure AWS credentials in `/root/.aws/credentials`
2. Create or update `pyproject.toml` from the template
3. Set required config variables:
```
[aws]
AWS_REGION = "your-region"
AWS_USM_SECRET = "your-secret-name"
```

### Debugging
- Use VS Code's Python debugger
- Set breakpoints in connector classes
- Monitor `logs/user_story_mapper_err.log`

## External Dependencies
- Miro API v2
- Jira API
- OpenAI API
- AWS Secrets Manager
- Sentence Transformers for clustering

## Common Pitfalls
- Always handle pagination in API responses
- Redact sensitive data in logs
- Convert Miro HTML content to plain text before processing
- Guard against API rate limits and transient failures
