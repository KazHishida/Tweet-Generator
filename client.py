from socket import *
import argparse
import tweepy
import json
import base64

auth = tweepy.OAuthHandler('HSpiivW44gNpuSEkTmrVIbOVy', '3EwTkcxBNmlcBzrbfpS4A61jsUVOaOYlbM5ZjH7e7JHDh7SdiX')
auth.set_access_token('2956699122-VOnyhXkDCiV3hjGLAVCSzvrPb6zHIKEs89WvGpy', 'jNeculRn0RRfQ2a0riO0Ep5htt73luNZnpIeJGPgZMIpO')

api = tweepy.API(auth)

parser = argparse.ArgumentParser()
parser.add_argument('--ip')
parser.add_argument("--port")
args = parser.parse_args()

while True:
    request = input("Enter request:\n")

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((args.ip, int(args.port)))

    if request.split()[0] == "GET":
        clientSocket.send(b'GET TWEET')
        message1 = json.loads(clientSocket.recv(2048))
        translation = base64.b64decode(message1['tweet']).decode('utf-8')
        print(f"Tweet: {translation}")
        request2 = input("Publish? Y/N\n")
        if request2 == "Y":
            api.update_status(translation)

    elif request.split()[0] == "POST":
        clientSocket.send(str.encode(f'POST {request[1]}'))
        message1 = clientSocket.recv(1024)
        print(message1.decode())

    else:
        break

clientSocket.close()
