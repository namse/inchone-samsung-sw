from typing import List

class Belt:
    pass

# 벨트가 각 칸 위에 있는 로봇과 함께 한 칸 회전한다.
def rotateBelt(belt: Belt):
    pass

# 가장 먼저 벨트에 올라간 로봇부터, 벨트가 회전하는 방향으로 한 칸 이동할 수 있다면 이동한다. 만약 이동할 수 없다면 가만히 있는다.
    # 로봇이 이동하기 위해서는 이동하려는 칸에 로봇이 없으며, 그 칸의 내구도가 1 이상 남아 있어야 한다.
def moveRobot(belt: Belt):
    pass

# 올리는 위치에 있는 칸의 내구도가 0이 아니면 올리는 위치에 로봇을 올린다.
def putRobot(belt: Belt):
    pass

# 내구도가 0인 칸의 개수가 K개 이상이라면 과정을 종료한다. 그렇지 않다면 1번으로 돌아간다.
def hasProblemWithBeltDurability(belt: Belt, maximumCount: int) -> bool:
    pass

def createBelt(size: int, durabilities: List[int]) -> Belt:
    pass

(n, k) = map(int, input().split())
durabilities = list(map(int, input().split()))

belt = createBelt(n, durabilities)

trial = 0
while True:
    trial += 1
    rotateBelt(belt)
    moveRobot(belt)
    putRobot(belt)
    if hasProblemWithBeltDurability(belt, k):
        break

print(trial)