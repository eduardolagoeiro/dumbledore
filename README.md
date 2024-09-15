# Python CLI with Ollama Integration (GPU-enabled)

This project is a Python CLI that interacts with a local Ollama instance to run LLaMA2, using a Retrieval-Augmented Generation (RAG) setup. The database stores relevant documents that are used to augment the LLaMA2 model’s responses.

## Requirements

- Python 3.8
- Docker
- Docker Compose
- NVIDIA GPU with CUDA support (for GPU acceleration)
- NVIDIA Drivers and CUDA (for GPU setup)

## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone git@github.com:eduardolagoeiro/dumbledore.git
cd dumbledore
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

### Step 4: Enable GPU Support in Docker (Ubuntu)

If you want to use your GPU for accelerated model inference, follow these steps to set up GPU support in Docker.

1. Install NVIDIA Drivers
   Ensure your NVIDIA drivers are installed. You can check if the GPU is detected by running:

```bash
nvidia-smi
```

If it’s not installed, follow the installation instructions for NVIDIA drivers.

2. Install NVIDIA Container Toolkit
   Add the NVIDIA Docker repository:

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
```

Install the NVIDIA Container Toolkit:

```bash
sudo apt-get install -y nvidia-container-toolkit
```

Restart the Docker service:

```bash
sudo systemctl restart docker
```

3. Configure Docker to Use the NVIDIA Runtime

Open the Docker configuration file:

```bash
sudo nano /etc/docker/daemon.json
```

Add or update the configuration to include the NVIDIA runtime:

```json
{
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  }
}
```

Save the file and restart Docker:

```bash
sudo systemctl restart docker
```

Test if Docker can access your GPU by running:

```bash
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

If everything is set up correctly, this command should display the GPU details inside the container.

### Step 5: Start Ollama in Docker (With GPU Support)

Once GPU support is set up, you can start Ollama with Docker Compose:

Start the Ollama container:

```bash
docker-compose up -d
```

Verify GPU usage in the container:

```bash
docker exec -it <container_name> nvidia-smi
```

### Step 6: Install LLaMA2 in the Container

After starting the Ollama container, you can install the LLaMA2 model by entering the container and pulling the model:

Enter the Ollama container:

```bash
docker exec -it ollama-container-name bash
```

Inside the container, install the LLaMA2 model:

```bash
ollama pull llama2
```

Exit the container:

```bash
exit
```

### Step 7: Run the CLI

Once the environment is set up and the Ollama instance is running with LLaMA2 installed, you can start the CLI by running:

```bash
python cli.py
```

This will open the main menu of the CLI, where you can interact with GitHub repositories or start chatting with the AI model.

### Step 8: Stop Ollama

When you're done with the project, you can stop the Ollama Docker container:

```bash
docker-compose down
```

#### Troubleshooting GPU Issues

Check Docker Version: Make sure you are running Docker version 19.03 or higher to support GPU acceleration. You can check your Docker version by running:

```bash
docker --version
```

Verify GPU Access: If the GPU is not detected, verify that your NVIDIA drivers and CUDA are correctly installed. You can also run:

```bash
nvidia-container-cli info
```

This command will give detailed information about your system’s GPU configuration for containers.
