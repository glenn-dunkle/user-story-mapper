# User Story Mapper
User Story Mapper is a Python-based tool designed to bridge the gap between Miro and StoriesOnBoard. It uses AI to generate affinity mappings from Miro notes and uses the output groups to create epics in the story map board.

## Features
- Use Miro to collaborate with team members to generate the brainstorm of notes (i.e. "post-it notes")
- Given URLs to the Miro board and the StoriesOnBoard story map, gather notes from Miro and group them into affinity clusters using AI
- Automatically create epics in StoriesOnBoard based on affinity groups
- Dockerized for consistent development and deployment
- Supports running in a VS Code Dev Container for reproducible development environments

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/get-started) installed
- (Optional) Python 3.8+ if running locally
- (Optional) [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) for a pre-configured environment

### Running with Docker
1. Build the Docker image:
   ```sh
   docker build -t userstorymapper:latest .
   ```
2. Run the application:
   ```sh
   docker run -it --rm userstorymapper:latest
   ```

Or use the provided Docker Compose files:
   ```sh
   docker-compose up
   ```
   - For debugging in VS Code, use:
   ```sh
   docker-compose -f docker-compose.debug.yml up
   ```

### Running Locally
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the application:
   ```sh
   python main.py
   ```

## Development Environment
- Recommended: Use the provided Dev Container configuration for a ready-to-code environment in VS Code.
- All dependencies and tools are pre-installed in the container.

## Project Structure
- `main.py` – Main entry point for the application
- `requirements.txt` – Python dependencies
- `Dockerfile` – Docker build instructions
- `docker-compose.yml` – Docker Compose configuration
- `docker-compose.debug.yml` – Docker Compose for debugging

## Troubleshooting
- If you encounter issues with Docker permissions, try running with `sudo` or ensure your user is in the `docker` group.
- For Python dependency issues, ensure you are using Python 3.8+ and a clean virtual environment.
- If running in a dev container, rebuild the container after changing dependencies.

## Contributing
Pull requests are welcome! Please open an issue first to discuss major changes.

## License
This project is licensed under the MIT License.
