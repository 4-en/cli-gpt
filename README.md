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
pip install git+https://github.com/4-en/cli-gpt.git
```

## Usage

Once installed, you can run the chatbot using one of the following commands from the terminal:

```bash
ask
```

```bash
cli-gpt
```

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

1. **Ask Anything:**

   ```bash
   ask Who are you?
   >> I am a command-line chatbot here to help you with any questions you may have.
   ```

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

4. **FFmpeg Magic:**

   ```bash
   ask -n -c "Convert the file demo.mkv to a new .mp4 file that starts at 1min and ends at 2min, while also having a size of 640x640, cropped from the original center."
   ffmpeg version 5.0.1-essentials_build-www.gyan.dev Copyright (c) 2000-2022 the FFmpeg developers
     built with gcc 11.2.0 (Rev7, Built by MSYS2 project)
   
   // ...removed some ffmpeg output...
     
   frame= 1439 fps=400 q=-1.0 Lsize=    3262kB time=00:01:00.00 bitrate= 445.4kbits/s speed=16.7x
   video:2239kB audio:962kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 1.904760%
   
   // ...removed some ffmpeg output...
   
   [libx264 @ 0000023f34350840] kb/s:305.52
   [aac @ 0000023f3460c200] Qavg: 546.231
   ```
   (actually worked)

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
