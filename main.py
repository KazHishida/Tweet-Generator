import get_tweets
import markov_chain
from socket import *
import argparse
import base64
import json

# Accept command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--ip')
parser.add_argument("--port")
parser.add_argument("--generate-model")
parser.add_argument("--load-folder")
parser.add_argument("--save-folder")
args = parser.parse_args()

# Initialize markov chain model
def initializeModel():
    if not args.generate_model:
        model = markov_chain.MarkovChain(initialize=False)
        model.loadModel(args.load_folder)
    else:
        tweets = get_tweets.returnTweets("tweet")
        print("finished loading tweets")
        model = markov_chain.MarkovChain(tweets=tweets)
        model.saveModel(args.save_folder)
    return model

if __name__ == '__main__':
    # Initialize Markov Chain
    model = initializeModel()
    # Create an IPv4 TCP socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Prepare a sever socket
    serverSocket.bind((args.ip, int(args.port)))  # second command line arg for port
    # Listen for connections from client
    serverSocket.listen(1)
    # Wait for instructions
    while True:
        # Establish connection
        print("Waiting...")
        connectionSocket, addr = serverSocket.accept()
        try:
            # Receive request and print
            message = connectionSocket.recv(2048)
            print(message.decode())
            try:
                # If request is a GET request:
                if message.decode('utf-8').split()[0] == "GET":
                    # Generate Input and encode in base64
                    input = model.generateInput()
                    b64Input = base64.b64encode(str.encode(input))
                    # Send encoded json input
                    newInput = json.dumps({'tweet': b64Input.decode('utf-8')})
                    connectionSocket.send(str.encode(newInput))
                # If request is a POST request:
                elif message.decode('utf-8').split()[0] == "POST":
                    # Print tweet
                    print(base64.b64decode(message.split()[1]).decode('utf-8'))
                    # Process input and send confirmation
                    model.processTokens([base64.b64decode(message.split()[1]).decode('utf-8')])
                    # Save new model
                    model.saveModel(args.save_folder)
                    connectionSocket.send(b'OK')  # send confirmation if successful
            except:
                connectionSocket.send(b'ERROR')
        except KeyboardInterrupt:  # User pressed Ctrl+C, exit gracefully
            break
    # Close server connection
    serverSocket.close()