# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 18:24:58 2017

@author: Mounika PSL
"""
import sys
import Queue as Z
from multiprocessing import Queue
from copy import deepcopy
import time

lines = []


def calculatePossibleColors(currentState, maxColored, minColored):
    possibleColors = set(deepcopy(SetOfAvailableColors))
    # print "Inside PossibleColors-->"+str(possibleColors)
    # print "Max Colored States-->"+str(maxColored)
    # print "Min Colored States-->"+str(minColored)
    for value in dict_map[currentState]:
        # print "Value-->"+str(value)
        if value in maxColored.keys():
            # print "Inisde maxColored-->"+value+"-->color-->"+maxColored[value]
            colorOfNeighbor = maxColored[value]
            possibleColors = possibleColors.difference(colorOfNeighbor)
            # print "possibleColors after removal-->"+str(possibleColors)
        if value in minColored.keys():
            # print "Inisde minColored-->"+value+"-->color-->"+minColored[value]
            colorOfNeighbor = minColored[value]
            possibleColors = possibleColors.difference(colorOfNeighbor)
            # print "possibleColors after removal-->"+str(possibleColors)
    # print "Final PossibleColors-->"+str(possibleColors)
    return possibleColors


def calculateInitialNeighbors(maxColored, minColored):
    neighbors = set()
    # print "Main Map-->"+str(dict_map)
    # print "Max color keys-->"+str(maxColored.keys())
    # print "Min color keys-->"+str(minColored.keys())
    for key in maxColored.keys():
        # print "Inside MaxColored-->"+key
        # print "---"+str(dict_map[key])
        for val in dict_map[key]:
            # print "Inside for-->"+val
            if val not in maxColored.keys() and val not in minColored.keys():
                # print "Inside if-->"+val
                neighbors.add(val)
    # print "neighbors after MAX-->"+str(neighbors)
    for key in minColored.keys():
        # print "Inside MinColored-->"+key
        for val in dict_map[key]:
            # print "Inside for-->"+val
            if val not in maxColored.keys() and val not in minColored.keys():
                # print "Inside if-->"
                neighbors.add(val)
    # print "neighbors after MAX-->"+str(neighbors)
    return neighbors


def calNeighborsSet(adjacentNode, minColored, maxColored):
    copyOfMap = deepcopy(dict_map)
    # print "copyofmap-->"+str(copyOfMap)
    # print "adjacentNode-->"+str(adjacentNode)
    # copyOfMaxColored=deepcopy(maxColored)
    # copyOfMinColored=deepcopy(minColored)
    copyOfAdjacentNodes = deepcopy(adjacentNode)
    nextPossibleChoices = set()
    # for adjNodeInst in copyOfAdjacentNodes:
    for value in copyOfMap[adjacentNode]:
        if value not in minColored and value not in maxColored:
            nextPossibleChoices.add(value)
    # print "Next PossibleNeighbors-->"+str(nextPossibleChoices)
    return nextPossibleChoices


def EvalutionFunction(maxColored, minColored):
    # print "Inside Eval Function"
    TotalMax = dict()
    TotalMin = dict()
    # print "maxColored-->"+str(maxColored)
    # print "minColored-->"+str(minColored)
    for key, value in player1_CW.items():
        TotalMax.update({key: 0})
    # print "TotalMax initialized-->"+str(TotalMax)
    for key, value in player2_CW.items():
        TotalMin.update({key: 0})
    # print "TotalMin initialized-->"+str(TotalMin)
    for key, values in maxColored.items():
        if values in TotalMax.keys():
            # print "TotalMax[value] before addition-->"+str(TotalMax[values])+"key->"+key+"values-->"+values
            TotalMax[values] = TotalMax[values] + int(player1_CW[values])
            # print "TotalMax[value] After addition-->"+str(TotalMax[values])
    # print "TotalMax after loop-->"+str(TotalMax)
    for key, values in minColored.items():
        if values in TotalMin.keys():
            # print "TotalMin[value] before addition-->"+str(TotalMin[values])+"key->"+key+"values-->"+values
            TotalMin[values] = TotalMin[values] + int(player2_CW[values])
            # print "TotalMin[value] After addition-->"+str(TotalMin[values])
    # print "TotalMin after loop-->"+str(TotalMin)
    MaxValue = 0
    MinValue = 0
    for key, value in TotalMax.items():
        MaxValue = MaxValue + TotalMax[key]
    # print "MaxValue-->"+str(MaxValue)
    for key, value in TotalMin.items():
        MinValue = MinValue + TotalMin[key]
    # print "MinValue-->"+str(MinValue)
    finalValue = MaxValue - MinValue
    # print "Final Value-->"+str(finalValue)
    return finalValue


def checkTerminal(maxColoredStates, minColoredStates, neighbors):
    # print "Inside checkTerminal"
    maxSet = set(maxColoredStates.keys())
    # print "maxSet-->"+str(maxSet)
    minSet = set(minColoredStates.keys())
    # print "minSet-->"+str(minSet)
    totalSet = minSet.union(maxSet)
    # print "totalSet-->"+str(totalSet)
    diffSet = totalSet.symmetric_difference(neighbors)
    # print "diffSet-->"+str(diffSet)
    # diffSet.
    if (len(diffSet) == 0):
        return True
    else:
        return False
        # currentNode + "," + color + "," + str(depth - 1) + "," + str(best[0]) + "," + str(best[1]) + "," + str(best[2])


def fileWrite(Node, Color, Depth, Value, Alpha, Beta):
    fo.write(Node + ", " + Color + ", " + Depth + ", " + Value + ", " + Alpha + ", " + Beta)
    fo.write("\n")
    return


def fileWriteFinal(Node, color, value):
    fo.write(Node + ", " + color + ", " + value)
    fo.write("\n")
    return


def calculateMinMax(currentNode, color, isMax, previousNeighbors, depth, maxColored, minColored, alpha, beta, path):
    # print "Node being evaluated-->"+str(currentNode)+"with color-->"+str(color)+"==>"+str(isMax)
    # print "Max Colored Nodes-->"+str(maxColored)
    # print "Min Colored Node-->"+str(minColored)
    # print "global depth-->"+str(global_depth)
    best = [None] * 4
    best_InTerminal = [0] * 4

    if (depth == int(global_depth) + 1):
        # print "Inside EVAL Depth-->Depth Reached"
        finalValue = EvalutionFunction(maxColored, minColored)
        # print "Inside EVAL Depth final value-->"+str(finalValue)
        best_InTerminal[0] = finalValue
        best_InTerminal[1] = alpha
        best_InTerminal[2] = beta
        best_InTerminal[3] = path + "-" + currentNode + "," + color
        # print "best_InTerminal"+str(best_InTerminal[0])+"-->"+str(best_InTerminal[1])+"-->"+str(best_InTerminal[2])+"-->"+str(best_InTerminal[3])
        return best_InTerminal
    elif checkTerminal(minColored, maxColored, previousNeighbors):
        # print "Inside EVAL-->isTerminal"
        finalValue = EvalutionFunction(maxColored, minColored)
        best_InTerminal[0] = finalValue
        best_InTerminal[1] = alpha
        best_InTerminal[2] = beta
        best_InTerminal[3] = path + "-" + currentNode + "," + color
        # print "best_InTerminal" + str(best_InTerminal[0]) + "-->" + str(best_InTerminal[1]) + "-->" + str(
        # best_InTerminal[2]) + "-->" + str(best_InTerminal[3])
        return best_InTerminal

    if (isMax == True):
        # print "Inside MAX-->"
        best[0] = float("-inf")
        best[1] = alpha
        best[2] = beta
        best[3] = path
        # best = float('-inf')
        isTerminal = True
        # current node is the one whose neighbors will be evaluated
        # copyOfCurrentNode=currentNode
        copyOfMap = deepcopy(dict_map)

        neighbors = deepcopy(previousNeighbors)

        # print "Neighbors-->"+str(neighbors)
        # copyOfNeighbors=deepcopy(neighbors)
        for adjNode in sorted(neighbors):
            # print "adjNode-->"+str(adjNode)+"neighbors-->"+str(neighbors)
            possibleColors = calculatePossibleColors(adjNode, maxColored, minColored)
            possibleColors = sorted(possibleColors)
            # print "valid colors for adjacent node-->"+adjNode+"are-->"+str(possibleColors)
            # copyOfNeighbors=deepcopy(neighbors)
            for c in sorted(possibleColors):
                isTerminal = False
                copyOfNeighbors = deepcopy(neighbors)
                # copyofNeighborsMap=deepcopy(neighbors)
                # dict_temp=dict()
                # dict_temp={adjNode : c}
                copyOfMaxColored = deepcopy(maxColored)
                copyOfMaxColored.update({adjNode: c})

                if adjNode in copyOfNeighbors:
                    # print "Node being deleted-->"+str(adjNode)
                    copyOfNeighbors.remove(adjNode)
                    # print "copyOfNeighbors after deletion-->"+str(copyOfNeighbors)
                    # fetching all the neighbors of the adjNode selected from the list of neighbors from the mainmap
                    for i in range(0, len(copyOfMap[adjNode])):
                        nextNode = copyOfMap[adjNode][i]
                        # print "nextNode-->"+str(nextNode)
                        if nextNode not in copyOfMaxColored.keys() and nextNode not in minColored.keys():
                            # print "Neighboring node being added-->"+str(nextNode)
                            copyOfNeighbors.add(nextNode)
                # neighbors=copyOfNeighbors
                # print "**************************new adjacent nodes map-->"+str(neighbors)
                # print "copyOfNeighbors-->"+str(copyOfNeighbors)
                # print "**********************************************************************************"
                # print "currentNode-->"+currentNode+"color-->"+c+"depth-->"+str(depth-1)+str(best[0])

                # print currentNode+", "+color+", "+str(depth-1)+", "+str(best[0])+", "+str(best[1])+", "+str(best[2])
                fileWrite(currentNode, color, str(depth - 1), str(best[0]), str(best[1]), str(best[2]))
                # fo.write(currentNode+","+color+","+str(depth-1)+","+str(best[0])+","+str(best[1])+","+str(best[2]))
                # fo.write("\n")
                # print "Function call-->"+str(adjNode)+"-->"+str(copyOfNeighbors)
                result = calculateMinMax(adjNode, c, False, copyOfNeighbors, depth + 1, copyOfMaxColored, minColored, alpha, beta,
                             path + "-" + adjNode + "," + c)
                # print "##################################################################################"
                fileWrite(adjNode, c, str(depth), str(result[0]), str(result[1]), str(result[2]))
                # print adjNode+", "+c+", "+str(depth)+", "+str(val[0])+", "+str(val[1])+", "+str(val[2])
                # fo.write(adjNode+","+c+","+str(depth)+","+str(val[0])+","+str(val[1])+","+str(val[2]))
                # fo.write("\n")
                # best=max(best,val)
                if (best[0] < result[0]):
                    best[3] = result[3]
                best[0] = max(best[0], result[0])
                alpha = max(best[0], alpha)
                if (beta <= alpha):
                    return best
                else:
                    best[1] = alpha
            neighbors.add(adjNode)
            maxColored.pop(adjNode, None)
            if maxColored.has_key(adjNode):
                # maxColored.__delitem__(adjNode)
                del maxColored[adjNode]
        if (isTerminal):
            finalValue = EvalutionFunction(maxColored, minColored)
            best_InTerminal[0] = finalValue
            best_InTerminal[1] = alpha
            best_InTerminal[2] = beta
            best_InTerminal[3] = path
            return best_InTerminal
        return best




    else:
        # print "Inside MIN-->"
        best[0] = float("inf")
        best[1] = alpha
        best[2] = beta
        best[3] = path
        # best = float('-inf')
        isTerminal = True
        # current node is the one whose neighbors will be evaluated
        # copyOfCurrentNode=currentNode
        copyOfMap = deepcopy(dict_map)
        # copyOfPreviousNeighbors=deepcopy(previousNeighbors)
        # neighbors set has all the neighbors of the "currentState"passed and which are not colored





        neighbors = deepcopy(previousNeighbors)
        # neighbors=set(calNeighborsSet(currentNode,maxColored,minColored))
        # neighbors=neighbors.union(set(previousNeighbors))
        # print "Neighbors-->"+str(neighbors)

        # print "Neighbors-->"+str(neighbors)
        # copyOfNeighbors=deepcopy(neighbors)
        for adjNode in sorted(neighbors):
            # print "adjNode-->"+str(adjNode)
            possibleColors = calculatePossibleColors(adjNode, maxColored, minColored)
            possibleColors = sorted(possibleColors)
            # print "valid colors for adjacent node-->"+adjNode+"are-->"+str(possibleColors)

            for c in sorted(possibleColors):
                isTerminal = False
                copyOfNeighbors = deepcopy(neighbors)
                # copyofNeighborsMap=deepcopy(neighbors)
                # dict_temp=dict()
                # dict_temp={adjNode : c}
                copyOfMinColored = deepcopy(minColored)
                copyOfMinColored.update({adjNode: c})
                if adjNode in copyOfNeighbors:
                    # print "Node being deleted-->"+str(adjNode)
                    copyOfNeighbors.remove(adjNode)
                    # print "copyOfNeighbors after deletion-->"+str(copyOfNeighbors)
                    # fetching all the neighbors of the adjNode selected from the list of neighbors from the mainmap
                    for i in range(0, len(copyOfMap[adjNode])):
                        nextNode = copyOfMap[adjNode][i]
                        # print "nextNode-->"+str(nextNode)
                        if nextNode not in maxColored.keys() and nextNode not in copyOfMinColored.keys():
                            # print "Neighboring node being added-->"+str(nextNode)
                            copyOfNeighbors.add(nextNode)
                # neighbors=copyOfNeighbors
                # print "**************************new adjacent nodes map-->"+str(copyOfNeighbors)
                # print "**********************************************************************************"
                # print "currentNode-->"+currentNode+"color-->"+c+"depth-->"+str(depth-1)+str(best[0])
                # print currentNode+", "+color+", "+str(depth-1)+", "+str(best[0])+", "+str(best[1])+", "+str(best[2])
                fileWrite(currentNode, color, str(depth - 1), str(best[0]), str(best[1]), str(best[2]))
                # fo.write(currentNode+", "+color+", "+str(depth-1)+", "+str(best[0])+", "+str(best[1])+", "+str(best[2]))
                # fo.write("\n")
                # print "Function call-->"+str(adjNode)+"-->"+str(copyOfNeighbors)
                result = calculateMinMax(adjNode, c, True, copyOfNeighbors, depth + 1, maxColored, copyOfMinColored, alpha, beta,
                             path + "-" + adjNode + "," + c)
                # print "##################################################################################"
                # print adjNode+","+c+","+str(depth)+","+str(val[0])+","+str(val[1])+","+str(val[2])
                fileWrite(adjNode, c, str(depth), str(result[0]), str(result[1]), str(result[2]))
                # fo.write(adjNode+","+c+","+str(depth)+","+str(val[0])+","+str(val[1])+","+str(val[2]))
                # fo.write("\n")
                # best=max(best,val)
                if (best[0] > result[0]):
                    best[3] = result[3]
                best[0] = min(best[0], result[0])
                beta = min(best[0], beta)
                if (beta <= alpha):
                    return best
                else:
                    best[2] = beta
            neighbors.add(adjNode)
            minColored.pop(adjNode, None)
            if minColored.has_key(adjNode):
                # maxColored.__delitem__(adjNode)
                del minColored[adjNode]
        if (isTerminal):
            finalValue = EvalutionFunction(maxColored, minColored)
            best_InTerminal[0] = finalValue
            best_InTerminal[1] = alpha
            best_InTerminal[2] = beta
            best_InTerminal[3] = path
            return best_InTerminal
        return best


start = time.time()
# with open(r'C:\Users\Mounika PSL\Desktop\AI\Assignment 2\testcases\t5.txt') as f:
# lines=f.readlines()
with open(sys.argv[2]) as f:
    lines.extend(f.read().splitlines())

global AllColorsAllStates
global coloredStates
global dict_map
global set_colors
global global_depth
global MIN
global fo
global MAX
MIN = float("-inf")
MAX = float("inf")
AllColorsAllStates = dict()
InitialNeighboringStates = []
dict_statesDomain = dict()
InitialColoredStates = dict()
i = 0;
dict_map = dict()
temp1 = dict()
set_colors = []
global player1_CW
global player2_CW
player1_CW = dict()
player2_CW = dict()
Initial_Player1_Colored = dict()
Initial_Player2_Colored = dict()
MinColoredStates = dict()
MaxColoredStates = dict()
depth = 0
global SetOfAvailableColors
SetOfAvailableColors = set()
player2_state = ''
player2_color = ''
startNode = ''
startColor = ''
fo = open("output.txt", "w")
for line in lines:
    if i == 0:
        # Reading input colors
        colors = line.split(',')
        for c in colors:
            c = c.strip()
            # print c
            set_colors.append(c)
        SetOfAvailableColors = set(set_colors)
        SetOfAvailableColors = sorted(SetOfAvailableColors)
        i = i + 1
    # CHECK FOR MORE NUMBER OF INITIAL ASSIGNMENTS
    elif i == 1:
        # Reading initial moves
        stmt = line.split(',')
        # print "+++++"+str(stmt)

        for n in stmt:
            s = n.split('-')
            # print "++++++"+str(s)
            s[1] = s[1].strip()
            # print y
            if s[1] == '1':
                # print "Inside if"
                y = s[0]
                x = y.split(':')
                Initial_Player1_Colored[x[0].strip()] = x[1].strip()
                InitialColoredStates[x[0].strip()] = x[1].strip()
                MaxColoredStates.update({x[0].strip(): x[1].strip()})
                # print "Player 1 Initially Colored"+str(Initial_Player1_Colored)
            if s[1] == '2':
                y = s[0]
                x = y.split(':')
                Initial_Player2_Colored[x[0].strip()] = x[1].strip()
                InitialColoredStates[x[0].strip()] = x[1].strip()
                player2_state = x[0].strip()
                player2_color = x[1].strip()
                startNode = x[0].strip()
                startColor = x[1].strip()
                MinColoredStates.update({x[0].strip(): x[1].strip()})
                # print "Player 2 Initially Colored"+str(Initial_Player2_Colored)

        i = i + 1
    elif i == 2:
        # reading depth
        depth = line.strip()
        global_depth = depth
        i = i + 1

    elif i == 3:
        # Reading color weight assignments of each player
        colors = line.split(',')
        for c in colors:
            # print c
            c = c.split(':')
            # print c
            # print c[0]
            # print c[1]
            player1_CW.update({c[0].strip(): c[1].strip()})
            # print "Player 1 color weightage"+str(player1_CW)
        i = i + 1
    elif i == 4:
        # print "+++++"+line
        colors = line.split(',')
        for c in colors:
            # print c
            c = c.split(':')
            # print c
            # print c[0]
            # print c[1]
            player2_CW.update({c[0].strip(): c[1].strip()})
            # print "Player 1 color weightage"+str(player1_CW)
        i = i + 1
        # print "Player 2 color weightage"+str(player2_CW)

    else:
        # Building map
        states = line.split(':')
        # print states[0]
        # print states[1]

        if states[0].strip() not in dict_map.keys():
            dict_map[states[0].strip()] = []
            AllColorsAllStates[states[0].strip()] = SetOfAvailableColors

        for n in states[1].split(','):
            dict_map[states[0].strip()].append(n.strip())
        i = i + 1

# AllColors=set(set_colors)

# finalDepth=0
# allColoredStates=dict()
# lstAllColoredStates=[]

neighbors = dict()

# Player2_colored_initially=deepcopy(Initial_Player2_Colored)

# neighbors1=dict()


neighbors = calculateInitialNeighbors(MaxColoredStates, MinColoredStates)
# print "after calculateInitialNeighbors-->"+str(neighbors)

val = calculateMinMax(startNode, startColor, True, neighbors, 1, MaxColoredStates, MinColoredStates, MIN, MAX, startNode)
# print startNode+", "+startColor+", 0, "+str(val[0])+", "+str(val[1])+", "+str(val[2])
fileWrite(startNode, startColor, str(0), str(val[0]), str(val[1]), str(val[2]))
# fo.write(startNode+", "+startColor+", 0, "+str(val[0])+", "+str(val[1])+", "+str(val[2]))
# fo.write("\n")
# print val
# print val[0]
path = val[3]
# print "Final Path-->"+path
if len(path) != 0:
    sentence = path.split('-')
    node = sentence[1].split(",")
    # print node[0]
    # print "node"
    color = node[1].split("-")
    finalColor = color[0]
    # print color[0]
    # print "Inside IF-->"
    # print node[0] + ", " + color[0] + ", " + str(val[0])
    fileWriteFinal(str(node[0]), str(color[0]), str(val[0]))
    # fo.write(node + ", " + color[0] + ", " + str(val[0]))

fo.close()
