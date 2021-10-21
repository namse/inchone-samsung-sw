from enum import Enum

# N은 항상 홀수이다.
# (r, c)는 격자의 r행 c열을 의미한다.
# 격자의 가장 왼쪽 윗 칸은 (1, 1)이다.
# 가장 오른쪽 아랫 칸은 (N, N)이다.
# 마법사 상어는 ((N+1)/2, (N+1)/2)에 있다.

# 일부 칸과 칸 사이에는 벽이 세워져 있다.

# 가장 처음에 상어가 있는 칸을 제외한 나머지 칸에는 구슬이 하나 들어갈 수 있다.
# 구슬은 1번 구슬, 2번 구슬, 3번 구슬이 있다.
# 연속하는 구슬: 같은 번호를 가진 구슬이 번호가 연속하는 칸에 있으면, 그 구슬을 연속하는 구슬이라고 한다.

# 블리자드 마법을 시전하려면 방향 di와 거리 si를 정해야 한다.
# 마법 = {di, si}
# 총 4가지 방향 ↑, ↓, ←, →가 있고, 정수 1, 2, 3, 4로 나타낸다.

# 상어는 di 방향으로 거리가 si 이하인 모든 칸에 있는 구슬을 모두 파괴한다.
# 구슬이 파괴되면 그 칸은 구슬이 들어있지 않은 빈 칸이 된다.
# 벽은 파괴되지 않는다.

	
# 폭발하는 구슬은 4개 이상 연속하는 구슬이 있을 때 발생한다.
	
# 구슬이 폭발해 빈 칸이 생겼으니 다시 구슬이 이동한다.
# 구슬이 이동한 후에는 다시 구슬이 폭발하는 단계입니다.
# 이 과정은 더 이상 폭발하는 구슬이 없을때까지 반복된다.

# 이제 더 이상 폭발한 구슬이 없을 때 구슬이 변화하는 단계가 된다.
# 연속하는 구슬은 하나의 그룹이라고 한다.
# 하나의 그룹은 두 개의 구슬 A와 B로 변한다.
# 구슬 A의 번호는 그룹에 들어있는 구슬의 개수이고,
# B는 그룹을 이루고 있는 구슬의 번호이다.

# 구슬은 다시 그룹의 순서대로 1번 칸부터 차례대로 A, B의 순서로 칸에 들어간다.
# 만약, 구슬이 칸의 수보다 많아 칸에 들어가지 못하는 경우 그러한 구슬은 사라진다.


# 마법사 상어는 블리자드를 총 M번 시전했다.
# 1×(폭발한 1번 구슬의 개수) + 2×(폭발한 2번 구슬의 개수) + 3×(폭발한 3번 구슬의 개수)를 구해보자.

from typing import Dict, List

class Position:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

class Grid:
    def __init__(self, sideLength: int) -> None:
        self.sideLength = sideLength
        self.stoneData = [[0 for _ in range(sideLength)] for _ in range(sideLength)]
        self.center = int((sideLength + 1) / 2)

    def getNextPosition(self, position: Position) -> Position or None:
        center = self.center
        col = position.col
        row = position.row

        if col == 1 and row == 1:
            return None

        if center < row and 2 * center - row <= col and col <= row - 1:
            return Position(row, col + 1)

        if col < center and col + 1 <= row and row <= 2 * center - col - 1:
            return Position(row + 1, col)

        if row <= center and row <= col and col <= 2 * center - row:
            return Position(row, col - 1)

        return Position(row - 1, col)

    def moveStonesForward(self) -> None:
        while True:
            stonePosition = Position(self.center, self.center - 1)
            isMovedAnyStone = False
            while True:
                nextPosition = self.getNextPosition(stonePosition)
                if nextPosition is None:
                    break
                if self.getStoneValue(stonePosition) == 0 and self.getStoneValue(nextPosition) != 0: 
                    nextPositionStoneValue = self.getStoneValue(nextPosition)
                    self.setStoneValue(stonePosition, nextPositionStoneValue)
                    self.setStoneValue(nextPosition, 0)
                    isMovedAnyStone = True

                stonePosition = nextPosition

            if isMovedAnyStone == False:
                break
    def setStoneValue(self, position: Position, value: int) -> None:
        self.stoneData[position.row - 1][position.col - 1] = value

    def getStoneValue(self, position: Position) -> int:
        return self.stoneData[position.row - 1][position.col - 1]

    def clear(self) -> None:
        self.stoneData = [[0 for _ in range(self.sideLength)] for _ in range(self.sideLength)]

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Magic:
    def __init__(self, direction: Direction, distance: int) -> None:
        self.direction = direction
        self.distance = distance

