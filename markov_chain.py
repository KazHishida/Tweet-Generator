import random
import json

maxOrder = 3 # Maximum order for variable order markov chain

class MarkovChain():
    def __init__(self, tweets=None, initialize=True):
        self.tweets = tweets
        self.model = {}
        self.initialStates = []
        # Create a list of tweets tokenized by word, then process it to add to markov chain
        if initialize:
            tokenList = [tweet['text'].split() for tweet in self.tweets]
            self.processTokens(tokenList)
    def processTokens(self, tokenList):
        '''
        Going through every word in every tweet in list, add states to the model
        '''
        for order in range(maxOrder):
            for tweet in tokenList:
                self.initialStates.append(tweet[0])
                for tokenIndex in range(len(tweet) - order):
                    state = ' '.join(tweet[tokenIndex:tokenIndex + order])
                    nextState = tweet[tokenIndex + order]
                    self.addToModel(state, nextState)
                self.addToModel(tweet[-1], None)
    def addToModel(self, state, nextState):
        '''
        Given the initial state and next state, add to model
        '''
        if state not in self.model:
            self.model[state] = {}
        if nextState not in self.model[state]:
            self.model[state][nextState] = 0
        self.model[state][nextState] += 1
    def generateInput(self):
        '''
        Generate a random input given the model and list of possible initial states
        '''
        # Initialize text as list containing a random initial state
        text = [random.choice(self.initialStates)]
        # Main loop to create string
        while True:
            for order in range(-maxOrder, 0):
                initialState = ' '.join(text[order:len(text)])
                if initialState in self.model and sum(self.model[initialState].values()) > 1:
                    break
            # Create list of potential states and probabilities
            nextStates = list(self.model[initialState].keys())
            nextProbs = list(self.model[initialState].values())
            # Select the next state using nextStates and nextProbs
            nextState = random.choices(nextStates, nextProbs)[0]
            # Check if None, if not, append, if so, break
            if not nextState or nextState=='null':
                break
            else:
                text.append(nextState)
        # Convert list to text and return
        return ' '.join(text)
    # Save and load models given folder name to store models in
    def saveModel(self, modelLocation):
        with open(f'{modelLocation}\model.txt', 'w', encoding='utf-8') as outfile:
            json.dump(self.model, outfile)
        with open(f'{modelLocation}\initialStates.txt', 'w', encoding='utf-8') as outfile:
            json.dump(self.initialStates, outfile)
    def loadModel(self, modelLocation):
        with open(f'{modelLocation}\model.txt', 'r', encoding='utf-8') as outfile:
            self.model = json.load(outfile)
        with open(f'{modelLocation}\initialStates.txt', 'r', encoding='utf-8') as outfile:
            self.initialStates = json.load(outfile)