# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


# noinspection PyClassHasNoInit
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


# noinspection PyUnusedLocal
def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    Open = util.Stack()
    Open.push(([problem.getStartState()], []))
    # Open contains tuples (array of states + sequence of actions from start state)

    while not Open.isEmpty():
        ThisNode = Open.pop()

        StatesInThisNode = ThisNode[0]
        ActionsSoFar = ThisNode[1]
        ThisState = StatesInThisNode[-1]

        if problem.isGoalState(ThisState):
            return ActionsSoFar
        for Succ in problem.getSuccessors(ThisState):
            if not Succ[0] in StatesInThisNode:
                Open.push((StatesInThisNode + [Succ[0]], ActionsSoFar + [Succ[1]]))

    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    Open = util.Queue()
    Open.push(([problem.getStartState()], []))
    # Same as depthFirstSearch

    Seen = {problem.getStartState(): 0}
    CostFn = problem.getCostOfActions

    while not Open.isEmpty():
        ThisNode = Open.pop()

        StatesInThisNode = ThisNode[0]
        ActionsSoFar = ThisNode[1]
        ThisState = StatesInThisNode[-1]
        if CostFn(ActionsSoFar) <= Seen[ThisState]:
            if problem.isGoalState(ThisState):
                return ActionsSoFar
            for Succ in problem.getSuccessors(ThisState):
                if Succ[0] not in Seen or CostFn(ActionsSoFar + [Succ[1]]) < Seen[Succ[0]]:
                    Open.push((StatesInThisNode + [Succ[0]], ActionsSoFar + [Succ[1]]))
                    Seen[Succ[0]] = CostFn(ActionsSoFar + [Succ[1]])

    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    def CostFn(Node):
        if hasattr(problem, "costFn"):
            return sum(problem.costFn(State) for State in Node[0])
        return problem.getCostOfActions(Node[1])

    Open = util.PriorityQueueWithFunction(CostFn)

    StartNode = ([problem.getStartState()], [])
    Open.push(StartNode)
    # Same as depthFirstSearch

    Seen = {StartNode[0][0]: CostFn(StartNode)}

    while not Open.isEmpty():
        ThisNode = Open.pop()

        StatesInThisNode = ThisNode[0]
        ActionsSoFar = ThisNode[1]
        ThisState = StatesInThisNode[-1]

        if CostFn(ThisNode) <= Seen[ThisState]:
            if problem.isGoalState(ThisState):
                return ActionsSoFar
            for Succ in problem.getSuccessors(ThisState):
                NewNode = (StatesInThisNode + [Succ[0]], ActionsSoFar + [Succ[1]])
                if Succ[0] not in Seen or CostFn(NewNode) < Seen[Succ[0]]:
                    Open.push(NewNode)
                    Seen[Succ[0]] = CostFn(NewNode)
    return []


# noinspection PyUnusedLocal
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    g = problem.getCostOfActions
    h = heuristic

    EvalFunc = lambda Node: (g(Node[1]) + h(Node[0][-1], problem), g(Node[1]))

    Open = util.PriorityQueueWithFunction(EvalFunc)

    StartNode = ([problem.getStartState()], [])
    Open.push(StartNode)
    # Same as depthFirstSearch

    Seen = {StartNode[0][0]: EvalFunc(StartNode)}

    while not Open.isEmpty():
        ThisNode = Open.pop()

        StatesInThisNode = ThisNode[0]
        ActionsSoFar = ThisNode[1]
        ThisState = StatesInThisNode[-1]

        if EvalFunc(ThisNode) <= Seen[ThisState]:
            if problem.isGoalState(ThisState):
                return ActionsSoFar
            for Succ in problem.getSuccessors(ThisState):
                NewNode = (StatesInThisNode + [Succ[0]], ActionsSoFar + [Succ[1]])
                if Succ[0] not in Seen or EvalFunc(NewNode) < Seen[Succ[0]]:
                    Open.push(NewNode)
                    Seen[Succ[0]] = EvalFunc(NewNode)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
