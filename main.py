"""
Author: Fawaz Ahmed & Kevin
NetId: fxa180017
Date: 3/16/2022
Version: 1.0
Notes: Main program for HW2P2
"""
import sys


def main():
    variables = {}
    constraints = []
    forwardChecking = False

    with open(sys.argv[1], 'r') as file:
        for variable in file:
            variable = variable.strip().split(': ')
            variables[variable[0]] = variable[1].split(' ')

    with open(sys.argv[2], 'r') as file:
        for constraint in file:
            constraint = constraint.strip().split(' ')
            constraints.append(constraint)

    if sys.argv[3] != 'none':
        forwardChecking = True

    print('test')


if __name__ == '__main__':
    main()
