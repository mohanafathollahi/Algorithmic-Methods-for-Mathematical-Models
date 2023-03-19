import numpy as np
import sys
import re

class DataReader(object):
    def __init__(self):
        self.n = 0
        self.m = 0
        self.gMatrix = np.zeros((0,0))
        self.hMatrix = np.zeros((0,0))

    def load(self, path):
        self.n = 0
        self.m = 0
        self.gMatrix = np.zeros((0,0))
        self.hMatrix = np.zeros((0,0))

        file = open(path, "r")
        nStr = "n = "
        mStr = "m = "
        gStartingStr = "G ="
        hStartingStr = "H ="
        inMatrixG = False
        inMatrixH = False
        inMatrixRow = "[ "
        matrixI_it = 0
        matrixJ_it = 0


        for line in file:
            if nStr in line: #obtain value of n
                self.n = int(line.split(nStr)[-1].split(";")[0])
                self.gMatrix = np.zeros((self.n, self.n))
            elif mStr in line: #obtain value of m
                self.m = int(line.split(mStr)[-1].split(";")[0])
                self.hMatrix = np.zeros((self.m, self.m))
            elif gStartingStr in line:  #check start of matrix g
                if(self.n <= 0):
                    self.errorThrow("Not a valid number for 'n' specified.")
                inMatrixG = True
                inMatrixH = False
                matrixI_it = 0
            elif hStartingStr in line:  #check start of matrix h
                if (self.m <= 0):
                    self.errorThrow("Not a valid number for 'm' specified.")
                inMatrixH = True
                inMatrixG = False
                matrixI_it = 0
            elif inMatrixG and (inMatrixRow in line):  #get row of values of matrix g
                if (self.n <= 0):
                    self.errorThrow("'n' value must be specified before the declaration of the matrix.")
                splitedLine = line.split('[')[-1].split(']')[0].strip().split(" ")
                matrixJ_it = 0
                for split in splitedLine:
                    if split != '' and split != "\t":
                        self.gMatrix[matrixI_it, matrixJ_it] = split
                        matrixJ_it = matrixJ_it + 1
                matrixI_it = matrixI_it + 1
                if (matrixJ_it == self.n - 1):
                    self.errorThrow("Not enough values in the declaration of the G matrix.")
            elif inMatrixH and (inMatrixRow in line):  #get row of values of matrix h
                if (self.m <= 0):
                    self.errorThrow("'m' value must be specified before the declaration of the matrix.")
                splitedLine = line.split('[')[-1].split(']')[0].strip().split(" ")
                matrixJ_it = 0
                for split in splitedLine:
                    if split != '' and split != "\t":
                        self.hMatrix[matrixI_it, matrixJ_it] = split
                        matrixJ_it = matrixJ_it + 1
                matrixI_it = matrixI_it + 1
                if (matrixJ_it == self.m - 1):
                    self.errorThrow("Not enough values in the declaration of the H matrix.")

        #print("Input file data:")
        #print(self.n)
        #print(self.m)
        #print(self.gMatrix)
        #print(self.hMatrix)

    def errorThrow(self, error):
        sys.exit(error)
        exit()

    def check(self):
        #check image
        for i in range(self.n):
            for j in range(self.n):
                if self.gMatrix[i][j] != self.gMatrix[j][i]:
                    self.errorThrow("Inconsistency in G matrix")
                if self.gMatrix[i][j] != 0 and i == j:
                    self.errorThrow("Inconsistency in G matrix")
        # check shape
            for i in range(self.m):
                for j in range(self.m):
                    if self.hMatrix[i][j] != self.hMatrix[j][i]:
                        self.errorThrow("Inconsistency in H matrix")
                    if self.hMatrix[i][j] != 0 and i == j:
                        self.errorThrow("Inconsistency in H matrix")