class Context:
    def __init__(self, gird: Grid, magics: List[Magic]) -> None:
        self.grid = gird
        self.magics = magics

def getContextFromInput() -> Context:
    (sideLength, magicCount) = map(int, input().split())
    grid = Grid(sideLength)

    for row in range(1, sideLength + 1):
        rowStoneData = list(map(int, input().split()))
        for col in range(1, sideLength + 1):
            stone = rowStoneData[col - 1]
            position = Position(row, col)
            grid.setStoneValue(position, stone)
    
    magics = []
    for _ in range(magicCount):
        (directionValue, distance) = map(int, input().split())
        magics.append(Magic(Direction(directionValue), distance))
    
    return Context(grid, magics)

directionRowColDeltaMap = {
    Direction.UP: (-1, 0),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
    Direction.RIGHT: (0, 1),
}

def getPositionsToDestory(context: Context, magic: Magic) -> List[Position]:
    positions = []

    center = context.grid.center

    (rowDelta, colDelta) = directionRowColDeltaMap[magic.direction]

    for distance in range(1, magic.distance + 1):
        row = center + rowDelta * distance
        col = center + colDelta * distance
        destoryPosition = Position(row, col)
        positions.append(destoryPosition)

    return positions

def useMagic(context: Context, magic: Magic) -> None:
    positionsToDestory: List[Position] = getPositionsToDestory(context, magic)

    for position in positionsToDestory:
        context.grid.setStoneValue(position, 0)

def moveStonesForward(context: Context) -> None:
    context.grid.moveStonesForward()

def destory4ContiguousStones(context: Context) -> Dict[int, int]:
    center = context.grid.center

    position = Position(center, center - 1)
    
    destoriedStones = {1: 0, 2: 0, 3: 0}

    while position is not None:
        stoneValue = context.grid.getStoneValue(position)

        if stoneValue == 0:
            position = context.grid.getNextPosition(position)
            continue
        
        sameStoneCount = 1
        nextPosition = context.grid.getNextPosition(position)
        while nextPosition is not None:
            nextPositionStoneValue = context.grid.getStoneValue(nextPosition)
            if nextPositionStoneValue != stoneValue:
                break
            sameStoneCount += 1
            nextPosition = context.grid.getNextPosition(nextPosition)
        
        if sameStoneCount < 4:
            position = nextPosition
            continue

        destoriedStones[stoneValue] += sameStoneCount

        for _ in range(sameStoneCount):
            context.grid.setStoneValue(position, 0)
            position = context.grid.getNextPosition(position)

    return destoriedStones

def addDestoriedStones(destoriedStones: Dict[int, int], destoriedStonesToAdd: Dict[int, int]) -> None:
    for stoneValue in destoriedStonesToAdd:
        destoriedStones[stoneValue] += destoriedStonesToAdd[stoneValue]

class Group:
    def __init__(self, stoneValue: int, stoneCount: int) -> None:
        self.stoneValue = stoneValue
        self.stoneCount = stoneCount

