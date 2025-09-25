# ai
    Use LLM tools from the command line!
    
    Usage: ai.py [-h] [-k API_KEY] [-s SYSTEM_INSTRUCTION] [-S SYSTEM_INSTRUCTION_FILE] [-p PROMPT_PREFIX]
                 [-P PROMPT_PREFIX_FILE] [-m MODEL] [--list-models] [-w SAVE_HISTORY] [-l LOAD_HISTORY] [-v] [-o | -c]
                 [-e EXPRESSION | -f FILE]
    
    A chatbot that can both use system instructions and append a prompt prefix to user queries.
    
    options:
      -h, --help            show this help message and exit
      -k API_KEY, --api-key API_KEY
                            The Gemini API key to use.
      -s SYSTEM_INSTRUCTION, --system-instruction SYSTEM_INSTRUCTION
                            The system instruction to guide the model's behavior as a string.
      -S SYSTEM_INSTRUCTION_FILE, --system-instruction-file SYSTEM_INSTRUCTION_FILE
                            The path to a text file containing the system instruction.
      -p PROMPT_PREFIX, --prompt-prefix PROMPT_PREFIX
                            The text to prepend to each user query as a string.
      -P PROMPT_PREFIX_FILE, --prompt-prefix-file PROMPT_PREFIX_FILE
                            The path to a text file containing the text to prepend to each user query.
      -m MODEL, --model MODEL
                            The name of the Gemini model to use.
      --list-models         Lists the available Gemini models and exits.
      -w SAVE_HISTORY, --save-history SAVE_HISTORY
                            Path to a file to save the chat history to.
      -l LOAD_HISTORY, --load-history LOAD_HISTORY
                            Path to a file to load the chat history from.
      -v, --verbose         Enables verbose output for debugging and status messages.
      -o, --once            Reads a single prompt from stdin to EOF, gets a response, and exits.
      -c, --chat            Starts an interactive chat loop.
      -e EXPRESSION, --expression EXPRESSION
                            A single prompt to send to the model from the command line.
      -f FILE, --file FILE  Path to a file containing a single prompt to send to the model from the command line.
    
    
    Example:
    
        $ python3 ai.py -s "Output only the usernames and user IDs with a colon delimiter." < passwd 
        root:0
        daemon:1
        bin:2
        sys:3
        sync:4
        games:5
        man:6
        lp:7
        mail:8
        news:9
        uucp:10
        proxy:13
        www-data:33
        backup:34
        list:38
        irc:40
        gnats:41
        nobody:65534
        testuser:1000
        anotheruser:1001
