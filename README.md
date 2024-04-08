# cli-gpt
A client for the openai api that works from terminal

## Usage
Default:
- Use "chat some question or other text" to send input to openai api and output response
Saves previous messages by default so that you can have an ongoing conversation between commands.

Other args:
- new: creates new conversation
- conv: outputs previous conversation
- key: changes api-key


## Other Ideas:
- support for other llms, maybe local or custom endpoints
- when called with no message, use stdin (for pipe support)
- instruction parameter to use with pipe
- code parameter that takes an instruction and ensures that the output is only code
