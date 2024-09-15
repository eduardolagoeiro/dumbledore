# Python CLI with Ollama Integration

This project is a Python CLI that interacts with a local Ollama instance to run LLaMA2, using a Retrieval-Augmented Generation (RAG) setup. The database stores relevant documents that are used to augment the LLaMA2 model’s responses.

## Requirements

- Python 3.8
- Docker
- Docker Compose

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```

### Step 2: Set up a Python Virtual Environment

Create and activate the virtual environment using Python 3.8:

```bash
python3.8 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Start Ollama in Docker

The project uses Ollama to run the LLaMA2 model locally. You need to set up and run Ollama using Docker.

Start the Ollama container using Docker Compose:

```bash
docker-compose up -d
```

Enter the running Ollama container:

```bash
docker exec -it ollama-container-name bash
```

Inside the container, install the LLaMA2 model:

```bash
ollama pull llama2
```

### Step 5: Run the CLI

Once the virtual environment is set up, and the Ollama instance is running with LLaMA2 installed, you can start the CLI by running:

```bash
python cli.py
```
