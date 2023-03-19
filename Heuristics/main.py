from DataReader import DataReader
from collections import defaultdict
import sys, os
import numpy as np
import timeit

def getFinalMatrix(assignments):
    finalMatrix = np.zeros((data.n,data.n))
    for assignment in assignments:
        for shapeNeighbour in getNodeNeighbours(assignments[assignment], data.m, data.hMatrix):
            connected = -1
            for neighbour in assignments:
                if assignments[neighbour] == shapeNeighbour:
                    connected = neighbour
            if connected != -1:
                finalMatrix[assignment,connected] = 1
            else:
                print("something went wrong when generating the final matrix")
    return finalMatrix

def getFinalObjectiveValue(assignments):
    imageLengthsSum = 0
    shapeLengthsSum = 0
    finalObjectiveValue = 0
    for assignment in assignments:
        for shapeNeighbour in getNodeNeighbours(assignments[assignment], data.m, data.hMatrix):
            connected = -1
            shapeLengthsSum = data.hMatrix[assignments[assignment],shapeNeighbour]
            for neighbour in assignments:
                if assignments[neighbour] == shapeNeighbour:
                    connected = neighbour
            if connected != -1:
                imageLengthsSum = data.gMatrix[assignment,connected]
            else:
                print("something went wrong when generating the final matrix")
            finalObjectiveValue = finalObjectiveValue + abs(imageLengthsSum-shapeLengthsSum)
    return finalObjectiveValue/2

def fileCheck(inst_path):
    if os.path.isfile(inst_path):
        print('Using instance ' + inst_path.split('/')[-1])
    else:
        print('File ' + inst_path + " not found. Aborting.")
        exit()

def getNodeNeighbours(node, size, matrix):
    neighbours = set()
    for x in range(size):
        if(matrix[node, x] != 0):
            neighbours.add(x)
    return neighbours

def areNeighbours(imageNode, assignedImageNode):
    if data.gMatrix[assignedImageNode,imageNode] != 0:
        return True
    return False

def checkFeasibility(imageN, shapeN, assignments):
    #satisfy connection with assignments if there are
    if len(assignments) != 0:
        shapeElemNeighbours = getNodeNeighbours(shapeN, data.m, data.hMatrix)
        assignmentsToSatisfy = set()
        for shape in shapeElemNeighbours:
            for assig in assignments:
                if assignments[assig] == shape:
                    assignmentsToSatisfy.add(assig)
        for assig in assignmentsToSatisfy:
            imageElemNeighbours = getNodeNeighbours(imageN, data.n, data.gMatrix)
            if assig not in imageElemNeighbours:
               return False
        return True
    else:
        return True


def recursivePaths(node, previousNode, a_list, size, matrix):
    nodeNeighbours = getNodeNeighbours(node, size, matrix)
    if ((len(nodeNeighbours) == 1 and previousNode in nodeNeighbours) or (node in a_list)):
        listCp = a_list.copy()
        listCp.append(node)
        return listCp
    else:
        listCopy = a_list.copy()
        listCopy.append(node)

        list_of_lists = []
        for neigh in nodeNeighbours:
            if neigh != previousNode:
                result = recursivePaths(neigh, node, listCopy, size, matrix)
                areLists = True
                for r in result:
                    if isinstance(r, type([])):
                        list_of_lists.append(r)
                    else:
                        areLists = False
                if not areLists:
                    list_of_lists.append(result)
        return list_of_lists

def getMximumCycleLength(cycles):
    maxLength = 0
    for l in cycles:
        if len(l) > maxLength:
            maxLength = len(l)
    return maxLength


def filterAndGetCycles(paths):
    result = []
    for p in paths:
        isCycle = (p.index(p[-1]) != len(p)-1)
        if isCycle:
            startingIndex = p.index(p[-1])
            localList = []
            for i in range(startingIndex, len(p)-1):
                localList.append(p[i])
            sortedList = set(localList)
            if sortedList not in result:
                result.append(sortedList)
    return result

