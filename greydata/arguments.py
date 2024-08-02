import argparse
import json

def setup_arguments(config_file='config.json'):
    """
    Set up and parse command line arguments based on the configuration from a JSON file.

    Args:
        config_file (str): Path to the JSON configuration file containing argument information.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    # Open and load the configuration from the JSON file
    with open(config_file, 'r', encoding='utf-8') as file:
        arguments = json.load(file)

    # Initialize the argument parser
    parser = argparse.ArgumentParser(description='Parse command line arguments.')

    # Mapping of types from string in JSON to Python types
    type_mapping = {
        'str': str,
        'int': int,
        'float': float,
        'bool': bool
    }

    # Add arguments to the parser based on the configuration
    for arg in arguments:
        name = arg.get('name')          # Argument name
        short = arg.get('short')        # Short form of the argument
        arg_type = type_mapping.get(arg.get('type', 'str'), str)  # Type of the argument
        default = arg.get('default')    # Default value
        help_text = arg.get('help', '') # Help text
        choices = arg.get('choices')    # Allowed choices, if any

        # Add the argument to the parser
        if choices:
            parser.add_argument(f'-{short}', f'--{name}', type=arg_type, default=default, help=help_text, choices=choices)
        else:
            parser.add_argument(f'-{short}', f'--{name}', type=arg_type, default=default, help=help_text)

    # Parse and return the command line arguments
    return parser.parse_args()
