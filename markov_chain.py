import random
maxOrder = 3

class MarkovChain():
    def __init__(self, tweets):
        self.tweets = tweets
        self.model = {}
        self.initialStates = []
        # Create a list of tweets tokenized by word, then process it to add to markov chain
        tokenList = [tweet['text'].split() for tweet in self.tweets]
        self.processTokens(tokenList)
    def processTokens(self, tokenList):
         for order in range(maxOrder):
            for tweet in tokenList:
                self.initialStates.append(tweet[0])
                for tokenIndex in range(len(tweet)-order):
                    state = ' '.join(tweet[tokenIndex:tokenIndex+order])
                    nextState = tweet[tokenIndex+order]
                    self.addToModel(state, nextState)
                self.addToModel(tweet[-1], None)
    def addToModel(self, state, nextState):
        if state not in self.model:
            self.model[state] = {}
        if nextState not in self.model[state]:
            self.model[state][nextState] = 0
        self.model[state][nextState] += 1
    def generateInput(self):
        # Initialize text as list containing a random initial state
        text = [random.choice(self.initialStates)]
        # Main loop to create string
        while True:
            for order in range(-maxOrder, 0):
                initialState = ' '.join(text[order:len(text)])
                if initialState in self.model and sum(self.model[initialState].values())>2:
                    break
            # Create list of potential states and probabilities
            nextStates = list(self.model[initialState].keys())
            nextProbs = list(self.model[initialState].values())
            # Select the next state using nextStates and nextProbs
            nextState = random.choices(nextStates, nextProbs)[0]
            print(f'Chosen word: {nextState} from {initialState} out of {self.model[initialState]}')
            # Check if None, if not, append, if so, break
            if nextState:
                text.append(nextState)
            else:
                break
        # Convert list to text and return
        return ' '.join(text)