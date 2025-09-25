import google.generativeai as genai
import os
import argparse
import json
import sys
from google.generativeai.types import content_types
from google.api_core.exceptions import GoogleAPIError

def save_history(chat_history, file_path, verbose=False):
    """
    Saves the chat history to a JSON file.
    
    Args:
        chat_history: The chat history object from the GenerativeModel.
        file_path: The path to the file where the history will be saved.
        verbose: If True, prints status messages.
    """
    try:
        # Convert history objects to a serializable list of dictionaries
        serializable_history = []
        for message in chat_history:
            parts = [part.text for part in message.parts]
            serializable_history.append({"role": message.role, "parts": parts})

        with open(file_path, 'w') as f:
            json.dump(serializable_history, f, indent=4)
        if verbose:
            print(f"Chat history saved to {file_path}", file=sys.stdout)
    except Exception as e:
        if verbose:
            print(f"Error saving chat history: {e}", file=sys.stderr)

def load_history(file_path, verbose=False):
    """
    Loads the chat history from a JSON file.
    
    Args:
        file_path: The path to the file to load the history from.
        verbose: If True, prints status messages.
    
    Returns:
        A list of Content objects for the chat history, or None if an error occurs.
    """
    try:
        with open(file_path, 'r') as f:
            serializable_history = json.load(f)

        # Convert the serializable list back to Content objects
        loaded_history = []
        for message in serializable_history:
            loaded_history.append(content_types.to_content(message))

        if verbose:
            print(f"Chat history loaded from {file_path}", file=sys.stdout)
        return loaded_history
    except FileNotFoundError:
        if verbose:
            print(f"Error: History file '{file_path}' not found.", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        if verbose:
            print(f"Error: Failed to decode JSON from '{file_path}'. File may be corrupted.", file=sys.stderr)
        return None
    except Exception as e:
        if verbose:
            print(f"An unexpected error occurred while loading history: {e}", file=sys.stderr)
        return None

def main():
    """
    Main function to run the chatbot interface.
    """
    # 1. Set up argument parsing
    parser = argparse.ArgumentParser(description="A chatbot that uses both system instructions and appends a prompt prefix to user queries.")
    parser.add_argument("-k", "--api-key", help="The Gemini API key to use.")
    parser.add_argument("-s", "--system-instruction", help="The system instruction to guide the model's behavior as a string.")
    parser.add_argument("-S", "--system-instruction-file", help="The path to a text file containing the system instruction.")
    parser.add_argument("-p", "--prompt-prefix", help="The text to prepend to each user query as a string.")
    parser.add_argument("-P", "--prompt-prefix-file", help="The path to a text file containing the text to prepend to each user query.")
    parser.add_argument("-m", "--model", default="gemini-1.5-flash", help="The name of the Gemini model to use.")
    parser.add_argument("--list-models", action="store_true", help="Lists the available Gemini models and exits.")
    parser.add_argument("-w", "--save-history", help="Path to a file to save the chat history to.")
    parser.add_argument("-l", "--load-history", help="Path to a file to load the chat history from.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enables verbose output for debugging and status messages.")
    
    # New mutually exclusive group for chat modes
    chat_mode_group = parser.add_mutually_exclusive_group()
    chat_mode_group.add_argument("-o", "--once", action="store_true", help="Reads a single prompt from stdin to EOF, gets a response, and exits.")
    chat_mode_group.add_argument("-c", "--chat", action="store_true", help="Starts an interactive chat loop.")

    # Mutually exclusive group for single prompt input
    single_prompt_group = parser.add_mutually_exclusive_group()
    single_prompt_group.add_argument("-e", "--expression", help="A single prompt to send to the model from the command line.")
    single_prompt_group.add_argument("-f", "--file", help="Path to a file containing a single prompt to send to the model from the command line.")

    args = parser.parse_args()

    # Check for mutually exclusive arguments (handled by argparse's group)
    if args.save_history and args.load_history:
        if args.verbose:
            print("Error: Cannot use --save-history and --load-history at the same time.", file=sys.stderr)
        return

    # 2. Determine the API Key
    api_key = args.api_key or os.environ.get("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)

    if not api_key:
        if args.verbose:
            print("Error: The Gemini API key was not provided.", file=sys.stderr)
            print("Please set it via the --api-key flag or the GOOGLE_API_KEY environment variable.", file=sys.stderr)
        return

    # 3. Handle the --list-models flag
    if args.list_models:
        if args.verbose:
            print("Available Gemini models for text generation:", file=sys.stdout)
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(f"  - {m.name}", file=sys.stdout)
        return

    # 4. Determine the System Instruction
    system_instruction = ""
    if args.system_instruction:
        system_instruction = args.system_instruction
    elif args.system_instruction_file:
        try:
            with open(args.system_instruction_file, 'r') as f:
                system_instruction = f.read().strip()
            if args.verbose:
                print(f"Loaded system instruction from {args.system_instruction_file}", file=sys.stdout)
        except FileNotFoundError:
            print(f"Error: System instruction file '{args.system_instruction_file}' not found.", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            with open("system_instructions.txt", 'r') as f:
                system_instruction = f.read().strip()
            if args.verbose:
                print("Loaded system instruction from default file 'system_instructions.txt'", file=sys.stdout)
        except FileNotFoundError:
            if args.verbose:
                print("No system instruction file found.", file=sys.stdout)
    
    # 5. Determine the Appended Rules
    prompt_prefix = ""
    if args.prompt_prefix:
        prompt_prefix = args.prompt_prefix
    elif args.prompt_prefix_file:
        try:
            with open(args.prompt_prefix_file, 'r') as f:
                prompt_prefix = f.read().strip()
            if args.verbose:
                print(f"Loaded prompt prefix from {args.prompt_prefix_file}", file=sys.stdout)
        except FileNotFoundError:
            print(f"Error: Prompt prefix file '{args.prompt_prefix_file}' not found.", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            with open("prompt_prefix.txt", 'r') as f:
                prompt_prefix = f.read().strip()
            if args.verbose:
                print("Loaded prompt prefix from default file 'prompt_prefix.txt'", file=sys.stdout)
        except FileNotFoundError:
            if args.verbose:
                print("No prompt prefix file found.", file=sys.stdout)

    try:
        # Initialize the GenerativeModel with the system instruction only if it's provided.
        model_kwargs = {}
        if system_instruction:
            model_kwargs['system_instruction'] = system_instruction
        model = genai.GenerativeModel(args.model, **model_kwargs)

        if args.verbose:
            print("Model and chat session initialized successfully.", file=sys.stdout)

        # Load chat history if specified
        if args.load_history:
            history = load_history(args.load_history, verbose=args.verbose)
            if history is not None:
                chat = model.start_chat(history=history)
            else:
                chat = model.start_chat()
                if args.verbose:
                    print("Starting a new chat session.", file=sys.stdout)
        else:
            chat = model.start_chat()

        # Handle --once mode (default)
        if not args.chat:
            args.once = True
            if args.expression or args.file:
                # The explicit prompt flags override stdin
                user_input = ""
                if args.expression:
                    user_input = args.expression
                else:
                    try:
                        with open(args.file, 'r') as f:
                            user_input = f.read().strip()
                        if args.verbose:
                            print(f"Loaded prompt from file: {args.file}", file=sys.stdout)
                    except FileNotFoundError:
                        print(f"Error: Prompt file '{args.file}' not found.", file=sys.stderr)
                        sys.exit(1)
            else:
                # Read from stdin until EOF
                user_input = sys.stdin.read().strip()
            
            if not user_input:
                if args.verbose:
                    print("No prompt provided. Exiting.", file=sys.stderr)
                return

            if prompt_prefix:
                modified_query = f"{prompt_prefix}\n{user_input}"
            else:
                modified_query = user_input
            
            if args.verbose:
                print(f"Sending query to model: {modified_query}", file=sys.stdout)

            response = chat.send_message(modified_query)

            if args.verbose:
                print(f"Bot: {response.text}", file=sys.stdout)
            else:
                print(response.text, file=sys.stdout)
            
            if args.save_history:
                save_history(chat.history, args.save_history, verbose=args.verbose)
            
            return

        # Handle --chat mode
        if args.chat:
            if args.verbose:
                print(f"Chatbot started using model '{args.model}'! Type 'exit' or 'quit' to end the conversation.", file=sys.stdout)
                print("-" * 50, file=sys.stdout)

            while True:
                try:
                    # Use sys.stderr.write for the prompt to avoid mixing with stdout output.
                    sys.stderr.write("You: ")
                    user_input = input()

                except EOFError:
                    if args.verbose:
                        print("\nEOF received, ending chat.", file=sys.stderr)
                    if args.save_history:
                        save_history(chat.history, args.save_history, verbose=args.stderr)
                    break

                if user_input.lower() in ['exit', 'quit']:
                    if args.verbose:
                        print("Ending chat. Goodbye!", file=sys.stdout)
                    if args.save_history:
                        save_history(chat.history, args.save_history, verbose=args.stderr)
                    break

                # Conditionally prepend the dynamic prefix to the user's query.
                if prompt_prefix:
                    modified_query = f"{prompt_prefix}\n{user_input}"
                else:
                    modified_query = user_input
                
                if args.verbose:
                    print(f"Sending query to model: {modified_query}", file=sys.stdout)
                
                response = chat.send_message(modified_query)

                if args.verbose:
                    print(f"Bot: {response.text}", file=sys.stdout)
                    print("-" * 50, file=sys.stdout)
                else:
                    print(response.text, file=sys.stdout)

                # Save history after each turn if enabled
                if args.save_history:
                    save_history(chat.history, args.save_history, verbose=args.stderr)

    except GoogleAPIError as e:
        print(f"A Gemini API error occurred: {e}", file=sys.stderr)
        if args.verbose:
            print("Please check your API key, model name, and network connection.", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        if args.verbose:
            print("Please review your arguments and setup.", file=sys.stderr)

if __name__ == "__main__":
    main()
