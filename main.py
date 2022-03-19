"""
Author: Fawaz Ahmed & Kevin Vigil
NetId: fxa180017 & kav170000
Date: 3/16/2022
Version: 1.0
Notes: Main program for HW2P2
"""
import sys
import itertools
from copy import deepcopy


def operator(constraint):
    options = {'>': constraint[0] > constraint[2],
               '<': constraint[0] < constraint[2],
               '=': constraint[0] == constraint[2],
               '!': constraint[0] != constraint[2]
               }
    return options[constraint[1]]


class Assignment:
    def __init__(self, vars, constraints_list, fc):
        self.nodes = {Node(v, constraints_list) for v in vars.items()}
        self.constraints = constraints_list
        self.nodeSize = len(self.nodes)
        self.forwardChecking = fc
        self.complete = False

    def select_unassigned_var(self, assignments):
        """
        The idea for heuristic selection will go through this process
        Priority 1: Most Constrained Variable: Will select the variable with the current smallest domain size that has
                    not already been assigned/selected
        Priority 2: Most Constraining Variable: Will select the variable with the largest constraint count that has not
                    already been assigned/selected
        Priority 3: Alphabetical: Will select the variable alphabetically that has not already been assigned/selected
        """
        selected = None
        for n in self.nodes:
            if n.key not in assignments:
                # Choose from nodes that are not currently selected.

                if selected is None:
                    # Initialize selected
                    selected = n

                elif len(n.domain) < len(selected.domain):
                    # If current node has smaller domain than selected node, change selected to current.
                    selected = n

                elif len(n.domain) == len(selected.domain):
                    # If current node and selected are equal (i.e. Priority 1) move to Priority 2.
                    # For loop to count constraints that are not part of assigned
                    operators = ['>', '<', '=', '!']
                    nCon = 0
                    sCon = 0
                    for con in n.constraints:
                        for x in con:
                            if x == n.key or x in operators:
                                continue
                            else:
                                if x not in assignments:
                                    nCon += 1
                    for con in selected.constraints:
                        for x in con:
                            if x == selected.key or x in operators:
                                continue
                            else:
                                if x not in assignments:
                                    sCon += 1

                    if nCon > sCon:
                        # If current node has a greater constraining count then change selected to current.
                        selected = n
                    elif nCon == sCon:
                        # If Priority 2 is equal, move forward to Priority 3.
                        if n.key < selected.key:
                            # Select alphabetically
                            selected = n
        return selected

    def orderValues(self, n1, dic):
        constraining_values = {}
        for v1 in n1.domain:
            num_legal_moves = 0
            for constraint in n1.constraints:
                # Left
                if n1.key == constraint[0]:
                    for n2 in self.nodes:
                        if n2.key == constraint[2] and n2.key not in dic:
                            for v2 in n2.domain:
                                if operator([v1, constraint[1], v2]):
                                    num_legal_moves += 1
                # Right
                elif n1.key == constraint[2]:
                    for n2 in self.nodes:
                        if n2.key == constraint[0] and n2.key not in dic:
                            for v2 in n2.domain:
                                if operator([v2, constraint[1], v1]):
                                    num_legal_moves += 1
            if num_legal_moves in constraining_values:
                constraining_values[num_legal_moves].append(v1)
            else:
                constraining_values[num_legal_moves] = [v1]

        ordered_domain_values = []
        for key in sorted(constraining_values.keys(), reverse=True):
            ordered_domain_values.append(constraining_values[key])
        return list(itertools.chain(*ordered_domain_values))

    def constraint_check(self, node, value, dict):
        for c in self.constraints:
            pos = -1
            if node.key in c:
                pos = c.index(node.key)
            if pos == 0 and c[2] in dict:
                if c[1] == '>' and not value > dict[c[2]]:
                    return False
                elif c[1] == '<' and not value < dict[c[2]]:
                    return False
                elif c[1] == '=' and not value == dict[c[2]]:
                    return False
                elif c[1] == '!' and not value != dict[c[2]]:
                    return False
            elif pos == 2 and c[0] in dict:
                if c[1] == '>' and not dict[c[0]] > value:
                    return False
                elif c[1] == '<' and not dict[c[0]] < value:
                    return False
                elif c[1] == '=' and not dict[c[0]] == value:
                    return False
                elif c[1] == '!' and not dict[c[0]] != value:
                    return False
        return True

    def __str__(self):
        ret_str = ""
        ret_str += "Nodes: \n"
        for v in self.nodes:
            ret_str += v.__str__()
        return ret_str


class Node:
    def __init__(self, var, con_list):
        self.key = var[0]
        self.domain = var[1]
        self.con_count = 0
        self.constraints = []

        # Determines which constraints belong to the variable. Used for heuristics and variable selection
        for con in con_list:
            if self.key in con:
                self.constraints.append(con)
                self.con_count += 1

    def __str__(self):
        ret_str = "Key: " + str(self.key) + "\nDomain: " + str(self.domain) + "\nConstraint Count: " + str(
            self.con_count) + "\n"
        return ret_str


def solve(problem):
    return recurs({}, problem)


def recurs(dic, problem):
    curNode = problem.select_unassigned_var(dic)
    if curNode is None:
        return dic
    for v in problem.orderValues(curNode, dic):
        if problem.constraint_check(curNode, v, dic):
            dic[curNode.key] = v
            if problem.forwardChecking:
                '''call run_forward_checking pass it through'''

            result = recurs(dic, problem)
            if result:
                return result
            dic.pop(curNode.key)
        else:
            dic[curNode.key] = v
            print(dic, " Failure")
            dic.pop(curNode.key)
    return False


def run_forward_checking(dict, problem, curNode):
    """will limit the domain of the current branch nodes
    issues: upon failure, domains are still limited by previous branches
    need to be able to backtrack and restore domains"""
    return None


def main():
    variables = {}  # dictionary
    constraints = []  # list
    forward_checking = False

    with open(sys.argv[2], 'r') as file:
        for constraint in file:
            constraint = constraint.strip().split(' ')
            constraints.append(constraint)

    print("\n")

    with open(sys.argv[1], 'r') as file:
        for variable in file:
            variable = variable.strip().split(': ')
            variables[variable[0]] = variable[1].split(' ')

    if sys.argv[3] != 'none':
        forward_checking = True

    problem = Assignment(variables, constraints, forward_checking)
    print(solve(problem), " Solution")


if __name__ == '__main__':
    main()
