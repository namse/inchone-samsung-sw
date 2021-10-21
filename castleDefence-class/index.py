from __future__ import annotations
from typing import Generator, Iterable, List

# 캐슬 디펜스는 성을 향해 몰려오는 적을 잡는 턴 방식의 게임이다.

# 게임이 진행되는 곳은 크기가 N×M인 격자판으로 나타낼 수 있다.
# 격자판은 1×1 크기의 칸으로 나누어져 있다.
# 각 칸에 포함된 적의 수는 최대 하나이다.
# 격자판의 N번행의 바로 아래(N+1번 행)의 모든 칸에는 성이 있다.


# 궁수는 성이 있는 칸에 배치할 수 있다.

# 게임 설명에서 보다시피 궁수를 배치한 이후의 게임 진행은 정해져있다.
# 격자판의 상태가 주어졌을 때 궁수의 공격으로 제거할 수 있는 적의 최대 수를 계산해보자.

# 격자판의 두 위치 (r1, c1), (r2, c2)의 거리는 |r1-r2| + |c1-c2|이다.


class Grid:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.enemyExistsMatrix = [
            [False for _ in range(cols)]
                for _ in range(rows)]

    def setEnemyExists(self, row: int, col: int) -> None:
        self.enemyExistsMatrix[row][col] = True

    def killEnemy(self, row: int, col: int) -> bool:
        isEnemyExists = self.enemyExistsMatrix[row][col]
        self.enemyExistsMatrix[row][col] = False
        return isEnemyExists
    
    def isEnemyExists(self, row: int, col: int) -> bool:
        return self.enemyExistsMatrix[row][col]
    
    def moveEnemiesDown(self) -> None:
        for row in range(self.rows - 1, 0, -1):
            for col in range(self.cols):
                self.enemyExistsMatrix[row][col] = self.enemyExistsMatrix[row - 1][col]

        for col in range(self.cols):
            self.enemyExistsMatrix[0][col] = False
    
    def copy(self) -> Grid:
        newGrid = Grid(self.rows, self.cols)
        for row in range(self.rows):
            for col in range(self.cols):
                newGrid.enemyExistsMatrix[row][col] = self.enemyExistsMatrix[row][col]
        return newGrid

class InputResult:
    def __init__(self, grid: Grid, archorRangeLimit: int):
        self.grid = grid
        self.archorRangeLimit = archorRangeLimit


def processInput() -> InputResult:
    (rows, cols, archorRangeLimit) = map(int, input().split())
    grid = Grid(rows, cols)
    
    for row in range(rows):
        isEnemyExistsList = list(map(int, input().split()))
        for col in range(cols):
            isEnemyExists = isEnemyExistsList[col]
            if isEnemyExists == 1:
                grid.setEnemyExists(row, col)
    
    return InputResult(grid, archorRangeLimit)


def getAllArchorPositionsCases(grid: Grid) -> Generator[List[int], None, None]:
    # 성을 적에게서 지키기 위해 궁수 3명을 배치하려고 한다.
    # 하나의 칸에는 최대 1명의 궁수만 있을 수 있다.

    for firstArchorPosition in range(grid.cols):
        for secondArchorPosition in range(firstArchorPosition + 1, grid.cols):
            for thirdArchorPosition in range(secondArchorPosition + 1, grid.cols):
                yield [firstArchorPosition, secondArchorPosition, thirdArchorPosition]

class Position:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

def getAttackPosition(grid: Grid, archorRangeLimit: int, archorCol: int) -> Position or None:
    closestEnemyPosition: None or Position = None
    closestEnemyDistance: None or int = None

    for row in range(grid.rows):
        for col in range(grid.cols):
            if not grid.isEnemyExists(row, col):
                continue

            archorRow = grid.rows
            distance = abs(archorCol - col) + abs(row - archorRow)
            isInRange = distance <= archorRangeLimit

            if not isInRange:
                continue
            
            if closestEnemyDistance is None or distance < closestEnemyDistance or col < closestEnemyPosition.col:
                closestEnemyDistance = distance
                closestEnemyPosition = Position(row, col)
    
    return closestEnemyPosition

def getAttackPositions(grid: Grid, archorRangeLimit: int, archorCols: List[int]) -> List[Position]:
    attackPositions: List[Position] = []

    for archorCol in archorCols:
        attackPosition = getAttackPosition(grid, archorRangeLimit, archorCol)
        if attackPosition is not None:
            attackPositions.append(attackPosition)

    return attackPositions


def getKilledEnemyCount(grid: Grid, archorRangeLimit: int, archorPositionsCase: List[int]) -> int:
    grid = grid.copy()
    killedEnemyCount = 0
    for _ in range(grid.rows):
        attackPositions: List[Position] = getAttackPositions(grid, archorRangeLimit, archorPositionsCase)

        # 공격받은 적은 게임에서 제외된다.
        for attackPosition in attackPositions:
            if grid.killEnemy(attackPosition.row, attackPosition.col):
                killedEnemyCount += 1
        
        # 궁수의 공격이 끝나면 적이 아래로 한 칸 이동한다.
        # 적이 성이 있는 칸으로 이동한 경우에는 게임에서 제외된다.
        grid.moveEnemiesDown()

    return killedEnemyCount

def getAllKilledEnemyCounts(grid: Grid,
    archorRangeLimit: int,
    archorPositionsCases: Iterable[List[int]]) -> Generator[int, None, None]:
    for archorPositionsCase in archorPositionsCases:
        yield getKilledEnemyCount(grid, archorRangeLimit, archorPositionsCase)

    # 각각의 턴마다 궁수는 적 하나를 공격할 수 있다.
    # 모든 궁수는 동시에 공격한다.
    # 궁수가 공격하는 적은 거리가 D이하인 적 중에서 가장 가까운 적이다.
    # 궁수가 공격할 적이 여럿일 경우에는 가장 왼쪽에 있는 적을 공격한다.
    # 같은 적이 여러 궁수에게 공격당할 수 있다.
    # 모든 적이 격자판에서 제외되면 게임이 끝난다.

    

# 격자판과 궁수의 공격 거리 제한 등을 입력받아 준비한다.
inputResult = processInput()

# 궁수 배치의 모든 경우의 수를 구한다.
allArchorPositionsCases = getAllArchorPositionsCases(inputResult.grid)

# 각 궁수 배치마다 제거할 수 있는 적의 수를 구한다.
allKilledEnemyCounts = getAllKilledEnemyCounts(inputResult.grid, inputResult.archorRangeLimit, allArchorPositionsCases)

# 그 중 가장 큰 수를 구해 출력한다.
maxKilledEnemyCount = max(allKilledEnemyCounts)

print(maxKilledEnemyCount)
