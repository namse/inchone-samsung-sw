# 이 나라의 지도는 N×M 크기의 이차원 격자로 나타낼 수 있고, 격자의 각 칸은 땅이거나 바다이다.

# 섬은 연결된 땅이 상하좌우로 붙어있는 덩어리를 말한다.

# 다리는 바다에만 건설할 수 있다.
# 다리의 길이는 다리가 격자에서 차지하는 칸의 수이다.
# 다리를 연결해서 모든 섬을 연결하려고 한다.
# 섬 A에서 다리를 통해 섬 B로 갈 수 있을 때, 섬 A와 B를 연결되었다고 한다.
# 다리의 양 끝은 섬과 인접한 바다 위에 있어야 한다.
# 다리의 방향이 중간에 바뀌면 안된다.
# 다리의 길이는 2 이상이어야 한다.

# 방향이 가로인 다리는 다리의 양 끝이 가로 방향으로 섬과 인접해야 한다.
# 방향이 세로인 다리는 다리의 양 끝이 세로 방향으로 섬과 인접해야 한다.

# 섬 A와 B를 연결하는 다리가 중간에 섬 C와 인접한 바다를 지나가는 경우에
# 섬 C는 A, B와 연결되어있는 것이 아니다.


# 다리가 교차하는 경우가 있을 수도 있다.
# 교차하는 다리의 길이를 계산할 때는 각 칸이 각 다리의 길이에 모두 포함되어야 한다.
	
# 나라의 정보가 주어졌을 때, 모든 섬을 연결하는 다리 길이의 최솟값을 구해보자.

from enum import Enum
from typing import List, Tuple

class Topography(Enum):
    SEA = 0
    ISLAND = 1

class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

class Position:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

class World:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.data = [[Topography.SEA for _ in range(cols)] for _ in range(rows)]

    # row and col's index are zero-based
    def setTopography(self, row: int, col: int, topography: Topography) -> None:
        self.data[row][col] = topography

    def isOutOfWorld(self, position: Position)-> bool:
        return position.row < 0 or position.row >= self.rows or position.col < 0 or position.col >= self.cols

    def isOnGround(self, position: Position) -> bool:
        return self.data[position.row][position.col] == Topography.ISLAND

def getAllDirectionAndNextPositionTuples(position: Position) -> List[Tuple[Direction, Position]]:
    return [
        (Direction.LEFT, Position(position.row, position.col - 1)),
        (Direction.RIGHT, Position(position.row, position.col + 1)),
        (Direction.UP, Position(position.row + 1, position.col)),
        (Direction.DOWN, Position(position.row - 1, position.col))
    ]

class Island:
    def __init__(self, grounds: List[Position], id: int) -> None:
        self.grounds = grounds
        self.id = id

    def isIn(self, position: Position) -> bool:
        for ground in self.grounds:
            if ground.row == position.row and ground.col == position.col:
                return True
        return False

    def getBorderAndDirectionTuples(self, world: World) -> List[Tuple[Position, Direction]]:
        tuples = []
        for ground in self.grounds:
            directionAndNextPositionTuples = getAllDirectionAndNextPositionTuples(ground)
            for (direction, nextPosition) in directionAndNextPositionTuples:
                if not world.isOutOfWorld(nextPosition) and not world.isOnGround(nextPosition):
                    tuples.append((ground, direction))
        return tuples

class ProblemContext:
    def __init__(self, world: World, islands: List[Island]) -> None:
        self.world = world
        self.islands = islands

def isPositionInList(targetPosition: Position, positions: List[Position]) -> bool:
    return any([targetPosition.row == position.row
                and targetPosition.col == position.col
                for position in positions])

def getConnectedGroundPositions(world: World, position: Position) -> List[Position]:
    searchedGrounds: List[Position] = []
    searchingGrounds: List[Position] = [position]

    while len(searchingGrounds) > 0:
        searchingGround = searchingGrounds.pop()
        searchedGrounds.append(searchingGround)
        allDirectionAndNextPositionTuples = getAllDirectionAndNextPositionTuples(searchingGround)
        for (_, nextPosition) in allDirectionAndNextPositionTuples:
            if world.isOutOfWorld(nextPosition) or not world.isOnGround(nextPosition):
                continue
            if isPositionInList(nextPosition, searchedGrounds) \
            or isPositionInList(nextPosition, searchingGrounds):
                continue
            
            searchingGrounds.append(nextPosition)

    return searchedGrounds

def getIslandsFromWorld(world: World) -> List[Island]:
    checkedPositions: List[Position] = []
    islands = []
    islandId = 0
    for row in range(world.rows):
        for col in range(world.cols):
            position = Position(row, col)
            if not world.isOnGround(position):
                continue
            if any([
                checkedPosition.row == row and checkedPosition.col == col
                for checkedPosition in checkedPositions
            ]):
                continue
            grounds = getConnectedGroundPositions(world, Position(row, col))
            for ground in grounds:
                checkedPositions.append(ground)
            island = Island(grounds, islandId)
            islandId += 1
            islands.append(island)

    return islands

