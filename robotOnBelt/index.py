from typing import List

class Belt:
    def __init__(self, size: int, durabilities: List[int]) -> None:
        self.size = size
        self.durabilities = durabilities
        self.robotPositions = []

# 벨트가 각 칸 위에 있는 로봇과 함께 한 칸 회전한다.
def rotateBelt(belt: Belt) -> None:
    rotatedDurabilities = belt.durabilities[-1:] + belt.durabilities[:-1]
    belt.durabilities = rotatedDurabilities

    belt.robotPositions = [getNextPosition(belt, position) for position in belt.robotPositions]
    
    pullPosition = belt.size - 1
    belt.robotPositions = [position for position in belt.robotPositions if position != pullPosition]


def getNextPosition(belt: Belt, position: int) -> int:
    nextPosition = position + 1
    if nextPosition == belt.size * 2:
        nextPosition = 0
    return nextPosition

# 가장 먼저 벨트에 올라간 로봇부터, 벨트가 회전하는 방향으로 한 칸 이동할 수 있다면 이동한다. 만약 이동할 수 없다면 가만히 있는다.
    # 로봇이 이동하기 위해서는 이동하려는 칸에 로봇이 없으며, 그 칸의 내구도가 1 이상 남아 있어야 한다.
def rotateRobots(belt: Belt):
    robotIndex = 0
    for _ in range(len(belt.robotPositions)):
        pullPosition = belt.size - 1

        position = belt.robotPositions[robotIndex]
        nextPosition = getNextPosition(belt, position)

        if not canPutRobot(belt, nextPosition):
            continue

        belt.robotPositions[robotIndex] = nextPosition
        belt.durabilities[nextPosition] -= 1

        if nextPosition == pullPosition:
            belt.robotPositions.pop(robotIndex)
            continue
        
        robotIndex += 1
        
def canPutRobot(belt: Belt, position: int) -> bool:
    isNextPositionDurabilityOk = belt.durabilities[position] > 0
    isNoRobotOnNextPosition = not any(position == robotPosition for robotPosition in belt.robotPositions)
    return isNextPositionDurabilityOk and isNoRobotOnNextPosition

# 올리는 위치에 있는 칸의 내구도가 0이 아니면 올리는 위치에 로봇을 올린다.
def putRobot(belt: Belt):
    putPosition = 0
    if canPutRobot(belt, putPosition):
        belt.robotPositions.append(putPosition)
        belt.durabilities[putPosition] -= 1

# 내구도가 0인 칸의 개수가 K개 이상이라면 과정을 종료한다. 그렇지 않다면 1번으로 돌아간다.
def hasProblemWithBeltDurability(belt: Belt, maximumCount: int) -> bool:
    return len([durability for durability in belt.durabilities if durability <= 0]) >= maximumCount

def createBelt(size: int, durabilities: List[int]) -> Belt:
    return Belt(size, durabilities)

(n, k) = map(int, input().split())
durabilities = list(map(int, input().split()))

belt = createBelt(n, durabilities)

trial = 0
while True:
    trial += 1
    rotateBelt(belt)
    rotateRobots(belt)
    putRobot(belt)
    if hasProblemWithBeltDurability(belt, k):
        break

print(trial)