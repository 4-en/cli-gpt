import argparse
import os
import sys
import platform
from pathlib import Path


from utils.config import Config

def get_args(args=None):
    # parse optional arguments and then main instruction as string
    # eg. python main.py --new --code this is some instruction

    parser = argparse.ArgumentParser(description='Chat with a language model using the terminal')

    parser.add_argument('-n', '--new', action='store_true', help='Starts a new conversation')
    parser.add_argument('-c', '--code', type=str, help='Forces the model to generate code')
    parser.add_argument('--conv", "--conversation', type=str, help='Prints the conversation so far')
    parser.add_argument('-k', '--key', type=str, help='Sets the API-key for models that require it')
    parser.add_argument('-i', '--instruction', type=str, help='Sets a custom instruction for the model')

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

import time
def get_conversation(data_dir):
    current_time = int(time.time())

def get_prompt(args_prompt=None):
    # get prompt from args
    prompt = " ".join(args_prompt)

    # check if prompt is empty
    if prompt == "":
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




def main():
    # get args
    args = get_args()

    # set instruction
    instruction = "You are a chatbot and are supposed to answer questions in a few sentences."

    # get prompt
    prompt = get_prompt(args.prompt)

    # get data directory
    data_dir = get_data_dir()

    # get config
    config = Config(data_dir / "config.ini")

    # get last conversation
    last_conversation_time = 0
    # TODO: get last conversation time from config and load conversation if it exists

    # get history
    history = ["What is the capital of France?", "The capital of France is Paris."]

    # combine history and prompt
    predict_prompt = "\n".join(history) + "\n" + prompt

    # get model connection
    model = None

    # generate response
    response = "This is a dummy response."
    # response = model.predict(instruction, prompt)



    