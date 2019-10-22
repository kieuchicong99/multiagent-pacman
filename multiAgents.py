# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent


class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        PacPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # return successorGameState.getScore()

        foodList = []
        for x, row in enumerate(newFood):
          for y, col in enumerate(row):
            if newFood[x][y] is True: foodList.append((x, y))
        if len(foodList) > 0:
          dist = 0
          for index in range(len(newGhostStates)):
            GhostPos = newGhostStates[index].getPosition()
            dist = manhattanDistance(PacPos, GhostPos)
          # if (dist >2.0 and dist >=(float(newScaredTimes[0]))) :
          if (dist > 2.0):
            return 1.0/(min([manhattanDistance(PacPos, food) for food in foodList])) + successorGameState.getScore()
          # if (dist < (float(newScaredTimes[0])) and dist>2.0    ) :
          #   return 100
          if dist <= 2.0:
            return -100
        else:
          return successorGameState.getScore()
        print (newScaredTimes)


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        res = self.value(gameState, 0)
        
        # print(res[0])
        return res[0]


      
    def value(self, gameState, depth):
        if depth == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if depth % gameState.getNumAgents() == 0:
            return self.maxFunc(gameState, depth)
        else:
            return self.minFunc(gameState, depth)

    def minFunc(self, gameState, depth):
        actions = gameState.getLegalActions(depth % gameState.getNumAgents())
        if len(actions) == 0:
            return (None, self.evaluationFunction(gameState))

        min_val = (None, 1000000000000)
        for action in actions:
            succ = gameState.generateSuccessor(depth % gameState.getNumAgents(), action)
            res = self.value(succ, depth+1)
            if res[1] < min_val[1]:
                min_val = (action, res[1])
        return min_val

    def maxFunc(self, gameState, depth):
        actions = gameState.getLegalActions(0)
        if len(actions) == 0:
            return (None, self.evaluationFunction(gameState))

        max_val = (None, -10000000000000)
        for action in actions:
            succ = gameState.generateSuccessor(0, action)
            res = self.value(succ, depth+1)
            if res[1] > max_val[1]:
                max_val = (action, res[1])
        return max_val
       

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
          
        res = self.value(gameState, 0, -10000000000, 10000000000)
        return res[0]

    def value(self, gameState, depth, alpha, beta):
        if depth == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if depth % gameState.getNumAgents() == 0:
            return self.maxFunc(gameState, depth, alpha, beta)
        else:
            return self.minFunc(gameState, depth, alpha, beta)

    def minFunc(self, gameState, depth, alpha, beta):
        actions = gameState.getLegalActions(depth % gameState.getNumAgents())
        if len(actions) == 0:
            return (None, self.evaluationFunction(gameState))

        min_val = (None, 10000000000)
        for action in actions:
            succ = gameState.generateSuccessor(depth % gameState.getNumAgents(), action)
            res = self.value(succ, depth+1, alpha, beta)

            if res[1] < min_val[1]:
                min_val = (action, res[1])

            if min_val[1] < alpha:
                return min_val

            beta = min(beta, min_val[1])
        return min_val

    def maxFunc(self, gameState, depth, alpha, beta):
        actions = gameState.getLegalActions(0)
        if len(actions) == 0:
            return (None, self.evaluationFunction(gameState))

        max_val = (None, -10000000000)
        for action in actions:
            succ = gameState.generateSuccessor(0, action)
            res = self.value(succ, depth+1, alpha, beta)

            if res[1] > max_val[1]:
                max_val = (action, res[1])
            if max_val[1] > beta:
                return max_val

            alpha = max(alpha, max_val[1])
        return max_val



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        res = self.value(gameState, 0)
        return res[0]

    def value(self, gameState, depth):
        if depth == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if depth % gameState.getNumAgents() == 0:
            return self.maxValue(gameState, depth)
        else:
            return self.expValue(gameState, depth)

    def expValue(self, gameState, depth):
        actions = gameState.getLegalActions(depth % gameState.getNumAgents())
        if len(actions) == 0:
            return (None, self.evaluationFunction(gameState))

        probability = 1./len(actions)
        exp_val = 0
        for action in actions:
            succ = gameState.generateSuccessor(depth % gameState.getNumAgents(), action)
            res = self.value(succ, depth+1)
            exp_val += res[1] * probability
        return (None, exp_val)

    def maxValue(self, gameState, depth):
        actions = gameState.getLegalActions(0)
        if len(actions) == 0:
            return (None, self.evaluationFunction(gameState))

        max_val = (None, -10000000000)
        for action in actions:
            succ = gameState.generateSuccessor(0, action)
            res = self.value(succ, depth+1)
            if res[1] > max_val[1]:
                max_val = (action, res[1])
        return max_val

def betterEvaluationFunction(state):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    newPos = state.getPacmanPosition()
    newFood = state.getFood()
    newGhostStates = state.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

      #------------------------------
      # ghost scared calculations
      #------------------------------
    v = False
    v_gs = False
    bAreGhostsScared = False
    if newScaredTimes[0]>5:
      bAreGhostsScared = True
      if v_gs:
        print newScaredTimes
        print state.getCapsules()
        #raw_input()
      #------------------------------
      # food calculations
      #------------------------------
    food_dist = []
    food_avg_dist = 0
    food_min_dist = 0
    food_list = state.getFood().asList()
    if v: 
      print food_list
    for f in food_list:
      food_dist.append(manhattanDistance(newPos, f))
    if v :
       print 'distances: ' + str(food_dist)
    if len(food_dist)>0:
      food_avg_dist = sum(food_dist)/(len(food_dist)*1.0)
      food_min_dist = min(food_dist)

    if v :
      print 'average food distance: '+ str(food_avg_dist)
    food_inv_min = (2.0/food_min_dist)**2 if food_min_dist >0 else 0
    if bAreGhostsScared:
      food_inv_min = food_inv_min * 10
      #------------------------------
      # ghost calculations
      #------------------------------
    ghost_dist = []
    ghost_avg_dist = 0
    ghost_min_dist =0    
    for g in newGhostStates:
      ghost_dist.append(manhattanDistance(newPos,g.getPosition()))
      
    if len(ghost_dist)>0:
      ghost_avg_dist = sum(ghost_dist)/(len(ghost_dist)*1.0)
      ghost_min_dist = -2.0/min(ghost_dist) if min(ghost_dist)>0 else 0
      
      # if ghosts are too far away it is not so dangerous
    walls = state.getWalls()
    hypothenuse = ( (walls.width)**2 + (walls.height)**2 )**0.5
    if min(ghost_dist) > hypothenuse/5.0 and not bAreGhostsScared:
      ghost_min_dist = ghost_min_dist * 0* -1
    # Ghost are scared, pacman should be atracted by them
    if bAreGhostsScared:
      ghost_min_dist = ghost_min_dist * -10
    if v: 
      print 'average gost distance: '+str(ghost_avg_dist)
      
    s = state.getScore()
    
    return s + ghost_min_dist + food_inv_min

    


# Abbreviation
better = betterEvaluationFunction