def getProblemContextFromInput() -> ProblemContext:
    (rows, cols) = map(int, input().split())

    world = World(rows, cols)

    for row in range(rows):
        rowData = list(map(int, input().split()))
        for col in range(cols):
            topography = Topography(rowData[col])
            world.setTopography(row, col, topography)
    
    islands = getIslandsFromWorld(world)

    return ProblemContext(world, islands)

def getAllIslandTuples(context: ProblemContext) -> List[Tuple[Island, Island]]:
    tuples = []
    for indexA in range(len(context.islands)):
        for indexB in range(indexA + 1, len(context.islands)):
            tuples.append((context.islands[indexA], context.islands[indexB]))  

    return tuples

def selectAllIslandTupleListCases(\
    islandTuples: List[Tuple[Island, Island]],\
    bridgeCount: int\
) -> List[List[Tuple[Island, Island]]]:
    result: List[List[Tuple[Island, Island]]] = []

    if bridgeCount == 0 or len(islandTuples) < bridgeCount:
        return []

    if bridgeCount == 1:
        return [[islandTuple] for islandTuple in islandTuples]

    for index in range(len(islandTuples)):
        subIslandTuples = islandTuples[index + 1:]
        subCases = selectAllIslandTupleListCases(subIslandTuples, bridgeCount - 1)
        for subCase in subCases:
            subCase.append(islandTuples[index])
            result.append(subCase)
    
    return result

def getAllIslandTupleListCases(context: ProblemContext) -> List[List[Tuple[Island, Island]]]:
    islandCount = len(context.islands)
    bridgeCount = islandCount - 1

    allIslandTuples: List[Tuple[Island, Island]] = getAllIslandTuples(context)

    allIslandTupleListCases = selectAllIslandTupleListCases(allIslandTuples, bridgeCount)

    return allIslandTupleListCases

class BridgeConnectionResult:
    def __init__(self, isSuccessful: bool, length: int or None) -> None:
        self.isSuccessful = isSuccessful
        self.length = length

class TryGetToIslandResult:
    def __init__(self, isSuccessful: bool, length: int or None) -> None:
        self.isSuccessful = isSuccessful
        self.length = length

def getNextPosition(position: Position, direction: Direction) -> Position:
    for (tupleDirection, nextPosition) in getAllDirectionAndNextPositionTuples(position):
        if tupleDirection == direction:
            return nextPosition

def tryGetToIsland(\
    context: ProblemContext,\
    border: Position,\
    direction: Direction,\
    island: Island\
) -> TryGetToIslandResult:
    length = 1
    targetPosition = getNextPosition(border, direction)
    while not context.world.isOutOfWorld(targetPosition):
        if island.isIn(targetPosition):
            bridgeLength = length - 1
            isSuccessful = bridgeLength > 1
            return TryGetToIslandResult(isSuccessful, bridgeLength)
        
        if context.world.isOnGround(targetPosition):
            return TryGetToIslandResult(False, None)

        targetPosition = getNextPosition(targetPosition, direction)
        length += 1
    
    return TryGetToIslandResult(False, None)

def tryConnectIslandsWithShortestBridge(\
    context: ProblemContext,\
    islandTuple: Tuple[Island, Island]\
)-> BridgeConnectionResult:
    (islandA, islandB) = islandTuple
    minBridgeLength = None

    borderAndDirectionTuples = islandA.getBorderAndDirectionTuples(context.world)
    for (border, direction) in borderAndDirectionTuples:
        result = tryGetToIsland(context, border, direction, islandB)
        if result.isSuccessful:
            if minBridgeLength is None or result.length < minBridgeLength:
                minBridgeLength = result.length
    
    return BridgeConnectionResult(minBridgeLength is not None, minBridgeLength)

def tryConnectAllIslandWithShortestBridges(\
    context: ProblemContext,\
    islandTupleList: List[Tuple[Island, Island]]\
)-> BridgeConnectionResult:
    sumOfLength = 0

    for islandTuple in islandTupleList:
        result = tryConnectIslandsWithShortestBridge(context, islandTuple)
        if not result.isSuccessful:
            return BridgeConnectionResult(False, None)
        sumOfLength += result.length

    return BridgeConnectionResult(True, sumOfLength)


# 지도와 섬에 대한 정보들을 입력으로 부터 가져온다.
context = getProblemContextFromInput()

# 모든 섬들이 연결되기 위한 섬 쌍의 리스트의 경우의 수 를 구한다.
allIslandTupleListCases = getAllIslandTupleListCases(context)

minSumOfBridgeLengths = -1

# 모든 섬을 연결시키는 다리에 대한 경우의 수 에 대해,
for islandTupleList in allIslandTupleListCases:
    # 두 섬을 연결시키는 최소 길이의 다리들을 놓아 연결하고,
    bridgeConnectionResult = tryConnectAllIslandWithShortestBridges(context, islandTupleList)
    if not bridgeConnectionResult.isSuccessful:
        continue

    # 그 때의 다리 길이의 합의 최솟값을 구한다.
    if minSumOfBridgeLengths == -1 or minSumOfBridgeLengths > bridgeConnectionResult.length:
        minSumOfBridgeLengths = bridgeConnectionResult.length

# 다리 길이의 최소값을 출력한다. 단, 연결하는게 불가능하면 -1을 출력해다오.
print(minSumOfBridgeLengths)