from __future__ import annotations
from typing import Generator, List

# 캐슬 디펜스는 성을 향해 몰려오는 적을 잡는 턴 방식의 게임이다.
# 게임이 진행되는 곳은 크기가 N×M인 격자판으로 나타낼 수 있다.
# 격자판은 1×1 크기의 칸으로 나누어져 있다.
# 각 칸에 포함된 적의 수는 최대 하나이다.


# 궁수의 공격이 끝나면 적이 이동한다.
# 적이 성이 있는 칸으로 이동한 경우에는 게임에서 제외된다.
# 모든 적이 격자판에서 제외되면 게임이 끝난다.

# 궁수의 공격으로 제거할 수 있는 적의 최대 수를 계산해보자.

class Field:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.enemyExistsMatrix = [[False for _ in range(cols)] for _ in range(rows)]

    # 적은 아래로 한 칸 이동한다.
    def moveAllEnemiesDown(self) -> None:
        for row in range(self.rows -2, -1, -1):
            for col in range(self.cols):
                self.enemyExistsMatrix[row+1][col] = self.enemyExistsMatrix[row][col]
        
        for col in range(self.cols):
            self.enemyExistsMatrix[0][col] = False

    def setEnemy(self, row: int, col: int) -> None:
        self.enemyExistsMatrix[row][col] = True
    
    def killEnemy(self, row: int, col: int) -> bool:
        isEnemyExists = self.enemyExistsMatrix[row][col]
        self.enemyExistsMatrix[row][col] = False
        return isEnemyExists

    def enemyExists(self, row: int, col: int) -> bool:
        return self.enemyExistsMatrix[row][col]
    
    def copy(self) -> Field:
        field = Field(self.rows, self.cols)
        for row in range(self.rows):
            for col in range(self.cols):
                field.enemyExistsMatrix[row][col] = self.enemyExistsMatrix[row][col]
        return field
        

# 성을 적에게서 지키기 위해 궁수 3명을 배치하려고 한다.
# 궁수는 성이 있는 칸에 배치할 수 있다.
# 격자판의 N번행의 바로 아래(N+1번 행)의 모든 칸에는 성이 있다.
# 하나의 칸에는 최대 1명의 궁수만 있을 수 있다.
def getAllArchorColsCases(cols: int) -> Generator[List[int]]:
    for a in range(cols):
        for b in range(a + 1, cols):
            for c in range(b + 1, cols):
                yield [a, b, c]

# 각각의 턴마다 궁수는 적 하나를 공격할 수 있다.
# 모든 궁수는 동시에 공격한다.
# 궁수가 공격하는 적은 거리가 D이하인 적 중에서 가장 가까운 적이다.
# 공격할 수 있는 적이 여럿일 경우에는 가장 왼쪽에 있는 적을 공격한다.
# 같은 적이 여러 궁수에게 공격당할 수 있다.
# 공격받은 적은 게임에서 제외된다.
# 격자판의 두 위치 (r1, c1), (r2, c2)의 거리는 |r1-r2| + |c1-c2|이다.

class Position:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

def findClosestEnemyPosition(field: Field, archorCol: int, maxArchorRange: int) -> Position | None:
    archorPosition = Position(field.rows, archorCol)

    minDistance = maxArchorRange + 1
    minDistanceMostLeftEnemyPosition = None
    for row in range(field.rows):
        for col in range(field.cols):
            if not field.enemyExists(row, col):
                continue
            
            distance = abs(row - archorPosition.row) + abs(col - archorPosition.col)
            if distance > maxArchorRange or distance > minDistance:
                continue

            if minDistance == distance:
                if minDistanceMostLeftEnemyPosition is None or minDistanceMostLeftEnemyPosition.col > col:
                    minDistanceMostLeftEnemyPosition = Position(row, col)
            else:
                minDistance = distance
                minDistanceMostLeftEnemyPosition = Position(row, col)

    return minDistanceMostLeftEnemyPosition
    

def shootEnemy(field: Field, archorCols: List[int], maxArchorRange: int) -> int:
    killedEnemiesCount = 0
    targetEnemyPositions = [findClosestEnemyPosition(field, archorCol, maxArchorRange) for archorCol in archorCols]

    for targetEnemyPosition in targetEnemyPositions:
        if targetEnemyPosition is None:
            continue

        if field.killEnemy(targetEnemyPosition.row, targetEnemyPosition.col):
            killedEnemiesCount += 1
        
    return killedEnemiesCount

def calculateKilledEnemiesCount(field: Field, archorCols: List[int], maxArchorRange: int) -> int:
    field = field.copy()
    killedEnemiesCount = 0

    for _ in range(field.rows):
        killedEnemiesCount += shootEnemy(field, archorCols, maxArchorRange)
        field.moveAllEnemiesDown()
    
    return killedEnemiesCount


(rows, cols, maxArchorRange) = map(int, input().split())
field = Field(rows, cols)

for row in range(rows):
    columnEnemyList = list(map(int, input().split()))
    for col in range(cols):
        if columnEnemyList[col] == 1:
            field.setEnemy(row, col)

maxKilledEnemiesCount = 0
for archorCols in getAllArchorColsCases(cols):
    killedEnemiesCount = calculateKilledEnemiesCount(field, archorCols, maxArchorRange)
    if maxKilledEnemiesCount < killedEnemiesCount:
        maxKilledEnemiesCount = killedEnemiesCount

print(maxKilledEnemiesCount)