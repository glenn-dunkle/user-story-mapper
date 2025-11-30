# AI Agents & Automation

This document describes AI agents and automation workflows for the User Story Mapper project.

## Overview

User Story Mapper integrates with external services to provide AI-powered automation:
- **Miro Integration**: Extracts and processes sticky notes from Miro boards
- **Jira Integration**: Creates epics based on AI-grouped stories
- **OpenAI Integration**: Generates summaries for story groups using GPT models
- **AWS Integration**: Manages secure credential storage via Secrets Manager

## Architecture

### Data Processing Pipeline

```
┌─────────────────────────────────────────┐
│    Miro Board (sticky notes)            │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│  MiroConnector                           │
│  - Retrieve board items                  │
│  - Extract text from notes               │
│  - Handle pagination                     │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│  AffinityGrouper (AI-powered)            │
│  - Cluster similar notes                 │
│  - Generate group summaries (GPT)        │
│  - Score and rank groups                 │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│  JiraConnector                           │
│  - Create epics from groups              │
│  - Link to stories                       │
│  - Update project board                  │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────┐
│    Jira Project (updated epics)          │
└──────────────────────────────────────────┘
```

## Components

### Connectors (`src/connectors/`)

#### MiroConnector
**Purpose**: Interact with Miro API to retrieve board data

**Key Methods**:
- `getBoard(board_id)` - Fetch sticky notes from a board
- `get_paginated()` - Handle paginated API responses
- Inherited pagination from HTTPHelper

**Configuration**:
```python
from src.util.config_helper import CONFIG
miro_key = CONFIG["credentials"]["MIRO_API_KEY"]
```

#### JiraConnector
**Purpose**: Create and manage Jira epics

**Key Methods**:
- `postGroupsToJira(affinity_groups)` - Create epics from grouped notes
- Manage epic creation and linking

#### SobConnector
**Purpose**: Legacy connector for Stories on Board integration

### Affinity Grouper (`src/affinity_grouper/`)

**Purpose**: AI-powered clustering and summarization

**Key Features**:
- Uses Sentence Transformers for semantic similarity
- Clusters similar notes using ML algorithms
- Calls OpenAI GPT to generate group summaries
- Confidence scoring for recommendations

**Key Methods**:
- `getAffinityGroups()` - Main grouping orchestration
- Supports configurable cluster count and distance thresholds

### Utilities (`src/util/`)

#### ConfigHelper
**Purpose**: Centralized configuration management

**Features**:
- Loads config from `pyproject.toml`
- Retrieves secrets from AWS Secrets Manager
- Manages credentials safely
- Global `CONFIG` dictionary access

#### LoggerHelper
**Purpose**: Consistent logging with sensitive data redaction

**Features**:
- Redacts API keys from logs
- Obfuscates email addresses and tokens
- Supports multiple log levels
- File and console output

#### HTTPHelper
**Purpose**: Base HTTP client with retry logic and pagination

**Features**:
- Automatic retries with exponential backoff
- Pagination support (offset and cursor-based)
- Timeout handling
- Error recovery

## Development Workflow

### Setup

1. **Configure AWS credentials**:
   ```bash
   mkdir -p ~/.aws
   # Add credentials in ~/.aws/credentials
   ```

2. **Set environment variables**:
   ```bash
   export AWS_REGION="your-region"
   export AWS_USM_SECRET="your-secret-name"
   ```

3. **Configure pyproject.toml**:
   ```toml
   [tool.config.aws]
   AWS_REGION = "us-east-1"
   AWS_USM_SECRET = "user-story-mapper-secrets"
   ```

### Testing

Run unit tests to validate components:

```bash
# All tests
python -m pytest tests/unit -v

# Specific module tests (e.g., Miro connector)
python -m pytest tests/unit/miro -v

# With coverage
python -m pytest tests/unit --cov=src --cov-report=html
```

### Debugging

**Using VS Code Debugger**:
1. Set breakpoints in source files
2. Use Python debug configuration
3. Monitor logs in `/app/logs/`

**Common Issues**:
- Missing AWS credentials → Check `~/.aws/credentials`
- API key not found → Verify AWS Secrets Manager has the secret
- Network errors → Check Miro/Jira API endpoints
- Rate limits → Add delays between API calls

## External Integrations

### Miro API v2
- **Endpoint**: `https://api.miro.com/v2`
- **Authentication**: Bearer token in Authorization header
- **Rate Limits**: Respects Miro's rate limiting policies
- **Pagination**: Cursor-based pagination

### Jira API
- **Endpoint**: Project-specific (configured in `pyproject.toml`)
- **Authentication**: Basic auth or token-based
- **Operations**: Epic creation, story linking

### OpenAI API
- **Model**: Configurable in config (e.g., `gpt-3.5-turbo`)
- **Usage**: Text summarization for grouped stories
- **Cost**: Metered by API usage

### AWS Secrets Manager
- **Storage**: Secure credential management
- **Rotation**: Supports automatic key rotation
- **Access**: IAM-based permission control

## Security Considerations

✅ **Credentials Management**
- API keys never in code
- Stored in AWS Secrets Manager or environment variables
- Automatic rotation support

✅ **Data Protection**
- Sensitive data redacted from logs
- HTTPS for all API communication
- Request signing for AWS

✅ **Error Handling**
- Graceful degradation on failures
- Comprehensive error logging
- Retry mechanisms for transient errors

✅ **Access Control**
- IAM roles for AWS operations
- Token-based authentication for APIs
- Rate limiting awareness

## Best Practices

### When Adding Features

1. **Extend HTTPHelper** for new API integrations
2. **Use LoggerHelper** for all logging
3. **Store configs** in `pyproject.toml` or AWS Secrets
4. **Add comprehensive tests** in `tests/unit/`
5. **Document new components** in this file

### When Debugging

1. **Check logs** in `/app/logs/user_story_mapper_err.log`
2. **Verify credentials** are properly set
3. **Test API connectivity** manually first
4. **Enable debug logging** for detailed output
5. **Use VS Code debugger** for step-through debugging

### Common Patterns

**Configuration Access**:
```python
from src.util.config_helper import CONFIG
api_key = CONFIG["credentials"]["MIRO_API_KEY"]
```

**Logging**:
```python
self.logger.debug(self._obfuscate(f"Processing with key: {api_key}"))
```

**API Calls with Pagination**:
```python
response = super().get_paginated(
    url=url,
    headers=headers,
    params=params
)
```

## Deployment

### Docker Deployment

```bash
# Build image
docker build -t userstorymapper:latest .

# Run with credentials
docker run -it --rm \
  -v ~/.aws:/root/.aws:ro \
  userstorymapper:latest
```

### CI/CD Integration

The project is configured for container-based deployment with:
- Docker support for consistent environments
- Environment variable injection for secrets
- Health checks and error handling

## Further Reading

- [README.md](README.md) - Project overview and setup
- [.github/copilot-instructions.md](.github/copilot-instructions.md) - AI agent instructions
- Local test suites in `tests/unit/`
- Configuration examples in `pyproject.toml`
