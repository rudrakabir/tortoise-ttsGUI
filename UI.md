# Tortoise TTS UI Guide

This guide provides basic instructions on how to install and run the Tortoise TTS Web UI.

## Prerequisites

- **Python**: You need Python installed (Python 3.9 or higher is recommended).
- **Git**: To clone the repository.
- **Anaconda/Miniconda** (Optional but recommended): For managing virtual environments.

## Installation

### 1. Clone the Repository

Open your terminal (Command Prompt, PowerShell, or Terminal on macOS/Linux) and run:

```bash
# Clone this repository
git clone <repository_url>
cd tortoise-tts
```

### 2. Set up a Python Environment (Recommended)

It is highly recommended to use a virtual environment to avoid conflicting dependencies.

**Using Conda:**

```bash
conda create --name tortoise python=3.9
conda activate tortoise
```

**Using venv (standard Python):**

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages.

**For macOS (Apple Silicon / M1 / M2 / M3):**

First, install the nightly version of PyTorch which has better support for Apple Silicon:

```bash
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
```

**For Windows / Linux (NVIDIA GPU):**

Install PyTorch with CUDA support (check [pytorch.org](https://pytorch.org/get-started/locally/) for the command matching your CUDA version), e.g.:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Then, install the rest of the requirements:**

```bash
pip install -r requirements.txt
```

> **Note:** If you encounter issues with `transformers` or `gradio`, ensure you have installed the versions specified in `requirements.txt`.

## Running the UI

Once installation is complete, you can start the Web UI.

1. Ensure your environment is activated (`conda activate tortoise` or `source venv/bin/activate`).
2. Run the UI script:

```bash
python start_ui.py
```

3. The script will initialize the model (this may take a few minutes the first time as it downloads model files).
4. Once ready, it will show a local URL (e.g., `http://127.0.0.1:7860`). Open this link in your web browser.

## Usage

- **Text**: Enter the text you want to convert to speech.
- **Voice**: Select a voice from the dropdown. "Random" will generate a random voice.
- **Quality Preset**:
    - `ultra_fast`: Fastest generation, lower quality.
    - `fast`: Good balance.
    - `standard`: Better quality, slower.
    - `high_quality`: Best quality, very slow.
- **Seed**: Optional. Enter a number to get reproducible results for the same text/voice.

Click **Generate Speech** and wait for the audio to appear. You can play it directly in the browser or download it.
