# User Story Mapper
User Story Mapper is a Python-based tool designed to bridge the gap between Miro and StoriesOnBoard. It uses AI to generate affinity mappings from Miro notes and uses the output groups to create epics in the story map board.
## Features
- Use Miro to collaborate with team members to generate the brainstorm of notes (i.e. "post-it notes")
- Given URLs to the Miro board and the StoriesOnBoard story map, gather notes from Miro and group them into affinity clusters
- Dockerized for consistent development and deployment

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/get-started) installed
- (Optional) Python 3.8+ if running locally

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

### Running Locally
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the application:
   ```sh
   python main.py
   ```

## Project Structure
- `main.py` – Main entry point for the application
- `requirements.txt` – Python dependencies
- `Dockerfile` – Docker build instructions
- `docker-compose.yml` – Docker Compose configuration

## Contributing
Pull requests are welcome! Please open an issue first to discuss major changes.

## License
This project is licensed under the MIT License.
