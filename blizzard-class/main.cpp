#include <iostream>
#include <map>
#include <vector>
// N은 항상 홀수이다.
// (r, c)는 격자의 r행 c열을 의미한다.
// 격자의 가장 왼쪽 윗 칸은 (1, 1)이다.
// 가장 오른쪽 아랫 칸은 (N, N)이다.
// 마법사 상어는 ((N+1)/2, (N+1)/2)에 있다.

// 일부 칸과 칸 사이에는 벽이 세워져 있다.

// 가장 처음에 상어가 있는 칸을 제외한 나머지 칸에는 구슬이 하나 들어갈 수 있다.
// 구슬은 1번 구슬, 2번 구슬, 3번 구슬이 있다.
// 연속하는 구슬: 같은 번호를 가진 구슬이 번호가 연속하는 칸에 있으면, 그 구슬을 연속하는 구슬이라고 한다.

// 블리자드 마법을 시전하려면 방향 di와 거리 si를 정해야 한다.
// 마법 = {di, si}
// 총 4가지 방향 ↑, ↓, ←, →가 있고, 정수 1, 2, 3, 4로 나타낸다.

// 상어는 di 방향으로 거리가 si 이하인 모든 칸에 있는 구슬을 모두 파괴한다.
// 구슬이 파괴되면 그 칸은 구슬이 들어있지 않은 빈 칸이 된다.
// 벽은 파괴되지 않는다.

// 폭발하는 구슬은 4개 이상 연속하는 구슬이 있을 때 발생한다.

// 구슬이 폭발해 빈 칸이 생겼으니 다시 구슬이 이동한다.
// 구슬이 이동한 후에는 다시 구슬이 폭발하는 단계입니다.
// 이 과정은 더 이상 폭발하는 구슬이 없을때까지 반복된다.

// 이제 더 이상 폭발한 구슬이 없을 때 구슬이 변화하는 단계가 된다.
// 연속하는 구슬은 하나의 그룹이라고 한다.
// 하나의 그룹은 두 개의 구슬 A와 B로 변한다.
// 구슬 A의 번호는 그룹에 들어있는 구슬의 개수이고,
// B는 그룹을 이루고 있는 구슬의 번호이다.

// 구슬은 다시 그룹의 순서대로 1번 칸부터 차례대로 A, B의 순서로 칸에 들어간다.
// 만약, 구슬이 칸의 수보다 많아 칸에 들어가지 못하는 경우 그러한 구슬은 사라진다.

// 마법사 상어는 블리자드를 총 M번 시전했다.
// 1×(폭발한 1번 구슬의 개수) + 2×(폭발한 2번 구슬의 개수) + 3×(폭발한 3번 구슬의 개수)를 구해보자.

class Grid
{
public:
    Grid(int sideLength) : sideLength(sideLength),
                           stoneData(std::vector<std::vector<int>>(sideLength,
                                                                   std::vector<int>(sideLength, 0)))
    {
    }

    int sideLength;
    std::vector<std::vector<int>> stoneData;
};

enum class Direction
{
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4,
};

class Magic
{
public:
    Magic(Direction direction, int distance) : direction(direction),
                                               distance(distance)
    {
    }

    Direction direction;
    int distance;
};

class Context
{
public:
    Context(
        Grid grid,
        std::vector<Magic> magics) : grid(grid), magics(magics)
    {
    }
    Grid grid;
    std::vector<Magic> magics;
};

Context getContextFromInput()
{
    int sideLength;
    int magicCount;
    std::cin >> sideLength >> magicCount;

    Grid grid(sideLength);

    for (int row = 1; row < sideLength + 1; row += 1)
    {
        for (int col = 1; col < sideLength + 1; col += 1)
        {
            int stone;
            std::cin >> stone;
            grid.setStone(row, col, stone);
        }
    }

    std::vector<Magic> magics;
    for (int magicIndex = 0; magicIndex < magicCount; magicIndex += 1)
    {
        int directionValue;
        int distance;
        std::cin >> directionValue >> distance;

        auto direction = Direction(directionValue);
        auto magic = Magic(direction, distance);
        magics.push_back(magic);
    }
    return Context(grid, magics);
}

struct Position
{
    Position(
        int row, int col) : row(row), col(col)
    {
    }
    int row;
    int col;
};

std::vector<Position> getPositionsToDestory(Context context, Magic magic)
{
    std::vector<Position> positions;
    const static std::map<Direction, std::pair<int, int>> directionRowColDeltaMap = {
        std::make_pair(Direction::UP, (-1, 0)),
        std::make_pair(Direction::DOWN, (1, 0)),
        std::make_pair(Direction::LEFT, (0, -1)),
        std::make_pair(Direction::RIGHT, (0, 1)),
    };

    auto center = (context.grid.sideLength + 1) / 2;

    auto pair = directionRowColDeltaMap.at(magic.direction);
    auto rowDelta = pair.first;
    auto colDelta = pair.second;

    for (auto distance = 1; distance <= distance + 1; distance += 1)
    {
        auto row = center + rowDelta * distance;
        auto col = center + colDelta * distance;
        Position destoryPosition(row, col);
        positions.push_back(destoryPosition);
    }

    return positions;
}

void useMagic(Context context, Magic magic)
{
    std::vector<Position> positionsToDestory = getPositionsToDestory(context, magic);

    for (const auto &position : positionsToDestory)
    {
        context.grid.setStone(position.row, position.col, 0);
    }
}

int main()
{
    // 격자 등 문제를 풀기 위한 정보를 가져온다.
    auto context = getContextFromInput();
    std::map<int, int> accumulatedDestoriedStones{
        {1, 0},
        {2, 0},
        {3, 0},
    };

    // M번 동안 다음을 시도한다.
    for (const auto &magic : context.magics)
    {
        //   1. 블리자드 쏜다.
        useMagic(context, magic);

        //   2. 구슬들을 앞으로 땡긴다.
        moveStonesForward(context);

        while (true)
        {
            //   3. 4연속 구슬들 터트린다.
            auto destoriedStones = destory4ContiguousStones(context);

            //   3.1 터트린 구슬을 저장한다.
            addDestoriedStones(accumulatedDestoriedStones, destoriedStones);

            //   4. 만약 4연속 구슬 터진게 하나도 없으면 6으로 이동.
            auto isNoStonesDestroid;
            if (isNoStonesDestroid)
            {
                break;
            }

            //   5. 구슬들을 앞으로 땡긴다. 3번으로 간다.
            moveStonesForward(context);
        }

        //   6. 구슬들을 그룹으로 만든다.
        auto groups = makeGroups(context);
        // 그룹을 다시 구슬로 바꿔 격자를 채운다.
        auto stones = convertGroupsToStones(groups);
        clearStones(context);
        fillStones(context, stones);
    }

    auto firstStoneCount;
    auto secondStoneCount;
    auto thridStoneCount;

    // 터트린 구슬들을 가지고
    // 1 * 1번구슬갯수 + 2 * 2번구슬갯수 + 3 * 3번구슬갯수 값을 출력한다.
    std::cout << firstStoneCount * 1 + secondStoneCount * 2 + thridStoneCount * 3 << std::endl;

    return 0;
}
