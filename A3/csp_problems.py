from csp import Variable, CSP
from constraints import *
from backtracking import bt_search


##################################################################
#  NQUEENS
##################################################################

def nQueens(n, tableCnstr):
    """Return an n-queens CSP, optionally use tableConstraints"""
    dom = []
    for i in range(n):
        dom.append(i + 1)

    vars = []
    for i in dom:
        vars.append(Variable('Q{}'.format(i), dom))

    cons = []
    for qi in range(len(dom)):
        for qj in range(qi + 1, len(dom)):
            if tableCnstr:
                con = QueensTableConstraint("C(Q{},Q{})".format(qi + 1, qj + 1),
                                            vars[qi], vars[qj], qi + 1, qj + 1)
            else:
                con = QueensConstraint("C(Q{},Q{})".format(qi + 1, qj + 1),
                                       vars[qi], vars[qj], qi + 1, qj + 1)
            cons.append(con)

    csp = CSP("{}-Queens".format(n), vars, cons)
    return csp


def solve_nQueens(n, algo, allsolns, tableCnstr=False, variableHeuristic='fixed', trace=False):
    """Create and solve an nQueens CSP problem. The first
       parameter is 'n' the number of queens in the problem,
       The second specifies the search algorithm to use (one
       of 'BT', 'FC', or 'GAC'), the third specifies if
       all solutions are to be found or just one, variableHeuristic
       specifies how the next variable is to be selected
       'random' at random, 'fixed' in a fixed order, 'mrv'
       minimum remaining values. Finally 'trace' if specified to be
       'True' will generate some output as the search progresses.
    """
    csp = nQueens(n, tableCnstr)
    solutions, num_nodes = bt_search(algo, csp, variableHeuristic, allsolns, trace)
    print "Explored {} nodes".format(num_nodes)
    if len(solutions) == 0:
        print "No solutions to {} found".format(csp.name())
    else:
        print "Solutions to {}:".format(csp.name())
        i = 0
        for s in solutions:
            i += 1
            print "Solution #{}: ".format(i),
            for (var, val) in s:
                print "{} = {}, ".format(var.name(), val),
            print ""


##################################################################
# SUDOKU
##################################################################

def sudokuCSP(initial_sudoku_board, model='neq'):
    """The input board is specified as a list of 9 lists. Each of the
       9 lists represents a row of the board. If a 0 is in the list it
       represents an empty cell. Otherwise if a number between 1--9 is
       in the list then this represents a pre-set board
       position. E.g., the board

       -------------------
       | | |2| |9| | |6| |
       | |4| | | |1| | |8|
       | |7| |4|2| | | |3|
       |5| | | | | |3| | |
       | | |1| |6| |5| | |
       | | |3| | | | | |6|
       |1| | | |5|7| |4| |
       |6| | |9| | | |2| |
       | |2| | |8| |1| | |
       -------------------
       would be represented by the list of lists

       [[0,0,2,0,9,0,0,6,0],
       [0,4,0,0,0,1,0,0,8],
       [0,7,0,4,2,0,0,0,3],
       [5,0,0,0,0,0,3,0,0],
       [0,0,1,0,6,0,5,0,0],
       [0,0,3,0,0,0,0,0,6],
       [1,0,0,0,5,7,0,4,0],
       [6,0,0,9,0,0,0,2,0],
       [0,2,0,0,8,0,1,0,0]]


       Construct and return CSP for solving this sudoku board using
       binary not equals if model='neq' or using allDiff constraints
       if model='alldiff'

       The CSP contains a variable for each cell of the board with
       with domain equal to {1-9} if the board has a 0 at that position,
       and domain equal {i} if the board has a fixed number i at that
       cell.

       The CSP has a neq constraint between every relevant pair of
       variables, or an alldiff constraint between every set of
       variables in a row, column, or sub-square
    """
    # your implementation for Question 4 changes this function
    # implement handling of model == 'alldiff'

    if model not in ['neq', 'alldiff']:
        print "Error wrong sudoku model specified {}. Must be one of {}".format(
            model, ['neq', 'alldiff'])

    # first define the variables
    i = 0
    var_array = []
    for row_list in initial_sudoku_board:
        var_array.append([])
        j = 0
        for _ in row_list:
            cell = initial_sudoku_board[i][j]
            if cell == 0:
                dom = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                dom = [cell]
            var = Variable("V{},{}".format(i + 1, j + 1), dom)
            var_array[i].append(var)
            j += 1
        i += 1

    # Set up the constraints
    # row constraints
    constraint_list = []

    for row in var_array:
        if model == 'neq':
            constraint_list.extend(post_all_pairs(row))
        elif model == 'alldiff':
            constraint_list.append(AllDiffConstraint("row num {} constraint".format(row), row))

    for colj in range(len(var_array[0])):
        scope = map(lambda row: row[colj], var_array)
        if model == 'neq':
            constraint_list.extend(post_all_pairs(scope))
        elif model == 'alldiff':
            constraint_list.append(AllDiffConstraint("column num {} constraint".format(colj), scope))

    for i in [0, 3, 6]:
        for j in [0, 3, 6]:
            # initial upper left hand index of sub-square
            scope = []
            for k in [0, 1, 2]:
                for l in [0, 1, 2]:
                    scope.append(var_array[i + k][j + l])
            if model == 'neq':
                constraint_list.extend(post_all_pairs(scope))
            elif model == 'alldiff':
                constraint_list.append(AllDiffConstraint("sub-square num {} constraint".format(scope), scope))

    vars = [var for row in var_array for var in row]
    return CSP("Sudoku", vars, constraint_list)


