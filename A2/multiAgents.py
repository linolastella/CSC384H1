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
import util
import random

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
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        distancesToFood = [manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()]
        distancesToGhosts = [manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newGhostStates]

        closestFood = min(distancesToFood) if len(distancesToFood) > 0 else 1

        if distancesToGhosts is not []:
            closestGhost = min(distancesToGhosts)
            return float(1) / ((11.1 * closestGhost ** -1 if closestGhost != 0 else 999) +
                               111.1 * len(newFood.asList()) +
                               5.5 * closestFood +
                               (sum(newScaredTimes) if sum(newScaredTimes) > 0 else 0))

        return float(3) / (closestFood ** -1 + 33 * len(newFood.asList()))


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
        def multi_agent_minimax(game_state, cur_agent, depth):
            best_move = None
            if game_state.isWin() or game_state.isLose() or depth == 0:
                return best_move, self.evaluationFunction(game_state)

            isPacman = cur_agent == 0
            isLastGhost = cur_agent == game_state.getNumAgents() - 1

            value = -float("inf") if isPacman else float("inf")

            all_actions = game_state.getLegalActions(cur_agent)
            for action in all_actions:
                next_state = game_state.generateSuccessor(cur_agent, action)

                if isLastGhost:
                    _, next_value = multi_agent_minimax(next_state, 0, depth - 1)
                else:
                    _, next_value = multi_agent_minimax(next_state, cur_agent + 1, depth)

                if isPacman and next_value > value:
                    value, best_move = next_value, action
                if not isPacman and next_value < value:
                    value, best_move = next_value, action

            return best_move, value

        return multi_agent_minimax(gameState, self.index, self.depth)[0]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def multi_agent_alpha_beta(game_state, cur_agent, depth, alpha, beta):
            best_move = None
            if game_state.isWin() or game_state.isLose() or depth == 0:
                return best_move, self.evaluationFunction(game_state)

            isPacman = cur_agent == 0
            isLastGhost = cur_agent == game_state.getNumAgents() - 1

            value = -float("inf") if isPacman else float("inf")

            all_actions = game_state.getLegalActions(cur_agent)
            for action in all_actions:
                next_state = game_state.generateSuccessor(cur_agent, action)

                if isLastGhost:
                    _, next_value = multi_agent_alpha_beta(next_state, 0, depth - 1, alpha, beta)
                else:
                    _, next_value = multi_agent_alpha_beta(next_state, cur_agent + 1, depth, alpha, beta)

                if isPacman:
                    if value < next_value:
                        value, best_move = next_value, action
                    if value >= beta:
                        return best_move, value
                    alpha = max(alpha, value)
                else:
                    if value > next_value:
                        value, best_move = next_value, action
                    if value <= alpha:
                        return best_move, value
                    beta = min(beta, value)

            return best_move, value

        return multi_agent_alpha_beta(gameState, self.index, self.depth, -float("inf"), float("inf"))[0]


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
        "*** YOUR CODE HERE ***"
        def multi_agent_expectimax(game_state, cur_agent, depth):
            best_move = None
            if game_state.isWin() or game_state.isLose() or depth == 0:
                return best_move, self.evaluationFunction(game_state)

            isPacman = cur_agent == 0
            isLastGhost = cur_agent == game_state.getNumAgents() - 1

            value = -99999 if isPacman else 0

            all_actions = game_state.getLegalActions(cur_agent)
            for action in all_actions:
                next_state = game_state.generateSuccessor(cur_agent, action)

                if isLastGhost:
                    _, next_value = multi_agent_expectimax(next_state, 0, depth - 1)
                else:
                    _, next_value = multi_agent_expectimax(next_state, cur_agent + 1, depth)

                if isPacman and next_value > value:
                    value, best_move = next_value, action
                if not isPacman:
                    value += next_value * len(all_actions) ** -1

            return best_move, value

        return multi_agent_expectimax(gameState, self.index, self.depth)[0]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:
      First, I store a bunch of useful information such as pacman position, food position, etc.
      Then, I compute some relative distances.
      Finally, I return some function of these numbers where the weights are calculated empirically (try and try and try...)
    """
    "*** YOUR CODE HERE ***"
    final_score = currentGameState.getScore()

    pacman_pos = currentGameState.getPacmanPosition()
    food_pos = currentGameState.getFood().asList()
    ghost_states = currentGameState.getGhostStates()
    scared_times = [ghostState.scaredTimer for ghostState in ghost_states]
    pellets_pos = currentGameState.getCapsules()

    distances_to_food = [manhattanDistance(pacman_pos, this_food) for this_food in food_pos]
    distances_to_ghosts = [manhattanDistance(pacman_pos, ghost_state.getPosition()) for ghost_state in ghost_states]
    distances_to_pellets = [manhattanDistance(pacman_pos, this_pellet) for this_pellet in pellets_pos]

    closest_food = min(distances_to_food) if len(distances_to_food) > 0 else 0
    closest_ghost = min(distances_to_ghosts) if len(distances_to_ghosts) > 0 else -100
    closest_pellet = min(distances_to_pellets) if len(distances_to_pellets) > 0 else 100

    # areas with plenty of food are good
    final_score += (99 * len(distances_to_food) + 5 * closest_food + 1) ** -1

    # areas with ghosts are dangerous, unless pacman ate a pellet
    if sum(scared_times) > 0:
        final_score += (45 * closest_ghost + 1000 * len(pellets_pos) + 121 * len(ghost_states) +
                        sum(scared_times) + 22 * closest_pellet) ** -1
    else:
        final_score -= 3 * (11 * closest_ghost + 89 * len(ghost_states) + 1) ** -1

    return final_score


# Abbreviation
better = betterEvaluationFunction
