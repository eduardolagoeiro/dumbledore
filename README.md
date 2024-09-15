# Python CLI with Ollama Integration (GPU-enabled)

This project is a Python CLI that interacts with a local Ollama instance to run LLaMA, using a Retrieval-Augmented Generation (RAG) setup. The database stores relevant documents that are used to augment the LLaMA model’s responses.

## Requirements

- Python 3.10
- Docker
- Docker Compose
- Ollama

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone git@github.com:eduardolagoeiro/dumbledore.git
cd dumbledore
```

### Step 2: Set up a Python Virtual Environment

Create and activate the virtual environment using Python 3.8:

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the CLI

Once the environment is set up and the Ollama instance is running with LLaMA installed, you can start the CLI by running:

```bash
python cli.py
```

This will open the main menu of the CLI, where you can interact with GitHub repositories or start chatting with the AI model.
