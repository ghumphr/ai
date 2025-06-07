#!/usr/bin/env python3

import argparse
import sys
import os
import google.generativeai as genai

def ai(input_text, model, api_key, system_instruction=None):
    """Sends input_text to the Gemini API and returns the response."""
    genai.configure(api_key=api_key)
    if model:
        model_instance = genai.GenerativeModel(model)
    else:
        model_instance = genai.GenerativeModel()

    if system_instruction:
        contents = [
            {"role": "user", "parts": [system_instruction]},
            {"role": "model", "parts": ["Okay, I will follow those instructions."]} #basic acknowledgement
        ]
        chat = model_instance.start_chat(history=contents)
        response = chat.send_message(input_text)
    else:
        response = model_instance.generate_content(input_text)
    return response.text

def main():
    parser = argparse.ArgumentParser(description="Send input to the Gemini API and output the response.")
    parser.add_argument("-e", "--expression", help="Gemini prompt expression (if not using stdin or file).")
    parser.add_argument("-m", "--model", help="Gemini model to use. If not provided, uses the API's default model.")
    parser.add_argument("-k", "--api_key", help="Gemini API key. If not provided, uses GOOGLE_API_KEY environment variable.")
    parser.add_argument("-f", "--file", help="Input file path.")
    parser.add_argument("-s", "--system", help="System instructions for the model.")

    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("GOOGLE_API_KEY")

    if not api_key:
        print("Error: API key not provided. Use -k or set GOOGLE_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    if args.expression:
        input_text = args.expression
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                input_text = f.read().strip()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
    else:
        input_text = sys.stdin.read().strip()

    try:
        output_text = ai(input_text, args.model, api_key, args.system)
        print(output_text)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