def makeGroups(context: Context) -> List[Group]:
    groups: List[Group] = []
    center = context.grid.center

    position = Position(center, center - 1)

    while position is not None:
        stoneValue = context.grid.getStoneValue(position)

        if stoneValue == 0:
            position = context.grid.getNextPosition(position)
            continue
        
        sameStoneCount = 1
        nextPosition = context.grid.getNextPosition(position)
        while nextPosition is not None:
            nextPositionStoneValue = context.grid.getStoneValue(nextPosition)
            if nextPositionStoneValue != stoneValue:
                break
            sameStoneCount += 1
            nextPosition = context.grid.getNextPosition(nextPosition)
        
        group = Group(stoneValue, sameStoneCount)
        groups.append(group)

        position = nextPosition

    return groups

def convertGroupsToStones(groups: List[Group]) -> List[int]:
    stones: List[int] = []
    for group in groups:
        stones.append(group.stoneCount)
        stones.append(group.stoneValue)
    return stones

def clearStones(context: Context) -> None:
    context.grid.clear()

def fillStones(context: Context, stones: List[int]) -> None:
    center = context.grid.center

    position = Position(center, center - 1)

    for stone in stones:
        if position is None:
            break
        context.grid.setStoneValue(position, stone)
        position = context.grid.getNextPosition(position)


# 격자 등 문제를 풀기 위한 정보를 가져온다.
context = getContextFromInput()
accumulatedDestoriedStones = {1: 0, 2: 0, 3: 0}

def getAllPositions(context: Context) -> List[Position]:
    positions = []
    center = context.grid.center
    position = Position(center, center - 1)

    while position is not None:
        positions.append(position)
        position = context.grid.getNextPosition(position)
    
    return positions

# M번 동안 다음을 시도한다.
for magic in context.magics:
    #   1. 블리자드 쏜다.
    useMagic(context, magic)

    #   2. 구슬들을 앞으로 땡긴다.
    moveStonesForward(context)


    print('-----AFTER PUSH FORWARD--------')
    for row in range(1, context.grid.sideLength + 1):
        line = ''
        for col in range(1, context.grid.sideLength + 1):
            position = Position(row, col)
            stoneValue = context.grid.getStoneValue(position)
            line += f"{stoneValue} "
        print(line)

    print('-------------\n\n\n\n')    

    while True:
        #   3. 4연속 구슬들 터트린다.
        destoriedStones = destory4ContiguousStones(context)

        print('-------------')    
        print(destoriedStones)


        print('-------------')
        for row in range(1, context.grid.sideLength + 1):
            line = ''
            for col in range(1, context.grid.sideLength + 1):
                position = Position(row, col)
                stoneValue = context.grid.getStoneValue(position)
                line += f"{stoneValue} "
            print(line)

        print('-------------\n\n\n\n')    
        
        #   3.1 터트린 구슬을 저장한다.
        addDestoriedStones(accumulatedDestoriedStones, destoriedStones)

        #   4. 만약 4연속 구슬 터진게 하나도 없으면 6으로 이동.
        
        for stoneValue in destoriedStones.values():
            print(stoneValue)
        isNoStonesDestroyed = all([stoneValue == 0 for stoneValue in destoriedStones.values()])
        print(f"isNoStonesDestroyed: {isNoStonesDestroyed}")
        if isNoStonesDestroyed:
            break
        
        #   5. 구슬들을 앞으로 땡긴다. 3번으로 간다.
        moveStonesForward(context)
    

    #   6. 구슬들을 그룹으로 만든다.
    groups = makeGroups(context)

    # 그룹을 다시 구슬로 바꿔 격자를 채운다.
    stones = convertGroupsToStones(groups)
    clearStones(context)
    fillStones(context, stones)

print(accumulatedDestoriedStones)

firstStoneCount = accumulatedDestoriedStones[1]
secondStoneCount = accumulatedDestoriedStones[2]
thirdStoneCount = accumulatedDestoriedStones[3]

# 터트린 구슬들을 가지고
# 1 * 1번구슬갯수 + 2 * 2번구슬갯수 + 3 * 3번구슬갯수 값을 출력한다.
print(firstStoneCount * 1 + secondStoneCount * 2 + thirdStoneCount * 3)



# allPositions = getAllPositions(context)

# print(context.grid.center)

# for position in allPositions:
#     print(position.row, position.col)