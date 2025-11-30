# User Story Mapper

User Story Mapper is a Python-based tool designed to bridge the gap between Miro and Jira. It uses AI to generate affinity mappings from Miro notes and creates epics in Jira based on the generated groups.

## Quick Start

1. **[Installation & Setup](README.md#installation)**
2. **[Running the Application](README.md#running-with-docker)**
3. **[Configuration Guide](README.md#configuration)**
4. **[AI Agents & Automation](AGENTS.md)** - Detailed architecture and workflows

## Features

- **Miro Integration**: Extract and process sticky notes from Miro boards
- **AI-Powered Grouping**: Cluster similar notes using semantic analysis
- **Smart Summarization**: Generate meaningful summaries using OpenAI GPT
- **Jira Automation**: Create epics automatically based on grouped stories
- **Secure Credentials**: Manage sensitive data safely with AWS Secrets Manager
- **Docker Support**: Consistent environments for development and deployment
- **VS Code Integration**: Dev container support for reproducible workflows

## Installation

### Prerequisites

- [Docker](https://www.docker.com/get-started) (recommended) or Python 3.8+
- AWS account with Secrets Manager access
- OpenAI API key
- Miro API access token
- Jira API credentials
- (Optional) [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

## Configuration

### Step 1: AWS Credentials

Create AWS credentials file at `~/.aws/credentials`:

```ini
[default]
aws_access_key_id = your_access_key
aws_secret_access_key = your_secret_key
```

### Step 2: AWS Secrets Manager

Store sensitive credentials in AWS Secrets Manager:
- Miro API token
- Jira credentials  
- OpenAI API key

### Step 3: Project Configuration

Update `pyproject.toml` with your AWS and project settings:

```toml
[tool.config.aws]
AWS_REGION = "us-east-1"
AWS_USM_SECRET = "user-story-mapper-secrets"

[tool.config.miro]
MIRO_BOARD_ID = "your-board-id"

[tool.config.jira]
JIRA_INSTANCE = "https://your-instance.atlassian.net"
JIRA_PROJECT_KEY = "YOUR_PROJECT"
```

See [AGENTS.md](AGENTS.md) for detailed configuration examples.

## Running with Docker

### Using Docker Build

1. Build the Docker image:
   ```bash
   docker build -t userstorymapper:latest .
   ```

2. Run with AWS credentials mounted:
   ```bash
   docker run -it --rm \
     -v ~/.aws:/root/.aws:ro \
     userstorymapper:latest
   ```

### Using Docker Compose

Standard execution:
```bash
docker-compose up
```

Debug mode with VS Code support:
```bash
docker-compose -f docker-compose.debug.yml up
```

## Project Structure

```
app/
├── src/
│   ├── main.py                    # Application entry point
│   ├── affinity_grouper/          # AI-powered grouping and summarization
│   │   └── affinity_grouper.py   # Clustering logic
│   ├── connectors/                # External API integrations
│   │   ├── miro_connector.py     # Miro board API client
│   │   ├── jira_connector.py     # Jira epic creation
│   │   └── sob_connector.py      # Legacy Stories on Board
│   ├── loggers/                  # Logging configuration
│   │   └── err_logger.py         # Error logging setup
│   └── util/                     # Shared utilities
│       ├── config_helper.py      # Configuration management
│       ├── http_helper.py        # HTTP client with pagination
│       └── logger_helper.py      # Logging utilities
├── tests/
│   └── unit/                     # Unit test suites
│       ├── miro/                 # Miro connector tests
│       ├── jira/                 # Jira connector tests
│       └── affinity_grouper/     # Grouping tests
├── docs/                         # Documentation
├── logs/                         # Application logs
├── pyproject.toml               # Project configuration & dependencies
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container configuration
├── docker-compose.yml           # Multi-container orchestration
├── AGENTS.md                    # AI agents & automation guide
├── README.md                    # This file
└── LICENSE.md                   # AGPL-3.0 License
```

## Testing

Run the unit test suite:

```bash
# All tests
python -m pytest tests/unit -v

# Specific test module (e.g., Miro tests)
python -m pytest tests/unit/miro -v

# With coverage report
python -m pytest tests/unit --cov=src --cov-report=html
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AWS Credentials not found | Ensure `~/.aws/credentials` exists and is properly formatted |
| API key errors | Verify credentials are stored in AWS Secrets Manager |
| Docker mount errors | Check volume path syntax: `-v ~/.aws:/root/.aws:ro` |
| Python version mismatch | Use Python 3.8+ or run via Docker |
| Miro/Jira connection errors | Test API endpoints manually and verify network access |
| Missing dependencies | Run `pip install -r requirements.txt` |

See [AGENTS.md](AGENTS.md) for detailed debugging and development guides.

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Write tests for new features in `tests/unit/`
- Follow existing code patterns and conventions
- Update documentation in [AGENTS.md](AGENTS.md) if needed
- Ensure all tests pass: `python -m pytest tests/unit -v`
- Check credentials are never committed to version control

## Documentation

- **[AGENTS.md](AGENTS.md)** - Detailed guide to AI agents, architecture, and integrations
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - AI coding agent instructions
- **[LICENSE.md](LICENSE.md)** - AGPL-3.0 License details

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

### Key Points

You are free to:
- ✅ Use this software for any purpose
- ✅ Modify and study the source code
- ✅ Share copies of the original or modified software

Under these conditions:
- 📋 **Disclose Source**: Make source code available when distributing
- 📝 **State Changes**: Clearly mark all modifications
- 🌐 **Network Use is Distribution**: If you run modified code on a server that others use over a network, you must make your modifications available to those users
- © **License Notice**: Include license and copyright notice with the code
- 📄 **Same License**: Modifications must be released under AGPL-3.0

For complete details, see [LICENSE.md](LICENSE.md).

### Under these conditions:
- **Disclose Source**: You must make the source code available when you distribute the software
- **State Changes**: You must clearly mark any changes you make to the software
- **Network Use is Distribution**: If you run a modified version of the software on a server that others can use over a network, you must make your modified source code available to those users
- **License and Copyright Notice**: You must include the license and copyright notice with the code
- **Same License**: Any modifications must be released under the same AGPL-3.0 license

### Complete License:
See the [LICENSE.md](LICENSE.md) file for the complete license text.
