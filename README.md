# Tweet Generator

Initially designed to create a parody Trump twitter account, this project uses a simple variable order markov chain trained on a large corpus of tweets. The model is implemented on a simple TCP socket server, allowing it to be constantly updated with new tweets, and allowing users to generate tweets off the server at any time. The model can also be saved and loaded from a given directory. This can be done with GET/POST requests detailed later on. The client script that is included makes making these requests simple, as well as allowing users to use the Twitter API to automatically publish these tweets. This will be updated to incorporate streaming, so the model can be constantly updated in real time using Twitter's Streaming API.

## Invoking Server

To run the server, run the script from the command line using the following flags:
```bash
main.py --ip (IP) --port (PORT) --load-model (OPTIONAL, FOLDER NAME) --save-model (OPTIONAL, FOLDER NAME) --generate-model (OPTIONAL, Default = False, True/False)
```
This will run the server on the given IP/Port, and will load/save the model on their respective given directories. If generate-model is set to True, this will generate a new model rather than load a new model, making that flag optional. If no folders are given, the models will be saved/loaded out of the directory the script is run from.

## Using client.py

Initialize the client script by running from the command line,
```bash
py client.py --ip (IP) --port (PORT)
```
This will be followed by an input request for a command. To this, respond with either GET or POST (b64 encoded tweet) to either request a tweet or update the model with a new tweet. The model will automatically save to the given directory after every update, and can be loaded back in later if the server needs to be restarted.
