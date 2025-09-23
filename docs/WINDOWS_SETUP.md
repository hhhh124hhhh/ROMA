# Windows Setup Guide for SentientResearchAgent

This guide explains how to set up and run SentientResearchAgent on Windows.

## Prerequisites

1. **Docker Desktop**: Install Docker Desktop for Windows from [https://docs.docker.com/docker-for-windows/install/](https://docs.docker.com/docker-for-windows/install/)
2. **Node.js**: Install Node.js from [https://nodejs.org/](https://nodejs.org/)
3. **Python 3.12+**: Install Python 3.12 or later from [https://www.python.org/downloads/](https://www.python.org/downloads/)

## Installation Options

### Option 1: Docker Setup (Recommended)

The Docker setup is the easiest way to get started on Windows.

1. **Configure Environment Variables**:
   - Copy `.env.example` to `.env` in the project root
   - Edit `.env` and add your API keys and configuration

2. **Run Docker Setup**:
   ```cmd
   setup.bat --docker
   ```
   
   Or run the interactive setup:
   ```cmd
   setup.bat
   ```

3. **Alternative Docker Commands**:
   - Start Docker services: `docker\start-docker.bat`
   - Stop Docker services: `docker\stop-docker.bat`
   - View logs: `docker\logs-docker.bat`

### Option 2: Native Setup (Advanced)

For native installation on Windows, you'll need to manually install dependencies:

1. **Install Python Dependencies**:
   ```cmd
   pip install pdm
   pdm install
   ```

2. **Install Frontend Dependencies**:
   ```cmd
   cd frontend
   npm install
   ```

3. **Configure Environment**:
   - Copy `.env.example` to `.env`
   - Update with your API keys

## Running the Application

### With Docker (Recommended)

1. **Start Services**:
   ```cmd
   docker\start-docker.bat
   ```

2. **Access Services**:
   - Backend API: http://localhost:5000
   - Frontend: http://localhost:3000

3. **View Logs**:
   ```cmd
   docker\logs-docker.bat
   ```

4. **Stop Services**:
   ```cmd
   docker\stop-docker.bat
   ```

### With Native Installation

1. **Start Backend**:
   ```cmd
   quickstart.bat
   ```

2. **Access Services**:
   - Backend API: http://localhost:5000
   - Frontend: http://localhost:3000

## Configuration

### Environment Variables

Edit the `.env` file to configure:

- LLM Provider Keys (OpenAI, OpenRouter, etc.)
- E2B API Key for code execution
- AWS Credentials for S3 integration
- Server Configuration
- Logging Configuration

### S3 Integration

To enable S3 integration:

1. Set `S3_MOUNT_ENABLED=true` in `.env`
2. Configure AWS credentials in `.env`
3. Set `S3_BUCKET_NAME` to your S3 bucket name
4. Optionally change `S3_MOUNT_DIR` (default: `/opt/sentient`)

## Troubleshooting

### Common Issues

1. **Docker not starting**:
   - Ensure Docker Desktop is running
   - Check Docker logs for error messages
   - Verify sufficient system resources

2. **Port conflicts**:
   - Ensure ports 5000 and 3000 are not in use
   - Modify port mappings in `docker-compose.yml` if needed

3. **Frontend not loading**:
   - Wait for the frontend to compile (check logs)
   - Ensure the backend is running and accessible

### Windows-Specific Issues

1. **Long Path Issues**:
   - Enable long path support in Windows Group Policy
   - Or move the project to a shorter path (e.g., `C:\roma`)

2. **File Permissions**:
   - Run scripts as Administrator if needed
   - Ensure proper write permissions for project directories

## Useful Commands

### Docker Management

```cmd
# Start services
docker\start-docker.bat

# Stop services
docker\stop-docker.bat

# View logs
docker\logs-docker.bat

# Rebuild images
cd docker
docker compose build --no-cache
```

### Native Management

```cmd
# Activate virtual environment
.venv\Scripts\activate.bat

# Run backend
python -m sentientresearchagent

# Run frontend (from frontend directory)
npm run dev
```

## E2B Integration

To set up E2B code execution:

1. Add `E2B_API_KEY` to `.env`
2. Run setup:
   ```cmd
   setup.bat --e2b
   ```
3. Test integration:
   ```cmd
   setup.bat --test-e2b
   ```

## Make Commands (if using WSL or Git Bash)

If you have WSL or Git Bash installed, you can also use the Makefile:

```bash
# Docker setup
make setup-docker

# Run backend
make run

# Run frontend
make frontend-dev

# View logs
make logs
```