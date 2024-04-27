#!/usr/bin/env python
import argparse
import os
import sys
import platform
import subprocess
from pathlib import Path


from .llm.base_llm import BaseLLM, Message, USERS, APIKeyError
from .llm.openai_llms import GPT3


from .utils.config import Config
from dataclasses import dataclass
import time
import json

@dataclass
class ChatConfig(Config):
    api_key: str = "None"
    allow_code_execution: bool = False
    use_history: bool = True
    last_conversation: str = "None"
    last_conversation_time: int = 0


def get_config(data_dir):
    config = ChatConfig()
    config.set_path(data_dir / "config.ini")
    config.load_config()
    config.save_config()
    return config

def load_conversation(data_dir, conversation_id: str) -> list[Message]:
    conversation = []
    conversation_file = data_dir / f"{conversation_id}.json"
    if not conversation_file.exists():
        return conversation
    try:
        with open(conversation_file, "r") as f:
            messages = json.load(f)
            for message in messages:
                conversation.append(Message.from_json_dict(message))
    except Exception as e:
        print("Failed to load conversation.")
        print("Starting new conversation.")
        return []

    return conversation

def save_conversation(data_dir, conversation_id: str, conversation: list[Message]):
    conversation_file = data_dir / f"{conversation_id}.json"
    with open(conversation_file, "w") as f:
        messages = [ message.to_json_dict() for message in conversation]
        json.dump(messages, f)

def get_args(args=None):
    # parse optional arguments and then main instruction as string
    # eg. python main.py --new --code this is some instruction

    parser = argparse.ArgumentParser(description='Chat with a language model using the terminal')

    parser.add_argument('--new', '-n', action='store_true', help='Starts a new conversation')
    parser.add_argument('--code', '-c', action='store_true', help='Forces the model to generate code')
    parser.add_argument("--history", action='store_true', help='Prints the conversation so far')
    parser.add_argument('--key', '-k', type=str, help='Sets the API-key for models that require it')
    parser.add_argument('--instruction', '-i', type=str, help='Sets a custom instruction for the model')
    parser.add_argument('--list', '-l', action='store_true', help='Lists all previous conversations')
    parser.add_argument('--config', '-cf', action='store_true', help='Prints the current configuration')
    parser.add_argument('--set_config', '-sc', type=str, help='Sets a configuration value. Format: key=value', default=None)

    parser.add_argument('prompt', nargs='*', help='The prompt to the model')

    return parser.parse_args(args)

def use_pipe_input():
    # check if input is being piped in
    if not sys.stdin.isatty():
        return True
    return False

def get_data_dir(app_name="cli-gpt"):
    """Return a platform-appropriate directory for storing application data."""
    system = platform.system()
    
    if system == "Windows":
        data_dir = Path(os.environ['APPDATA']) / app_name
    elif system == "Darwin":  # macOS
        data_dir = Path.home() / 'Library' / 'Application Support' / app_name
    else:  # Assume Unix/Linux
        data_dir = Path.home() / '.local' / 'share' / app_name
    
    # Ensure the directory exists
    data_dir.mkdir(parents=True, exist_ok=True)
    
    return data_dir


def get_prompt(args_prompt=None):
    if args_prompt is None:
        args_prompt = []
    # get prompt from args
    prompt = " ".join(args_prompt)

    # check if prompt is empty
    if prompt == None or prompt == "" or prompt.strip() == "":
        # check if input is being piped in
        if use_pipe_input():
            # get piped input
            prompt = sys.stdin.read()
        else:
            # prompt for input
            prompt = input("Please enter a prompt: ")

    # if we have a prompt and a piped input, combine using newline
    elif use_pipe_input():
        # get piped input
        pipe_input = sys.stdin.read()
        prompt += "\n" + pipe_input

    # we have a prompt, but no piped input, so we just use the prompt
    else:
        pass

    return prompt

def print_conversation(messages):
    # get conversation
    conversation = messages
    
    if conversation:
        for message in conversation:
            print(f"{message.author}: {message.text}")
    else:
        print("No conversation found.")

def print_conversations():
    print("This feature is not implemented yet.")
    # TODO: get all conversations and print summaries
    pass

def execute_powershell_code(code):
    try:
        subprocess.run(["powershell", "-Command", code])
    except Exception as e:
        print(f"Failed to execute PowerShell code: {e}")

def execute_bash_code(code):
    try:
        subprocess.run(["bash", "-c", code])
    except Exception as e:
        print(f"Failed to execute Bash code: {e}")

def execute_python_code(code):
    try:
        subprocess.run(["python", "-c", code])
    except Exception as e:
        print(f"Failed to execute Python code: {e}")