def getCycles(node, size, matrix):
    paths = recursivePaths(node, -1, [], size, matrix)
    cycles = filterAndGetCycles(paths)

    maximumCycle = getMximumCycleLength(cycles)
    result = defaultdict(list)
    for c in cycles:
        result[len(c)].append(c)
    return result

def remove_empty_keys(dict):
    for elem in dict.copy().keys():
        if not dict[elem]:
            del dict[elem]

def checkCombination(combination, currentShapeCycle, elem):
    totalLengthsSum = 0
    shapeLengthsSum = 0
    imageLengthsSum = 0
    didComplete = True

    currentShapeCycleCopy = currentShapeCycle.copy()

    for c in range(combination):
        item = currentShapeCycleCopy.pop(0)
        currentShapeCycleCopy.append(item)

    for shapeNode in range(len(currentShapeCycle)):
        shapeNeighbours = getNodeNeighbours(currentShapeCycleCopy[shapeNode], data.m, data.hMatrix)
        imageNeighbours = getNodeNeighbours(elem[shapeNode], data.n, data.gMatrix)
        if len(shapeNeighbours) <= len(imageNeighbours):
            if shapeNode == len(currentShapeCycle) - 1:
                imageLengthsSum = data.gMatrix[elem[shapeNode], elem[0]]
                shapeLengthsSum = data.hMatrix[currentShapeCycleCopy[shapeNode], currentShapeCycleCopy[0]]
            else:
                imageLengthsSum = data.gMatrix[elem[shapeNode], elem[shapeNode + 1]]
                shapeLengthsSum = data.hMatrix[currentShapeCycleCopy[shapeNode], currentShapeCycleCopy[shapeNode+1]]
            totalLengthsSum = totalLengthsSum + abs(imageLengthsSum - shapeLengthsSum)
        else:
            didComplete = False
            break
    if didComplete:
        return [totalLengthsSum, currentShapeCycleCopy, elem]
    else:
        return [-1, -1, -1]

def getBestFeasableCycle(currentShapeCycle, imageCycles):
    bestCycleBasedOnWeight = []
    #check neighbourhoods that have been previously assigned
    currentShapeCycle = list(currentShapeCycle)
    for elem in imageCycles[len(currentShapeCycle)]:
        elem = list(elem)
        for combination in range(len(currentShapeCycle)):
            result = checkCombination(combination, currentShapeCycle, elem)
            if result[0] != -1:
                bestCycleBasedOnWeight.append(result)
    bestCycleBasedOnWeight = sorted(bestCycleBasedOnWeight)
    if len(bestCycleBasedOnWeight) != 0:
        return [bestCycleBasedOnWeight[0][1],bestCycleBasedOnWeight[0][2]]
    return[]

def getAssignedImage(shape, assignments):
    for assig in assignments:
        if assignments[assig] == shape:
            return shape
    sys.exit("Error")
    exit()


def getFeasibleAssignment(remainingShapes, usedShapes, assignments):
    feasibleAssignmentList = []
    for elem in remainingShapes:
        shapeNeigh = getNodeNeighbours(elem, data.m, data.hMatrix)
        for used in usedShapes:
            if used in shapeNeigh:
                usedImageNeighbour = 0
                for assig in assignments:
                    if assig == used:
                        usedImageNeighbour = assignments[assig]
                assigNeigh = getNodeNeighbours(usedImageNeighbour, data.n, data.gMatrix)
                for n in assigNeigh:
                    if n not in assignments.keys():
                        nNeigh = getNodeNeighbours(n, data.n, data.gMatrix)
                        if len(shapeNeigh) <= len(nNeigh):
                            weight = abs(data.gMatrix[n,used]-data.hMatrix[elem,used])
                            feasibleAssignmentList.append([weight, elem, n])
    feasibleAssignmentList = sorted(feasibleAssignmentList)
    if len(feasibleAssignmentList) == 0:
        return []
    else:
        return [feasibleAssignmentList[0][1], feasibleAssignmentList[0][2]]