def post_all_pairs(var_list):
    """create a not equal constraint between all pairs of variables in var_list
       return list of constructed constraint objects
    """
    constraints = []
    for i in range(len(var_list)):
        for j in range(i + 1, len(var_list)):
            c = NeqConstraint("({},{})".format(var_list[i].name(), var_list[j].name()), [var_list[i], var_list[j]])
            constraints.append(c)
    return constraints


def solve_sudoku(initialBoard, model, algo, allsolns,
                 variableHeuristic='fixed', trace=False):
    if model not in ['neq', 'alldiff']:
        print "Error wrong sudoku model specified {}. Must be one of {}".format(
            model, ['neq', 'alldiff'])
    csp = sudokuCSP(initialBoard, model)

    solutions, num_nodes = bt_search(algo, csp, variableHeuristic, allsolns, trace)
    print "Explored {} nodes".format(num_nodes)
    if len(solutions) == 0:
        print "No solutions to {} found".format(csp.name())
    else:
        i = 0
        for s in solutions:
            i += 1
            print "Solution #{}: ".format(i)
            sudoku_print_soln(s)


def sudoku_print_soln(s):
    """s is a list of (var,value) pairs. Organize them into
       the right order and then print it in a board layout
    """
    s.sort(key=lambda varval_pair: varval_pair[0].name())
    print "-" * 37
    for i in range(0, 9):
        print "|",
        for j in range(0, 9):
            indx = i * 9 + j
            print s[indx][1], "|",
        print ""
        print "-" * 37


##################################################################
# Plane Sequencing
##################################################################