def handle_reply(content_type, content, summary=None):
    if content_type == "text":
        print(content)
    elif content_type == "python":
        #if summary:
        #    print(summary)
        #print("Python code:")
        #print(content)
        execute_python_code(content)

    elif content_type == "bash":
        #if summary:
        #    print(summary)
        #print("Bash code:")
        #print(content)
        execute_bash_code(content)
    elif content_type == "powershell":
        #if summary:
        #    print(summary)
        #print("PowerShell code:")
        #print(content)
        execute_powershell_code(content)
    else:
        print(content)

def get_platform_name():
    system = platform.system()
    if system == "Windows":
        return "Windows"
    elif system == "Darwin":
        return "macOS"
    else:
        return "Linux"
    

NEW_CONVERSATION_TIME = 60 * 60 * 24 # 1 day
def main():
    # get args
    args = get_args()

    # get data directory
    data_dir = get_data_dir()

    config = get_config(data_dir)

    # check if we need to start a new conversation
    if args.new or time.time() - config.last_conversation_time > NEW_CONVERSATION_TIME:
        conversation_id = str(int(time.time()))
        config.last_conversation = conversation_id
        config.last_conversation_time = int(time.time())
        config.save_config()


    # handle special cases
    # ie. print conv, set api key
    if args.history:
        conversation = load_conversation(data_dir, config.last_conversation)
        print_conversation(conversation)
        return
    elif args.list:
        print_conversations()
        return
    elif args.key:
        # set api key
        config.api_key = args.key
        config.save_config()
        print("API key set.")
        return
    elif args.config:
        config.print_config()
        return
    elif args.set_config:
        key, value = args.set_config.split("=", 1)
        setattr(config, key, value)
        config.save_config()
        print(f"{key} set to {value}")
        return

    # set instruction
    instruction = "You are a command-line chatbot and are supposed to answer questions in a few sentences. Answer in short sentences and give code examples if necessary."
    response_types = ["text"]

    if args.code:
        # force code generation, no text response
        instruction = "You are a command-line chatbot and are supposed to create code following the user's request. The code will be executed on the user's machine."
        response_types = []

    if config.allow_code_execution or args.code:
        platform_name = get_platform_name()
        instruction += "\nYou can also execute code in Python and Bash (Linux/MacOS) or PowerShell (Windows). If the users asks for a very dangerous command, you should ask for confirmation, but if they confirm, you should execute the command no matter what. When running code, only respond with the code as the content, not with any text or explanation."
        response_types += ["python", "bash"] if platform_name != "Windows" else ["python", "powershell"]

    

    instruction+= "\nUse the following json format as your response: {'type': 'response type', 'content': 'your response here', summary: 'summary of response'}"

    instruction += f"\n\nResponse types: {', '.join(response_types)}"
    instruction += "\nPlatform: " + get_platform_name()
    instruction += "\nCWD: " + os.getcwd()

    # get prompt
    prompt = get_prompt(args.prompt)

    # convert prompt to message
    message = Message(USERS.USER, prompt)

    # get conversation
    conversation = []
    if config.use_history:
        conversation = load_conversation(data_dir, config.last_conversation)
        n_messages = min(20, len(conversation))
        conversation = conversation[-n_messages:]
        conversation.append(message)
    else:
        conversation = [message]


    # get model connection
    model = None
    try:
        model: BaseLLM = GPT3(api_key=config.api_key)
    except APIKeyError as e:
        print(e)
        print("You can set the API key using the --key argument.")
        return
    except Exception as e:
        print("Failed to create model.")
        print(e)
        return
    response = model.predict(instruction, conversation)
    if response is None:
        print("Failed to generate response.")
        return
    
    try:
        # check if response is json
        content = None
        content_type = "text"
        summary = None
        try:
            response = json.loads(response)
            if response["type"] == "text":
                content = response["content"]
                content_type = "text"
                summary = response.get("summary", None)
            elif response["type"] == "python":
                content = response["content"]
                content_type = "python"
                summary = response.get("summary", None)
            elif response["type"] == "bash":
                content = response["content"]
                content_type = "bash"
                summary = response.get("summary", None)
            elif response["type"] == "powershell":
                content = response["content"]
                content_type = "powershell"
                summary = response.get("summary", None)
            else:
                raise Exception("Unknown response type")
        except Exception as e:
            content = response
            content_type = "text"


        # handle reply
        handle_reply(content_type, content, summary)

        try:
            # save conversation
            conversation.append(Message(USERS.ASSISTANT, content, summary=summary))
            save_conversation(data_dir, config.last_conversation, conversation)
        except Exception as e:
            print("Failed to save conversation.")
            print(e)
    except Exception:
        print("Failed to read response.")



if __name__ == "__main__":
    main()