def getFirstAssignment():
    maxNeighbourhoodShapeNode = 0
    shapeNodeNeighbourCount = 0
    for nodeId in range(data.m):
        localNodeNeighbours = getNodeNeighbours(nodeId, data.m, data.hMatrix)
        if len(localNodeNeighbours) > shapeNodeNeighbourCount:
            maxNeighbourhoodShapeNode = nodeId
            shapeNodeNeighbourCount = len(localNodeNeighbours)

    maxNeighbourhoodImageNode = 0
    imageNodeNeighbourCount = 0
    for nodeId in range(data.n):
        localNodeNeighbours = getNodeNeighbours(nodeId, data.n, data.gMatrix)
        if len(localNodeNeighbours) > imageNodeNeighbourCount:
            maxNeighbourhoodImageNode = nodeId
            imageNodeNeighbourCount = len(localNodeNeighbours)

    if shapeNodeNeighbourCount <= imageNodeNeighbourCount:
        return [maxNeighbourhoodShapeNode, maxNeighbourhoodImageNode]
    else:
        return []

def run():
    assignments = {}
    usedShapes = set()
    imageCycles = getCycles(0, data.n, data.gMatrix)
    shapeCycles = getCycles(0, data.m, data.hMatrix)

    while len(assignments) < data.m:
        maxShapeCycle = 0
        maxImageCycle = 0
        if len(shapeCycles) > 0:
            maxShapeCycle = max(shapeCycles, key=shapeCycles.get)
        if len(imageCycles) > 0:
            maxImageCycle = max(imageCycles, key=imageCycles.get)
        if maxShapeCycle > maxImageCycle: #we check if in case of having a cycle of shape matrix, if we could fit it in image
            sys.exit("INFEASIBLE")
            exit()
        else:
            if len(assignments) == 0 and len(shapeCycles) != 0: #we check if we have cycles remaining and if so we try to get a feasible place to assign them
                currentShapeCycle = shapeCycles[maxShapeCycle][0]
                bestCycleAssignment = getBestFeasableCycle(currentShapeCycle, imageCycles)
                if len(bestCycleAssignment) != 0:
                    for iter in range(len(currentShapeCycle)):
                        assignments[bestCycleAssignment[1][iter]] = bestCycleAssignment[0][iter]
                        usedShapes.add(bestCycleAssignment[0][iter])
                    imageCycles[maxShapeCycle].remove(set(bestCycleAssignment[1]))
                    shapeCycles[maxShapeCycle].remove(currentShapeCycle)
                    remove_empty_keys(imageCycles)
                    remove_empty_keys(shapeCycles)
                else:
                    sys.exit("INFEASIBLE")
                    exit()
            else:
                #we have no cycles so we must check were can we place it based on number of neighbours and if it has neighbours that have been previously assigned
                if len(assignments) == 0:
                    result = getFirstAssignment()
                    if len(result) != 0:
                        assignments[result[0]] = result[1]
                        usedShapes.add(result[0])
                    else:
                        sys.exit("INFEASIBLE")
                        exit()
                else:
                    remainingShapes = set(range(data.m))
                    remainingShapes = remainingShapes.difference(usedShapes)
                    result = getFeasibleAssignment(remainingShapes, usedShapes, assignments)
                    if len(result) != 0:
                        assignments[result[0]] = result[1]
                        usedShapes.add(result[0])
                    else:
                        sys.exit("INFEASIBLE")
                        exit()
    return assignments

if __name__ == '__main__':
    # Checks that the path to the instance exists
    fileCheck(sys.argv[1])

    # Loads the instance
    data = DataReader()
    data.load(sys.argv[1])
    data.check()

    start = timeit.default_timer()
    assignments = run()
    print("Assignments")
    print(assignments)

    #swap assignments to better operate
    reversedDict = {}
    for assign in assignments:
        reversedDict[assignments[assign]] = assign

    #finalMatrix = getFinalMatrix(reversedDict)
    #print("Final Matrix")
    #print(finalMatrix)
    totalObjectiveValue = getFinalObjectiveValue(reversedDict)
    end = timeit.default_timer()

    print("--- Elapsed time: %s seconds ---" % (end - start))
    print("Objective value = ", totalObjectiveValue)