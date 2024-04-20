# CLI-GPT Chatbot

CLI-GPT is a command-line interface chatbot that leverages large language models (LLM) such as GPT-3 to interact with users. This tool allows you to have real-time text conversations with an AI, manage conversation histories, and optionally execute code in different scripting environments based on user permissions.

## Features

- Real-time text interaction with a GPT-based model.
- Ability to start new conversations or list past ones.
- Optional code execution capabilities in Python, Bash (on Linux/macOS), or PowerShell (on Windows).
- Configuration of API keys and user settings via a local config file.

## Installation

To install CLI-GPT, you will need Python installed on your system. You can then install this project directly from the GitHub repository using pip:

```bash
pip install git+https://github.com/yourusername/cli-gpt.git
```

Replace `https://github.com/yourusername/cli-gpt.git` with the actual URL of your repository.

## Usage

Once installed, you can run the chatbot using the following command from the terminal:

```bash
python -m cli_gpt
```

### Command Line Arguments

- `-n, --new`: Starts a new conversation.
- `-c, --code`: Forces the model to generate code.
- `--history`: Prints the conversation so far.
- `-k, --key`: Sets the API-key for models that require it.
- `-i, --instruction`: Sets a custom instruction for the model.
- `-l, --list`: Lists all previous conversations.
- `prompt`: The prompt to the model.

### Examples

1. **Starting a New Conversation:**

   ```bash
   python -m cli_gpt --new "Hello, how are you?"
   ```

2. **Print Conversation History:**

   ```bash
   python -m cli_gpt --history
   ```


3. **Setting an API Key:**

   ```bash
   python -m cli_gpt --key "your-api-key"
   ```

## Configuration

On the first run, the application will generate a default configuration file in a platform-appropriate application data directory. You can modify this configuration file to set the API key permanently or change other settings like allowing code execution.


## Other Ideas:
- support for other llms, maybe local or custom endpoints
- when called with no message, use stdin (for pipe support)
- instruction parameter to use with pipe
- code parameter that takes an instruction and ensures that the output is only code
- detected if used with pipe, use message as instruction and pipe input as content
- kinda risky: output python code and execute automatically
  - eg: "crop all images in the directory abc to 512x512" -> python gpt-code.py