class PlaneProblem:
    """Class to hold an instance of the plane scheduling problem.
       defined by the following data items
       a) A list of planes

       b) A list of needed flights

       c) Legal flights for each plane. Specified as a list of lists
          For each list L. L[0] = a particular plane P. and L[1], L[2} ...
          are all of the flights that P is equipped to fly.
          This must be a subset of the list of flights

       d) Possible starting flights for each plane. Specified as a
          list of lists For each list L. L[0] = a particular plane P,
          and L[1], L[2], ...  are all of the flights that in the same
          place the plane that P is initially located. This must be a
          subset of the list of flights. Note however, that that P
          might not be able to fly all of these flights (so the list
          (c) needs to be checked as well)


       e) A list of pairs of flights (f1,f2) such that f2 can legally
          follow f1 in a plane's schedule. (That is, f2 starts at the
          same location that f1 end).

       f) A list of flights that end in a location where maintenance
          can be performed

       g) In integer specifying the minimum frequency of plane
          maintenance. That is, if the minimum frequency is 4, then at
          least one out of every sequence of 4 flights a plane makes
          must be a flight ending at a location where maintenance can
          be performed.

        See plane_scheduling.py for examples of the use of this class.
        Note also the access functions can_fly and can_start
    """

    def __init__(self, planes, flights, can_fly, flights_at_start,
                 can_follow, maintenance_flights, min_maintenance_frequency):
        self.planes = planes
        self.flights = flights
        self._can_fly = dict()
        self._flights_at_start = dict()
        self.can_follow = can_follow
        self.maintenance_flights = maintenance_flights
        self.min_maintenance_frequency = min_maintenance_frequency

        # do some data checks
        for l in can_fly:
            for f in l[1:]:
                if f not in flights:
                    print "PlaneProblem Error, can_fly contains a non-flight", f
        for l in flights_at_start:
            for f in l[1:]:
                if f not in flights:
                    print "PplaneProblem Error, flights_at_start contains a non-flight", f
        for (f1, f2) in can_follow:
            if f1 not in flights or f2 not in flights:
                print "PlaneProblem Error, can_follow contains pair with non-flight (", f1, ",", f2, ")"

        for f in maintenance_flights:
            if f not in flights:
                print "PlaneProblem Error, maintenance_flights contains a non-flight", f

        if min_maintenance_frequency == 0:
            print "PlaneProblem Error, min_maintenance_frequency must be greater than 0"

        # now convert can_fly and flights_at_start to a dictionary that
        # can be indexed by the plane.
        for l in can_fly:
            self._can_fly[l[0]] = l[1:]
        for l in flights_at_start:
            self._flights_at_start[l[0]] = l[1:]

        # some useful access functions

    def can_fly(self, plane):
        """Return list of flights plane can fly"""
        return self._can_fly[plane]

    def can_start(self, plane):
        """Return list of flights plane can start with"""
        return list(
            set(self._can_fly[plane]).intersection(
                self._flights_at_start[plane]))


