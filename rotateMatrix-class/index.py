from __future__ import annotations
# 배열 A의 값은 각 행에 있는 모든 수의 합 중 최솟값을 의미한다.

# 회전 연산은 세 정수 (r, c, s)로 이루어져 있다.
# 회전 연산은 가장 왼쪽 윗 칸이 (r-s, c-s), 가장 오른쪽 아랫 칸이 (r+s, c+s)인 정사각형을 시계 방향으로 한 칸씩 돌리는 것이다.
# 배열의 칸 (r, c)는 r행 c열을 의미한다.
# 회전 연산이 두 개 이상이면, 연산을 수행한 순서에 따라 최종 배열이 다르다.

# 배열 A와 사용 가능한 회전 연산들이 주어졌을 때, 배열 A의 값의 최솟값을 구해보자.
# 회전 연산은 모두 한 번씩 사용해야 하며, 순서는 임의로 정해도 된다.

from typing import List

class Position:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

class Matrix:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        # data's base index = 0
        self.data = [[0] * cols for _ in range(rows)]

    def setValue(self, position: Position, value: int) -> None:
        self.data[position.row - 1][position.col - 1] = value

    def getValue(self, position: Position) -> int:
        return self.data[position.row - 1][position.col - 1]
    
    def copy(self) -> Matrix:
        new_matrix = Matrix(self.rows, self.cols)
        for row in range(self.rows):
            for col in range(self.cols):
                position = Position(row, col)
                new_matrix.setValue(position, self.getValue(position))
        return new_matrix
    
    def print(self) -> None:
        print('------------')
        for row in range(self.rows):
            logLine = ''
            for col in range(self.cols):
                position = Position(row, col)
                logLine += f"{self.getValue(position)} "
            print(logLine)
        print()

class RotateOperation:
    def __init__(self, row: int, col: int, radius: int) -> None:
        self.row = row
        self.col = col
        self.radius = radius

class InputResult:
    def __init__(self, matrix: Matrix, rotateOperations: List[RotateOperation]) -> None:
        self.matrix = matrix
        self.rotateOperations = rotateOperations

def processInput() -> InputResult:
    (rows, cols, operationCount) = map(int, input().split())
    matrix = Matrix(rows, cols)

    for row in range(1, rows+ 1):
        rowData = list(map(int, input().split()))
        for col in range(1, cols + 1):
            colData = rowData[col - 1]
            matrix.setValue(Position(row, col), colData)

    rotateOperations = []
    for _ in range(operationCount):
        (row, col, radius) = map(int, input().split())
        rotateOperation = RotateOperation(row, col, radius)
        rotateOperations.append(rotateOperation)

    return InputResult(matrix, rotateOperations)

def getAllRotateOperationsCases(rotateOperations: List[RotateOperation]) -> List[List[RotateOperation]]:
    if len(rotateOperations) <= 1:
        return [rotateOperations]
    result = []

    for index in range(len(rotateOperations)):
        nextRotateOperations = []
        for nextRotateOperationIndex in range(len(rotateOperations)):
            if nextRotateOperationIndex != index:
                nextRotateOperations.append(rotateOperations[nextRotateOperationIndex])

        subCases = getAllRotateOperationsCases(nextRotateOperations)

        for subCase in subCases:
            result.append([rotateOperations[index]] + subCase)

    return result

def getTargetPositions(centerPosition: Position, distance: int) -> List[Position]:
    targetPositions: List[Position] = []
    
    leftTop = Position(centerPosition.row - distance, centerPosition.col - distance)
    rightTop = Position(centerPosition.row - distance, centerPosition.col + distance)
    rightBottom = Position(centerPosition.row + distance, centerPosition.col + distance)
    leftBottom = Position(centerPosition.row + distance, centerPosition.col - distance)
    vertexAndDeltaList = [
        (leftTop, (0, +1)),
        (rightTop, (1, 0)),
        (rightBottom, (0, -1)),
        (leftBottom, (-1, 0)),
    ]
    for vertexAndDelta in vertexAndDeltaList:
        (vertex, delta) = vertexAndDelta
        for i in range(2 * distance):
            targetPosition = Position(vertex.row + i * delta[0], vertex.col + i * delta[1])
            targetPositions.append(targetPosition)

    return targetPositions

def rotateMatrix(matrix: Matrix, rotateOperations: List[RotateOperation]) -> None:
    matrix = matrix.copy()
    for rotateOperation in rotateOperations:
        for distance in range(1, rotateOperation.radius + 1):
            centerPosition = Position(rotateOperation.row, rotateOperation.col)
            targetPositions: List[Position] = getTargetPositions(centerPosition, distance)

            firstPosition = targetPositions[0]
            
            lastTargetPosition: Position = targetPositions[-1]
            lastTargetValue = matrix.getValue(lastTargetPosition)
            
            for index in range(len(targetPositions) - 2, -1, -1):
                targetPosition = targetPositions[index]
                targetValue = matrix.getValue(targetPosition)
            
                nextTargetPosition = targetPositions[index + 1]
                matrix.setValue(nextTargetPosition, targetValue)
            
            matrix.setValue(firstPosition, lastTargetValue)
        
        matrix.print()
    return matrix

def getMatrixValue(matrix: Matrix) -> int:
    sumOfRows = []
    
    for row in range(1, matrix.rows + 1):
        sumOfRow = 0
        for col in range(1, matrix.cols + 1):
            position = Position(row, col)
            sumOfRow += matrix.getValue(position)
        sumOfRows.append(sumOfRow)
    
    return min(sumOfRows)

# 입력 받아서 배열 A와 회전 연산들을 가져온다.
inputResult = processInput()

# 모든 회전 연산의 순서쌍을 가져온다.
allRotateOperationsCases = getAllRotateOperationsCases(inputResult.rotateOperations)

minimumMatrixValue: None or int = None

# 모든 회전 연산의 순서쌍에 대해서 배열 A를 회전연산한다.
for rotateOperations in allRotateOperationsCases:
    rotatedMatrix = rotateMatrix(inputResult.matrix, rotateOperations)

    # 회전된 배열의 크기가 가장 작을 때를 구한다.
    matrixValue = getMatrixValue(rotatedMatrix)
    if minimumMatrixValue == None or minimumMatrixValue > matrixValue:
        minimumMatrixValue = matrixValue

# 최전된 배열의 크기가 가장 작을 때의 값을 출력한다.
print(minimumMatrixValue)
