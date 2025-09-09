# User Story Mapper
User Story Mapper is a Python-based tool designed to bridge the gap between Miro and Jira. It uses AI to generate affinity mappings from Miro notes and creates epics in Jira based on the generated groups.

## Features
- Use Miro to collaborate with team members to generate the brainstorm of notes
- Gather notes from Miro and group them into affinity clusters using AI-powered analysis
- Uses OpenAI's GPT models to generate meaningful summaries for each group
- Automatically create epics in Jira based on affinity groups
- Secure credential management using AWS Secrets Manager
- Dockerized for consistent development and deployment
- Supports running in a VS Code Dev Container for reproducible development environments

## Prerequisites
- [Docker](https://www.docker.com/get-started) installed
- AWS account with Secrets Manager access
- OpenAI API key
- Miro API access token
- Jira API credentials
- (Optional) Python 3.8+ if running locally
- (Optional) [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers)

## Configuration
1. Create AWS credentials file:
   ```ini
   [default]
   aws_access_key_id = your_access_key
   aws_secret_access_key = your_secret_key
   ```

2. Store sensitive credentials in AWS Secrets Manager:
   - Miro API token
   - Jira credentials
   - OpenAI API key

3. Update `pyproject.toml` with your configuration:
   ```toml
   [tool.config.aws]
   AWS_REGION = "your-region"
   AWS_USM_SECRET = "your-secret-name"
   ```

## Running with Docker
1. Build the Docker image:
   ```sh
   docker build -t userstorymapper:latest .
   ```

2. Run with credentials mounted:
   ```sh
   docker run -it --rm \
     -v ~/.aws:/root/.aws:ro \
     userstorymapper:latest
   ```

Or use Docker Compose:
   ```sh
   docker-compose up
   ```

For debugging in VS Code:
   ```sh
   docker-compose -f docker-compose.debug.yml up
   ```

## Project Structure
```
app/
├── src/
│   ├── affinity_grouper/    # AI-powered grouping logic
│   ├── connectors/          # API clients for Miro and Jira
│   ├── loggers/            # Logging configuration
│   ├── util/               # Helper utilities
│   └── main.py            # Application entry point
├── tests/                 # Unit tests
├── pyproject.toml        # Project configuration
├── requirements.txt      # Python dependencies
└── docker-compose.yml   # Docker configuration
```

## Troubleshooting
- **AWS Credentials**: Ensure AWS credentials are properly mounted and have correct permissions
- **API Access**: Verify all API tokens are valid and stored in AWS Secrets Manager
- **Docker Mounts**: Check that AWS credentials volume is properly mounted
- **Python Dependencies**: Use Python 3.8+ and a clean virtual environment if running locally

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License
This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). This means:

### You are free to:
- Use this software for any purpose
- Study and modify the source code
- Share copies of the original or modified software

### Under these conditions:
- **Disclose Source**: You must make the source code available when you distribute the software
- **State Changes**: You must clearly mark any changes you make to the software
- **Network Use is Distribution**: If you run a modified version of the software on a server that others can use over a network, you must make your modified source code available to those users
- **License and Copyright Notice**: You must include the license and copyright notice with the code
- **Same License**: Any modifications must be released under the same AGPL-3.0 license

### Complete License:
See the [LICENSE.md](LICENSE.md) file for the complete license text.
