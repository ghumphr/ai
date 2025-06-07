# ai
Use LLM tools from the command line!

Usage: 

    ai.py [-h] [-e EXPRESSION] [-m MODEL] [-k API_KEY] [-f FILE] [-s SYSTEM]
    
    Send input to the Gemini API and output the response.
    
    options:
      -h, --help            show this help message and exit
      -e EXPRESSION, --expression EXPRESSION
                            Gemini prompt expression (if not using stdin or file).
      -m MODEL, --model MODEL
                            Gemini model to use. If not provided, uses the API's default model.
      -k API_KEY, --api_key API_KEY
                            Gemini API key. If not provided, uses GOOGLE_API_KEY environment variable.
      -f FILE, --file FILE  Input file path.
      -s SYSTEM, --system SYSTEM
                            System instructions for the model.

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