def solve_planes(planes_problem, algo, allsolns,
                 variableHeuristic='mrv', silent=False, trace=False):
    # Your implementation for Question 6 goes here.
    #
    # Do not change the functions signature
    # (the autograder will twig out if you do).

    # If the silent parameter is set to True
    # you must ensure that you do not execute any print statements
    # in this function.
    # (else the output of the autograder will become confusing).
    # So if you have any debugging print statements make sure you
    # only execute them "if not silent". (The autograder will call
    # this function with silent=True, plane_scheduling.py will call
    # this function with silent=False)

    # You can optionally ignore the trace parameter
    # If you implemented tracing in your FC and GAC implementations
    # you can set this argument to True for debugging.
    #
    # Once you have implemented this function you should be able to
    # run plane_scheduling.py to solve the test problems (or the autograder).
    #
    #
    """This function takes a planes_problem (an instance of PlaneProblem
       class) as input. It constructs a CSP, solves the CSP with bt_search
       (using the options passed to it), and then from the set of CSP
       solutions it constructs a list of lists specifying a schedule
       for each plane and returns that list of lists
       The required format is the list of lists is:

       For each plane P the list of lists contains a list L.
       L[0] == P (i.e., the first item of the list is the plane)
       and L[1], ..., L[k] (i.e., L[1:]) is the sequence of flights
       assigned to P.

       The returned list of lists should contain a list for every
       plane.
    """
    # BUILD your CSP here and store it in the variable csp
    variables = []
    constraints = []

    all_planes = planes_problem.planes
    all_flights = planes_problem.flights

    NO_FLIGHT_VALUE = "__NO_FLIGHT__"

    # Helper functions, based on my choice of variables' names
    extract_plane = lambda var_name: var_name[var_name.find('~') + 1: var_name.rfind('~')]
    extract_slot = lambda var_name: int(var_name[var_name.rfind('~') + 1:])

    # Variables
    # One variable per plane and flight slot
    for plane in all_planes:
        dom = planes_problem.can_fly(plane)
        for i in range(len(dom)):
            if i == 0:  # if first plane, dom must be restricted to the ones that "can start"
                variables.append(Variable("Var~{}~{}".format(plane, i + 1),
                                          planes_problem.can_start(plane) + [NO_FLIGHT_VALUE]))
            else:
                variables.append(Variable("Var~{}~{}".format(plane, i + 1), dom + [NO_FLIGHT_VALUE]))

    # Sequence of flights must be feasible
    # Note: every flight can precede NO_FLIGHT_VALUE, including NO_FLIGHT_VALUE itself, but none can follow it
    idx = 0  # index of variables list
    while idx < len(variables) - 1:
        curr_plane = extract_plane(variables[idx].name())
        next_plane = extract_plane(variables[idx + 1].name())

        if curr_plane == next_plane:
            constr_name = "CanFollow~{}~{}".format(variables[idx].name(), variables[idx + 1].name())
            constr_scope = [variables[idx], variables[idx + 1]]
            acceptable_pairs = planes_problem.can_follow + [(fl, NO_FLIGHT_VALUE) for fl in variables[idx].domain()]

            constraints.append(TableConstraint(constr_name, constr_scope, acceptable_pairs))

        idx += 1

    # Mainteinance check
    min_freq = planes_problem.min_maintenance_frequency
    mant_flights = planes_problem.maintenance_flights + [NO_FLIGHT_VALUE]

    idx_first = 0  # index of first plane
    idx_last = 0  # index of last plane
    while idx_last < len(variables):
        curr_plane = extract_plane(variables[idx_first].name())
        next_plane = extract_plane(variables[idx_last].name())

        if curr_plane != next_plane:
            num_of_flights = idx_last - idx_first
            all_subsequences = [variables[idx_first:idx_last][i:i + min_freq]
                                for i in range(num_of_flights - min_freq + 1)]

            for subsequence in all_subsequences:
                constraints.append(NValuesConstraint("MainteinanceCheckForPlane~{}".format(curr_plane), subsequence,
                                                     mant_flights, 1, min_freq))

            idx_first = idx_last

        idx_last += 1

    if idx_first == 0:  # if there was only one plane
        for subsequence in [variables[i:i + min_freq] for i in range(idx_last - min_freq + 1)]:
            constraints.append(NValuesConstraint("MaintCheckForOnlyPlane", subsequence, mant_flights, 1, min_freq))

    # All flights must be scheduled exactly once
    for flight in all_flights:
        constraints.append(NValuesConstraint("Flight~{}~uniqueness".format(flight), variables, [flight], 1, 1))

    csp = CSP("Plane scheduling CSP", variables, constraints)

    # invoke search with the passed parameters
    solutions, num_nodes = bt_search(algo, csp, variableHeuristic, allsolns, trace)

    # Convert each solution into a list of lists specifying a schedule
    # for each plane in the format described above.
    to_return = []

    for solution in solutions:
        planes_to_routes = {plane: [None] * len(all_flights) for plane in all_planes}

        for var, val in solution:
            curr_plane = extract_plane(var.name())
            curr_slot = extract_slot(var.name()) - 1

            planes_to_routes[curr_plane][curr_slot] = val if val != NO_FLIGHT_VALUE else None

        converted_solutions = map(lambda plane: [plane] + planes_to_routes[plane], planes_to_routes.keys())

        # get rid of None's in a functional programming way
        to_return.append(map(lambda schedule: filter(lambda fl: fl is not None, schedule), converted_solutions))

    # then return a list containing all converted solutions
    # (i.e., a list of lists of lists)
    return to_return
