from socket import *
import argparse
import tweepy
import json
import base64

# Set up twitter API
auth = tweepy.OAuthHandler('HSpiivW44gNpuSEkTmrVIbOVy', '3EwTkcxBNmlcBzrbfpS4A61jsUVOaOYlbM5ZjH7e7JHDh7SdiX')
auth.set_access_token('2956699122-VOnyhXkDCiV3hjGLAVCSzvrPb6zHIKEs89WvGpy', 'jNeculRn0RRfQ2a0riO0Ep5htt73luNZnpIeJGPgZMIpO')
api = tweepy.API(auth)

# Take command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--ip')
parser.add_argument("--port")
args = parser.parse_args()

# Loop and take commands
while True:
    # Take request
    request = input("Enter request:\n")
    # Connect to server
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((args.ip, int(args.port)))
    # GET request
    if request.split()[0] == "GET":
        # Request and receive generated tweet
        clientSocket.send(b'GET TWEET')
        message1 = json.loads(clientSocket.recv(2048))
        # Decode and print tweet
        translation = base64.b64decode(message1['tweet']).decode('utf-8')
        print(f"Tweet: {translation}")
        # Publish tweet to twitter?
        request2 = input("Publish? Y/N\n")
        if request2 == "Y":
            api.update_status(translation)
    # POST request
    elif request.split()[0] == "POST":
        # Send tweet to server and print response
        clientSocket.send(str.encode(f'POST {request[1]}'))
        message1 = clientSocket.recv(1024)
        print(message1.decode())
    else:
        break

clientSocket.close()
