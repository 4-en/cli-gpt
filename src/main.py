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

    parser.add_argument('instruction', nargs='*', help='The instruction to the model')

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



def main():
    args = get_args()
    