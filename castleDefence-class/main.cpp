#include <iostream>
#include <vector>

// 캐슬 디펜스는 성을 향해 몰려오는 적을 잡는 턴 방식의 게임이다.

// 게임이 진행되는 곳은 크기가 N×M인 격자판으로 나타낼 수 있다.
// 격자판은 1×1 크기의 칸으로 나누어져 있다.
// 각 칸에 포함된 적의 수는 최대 하나이다.
// 격자판의 N번행의 바로 아래(N+1번 행)의 모든 칸에는 성이 있다.

// 성을 적에게서 지키기 위해 궁수 3명을 배치하려고 한다.
// 궁수는 성이 있는 칸에 배치할 수 있다.
// 하나의 칸에는 최대 1명의 궁수만 있을 수 있다.
// 각각의 턴마다 궁수는 적 하나를 공격할 수 있다.
// 모든 궁수는 동시에 공격한다.
// 같은 적이 여러 궁수에게 공격당할 수 있다.
// 공격받은 적은 게임에서 제외된다.
// 궁수의 공격이 끝나면 적이 아래로 한 칸 이동한다.
// 적이 성이 있는 칸으로 이동한 경우에는 게임에서 제외된다.
// 모든 적이 격자판에서 제외되면 게임이 끝난다.

// 게임 설명에서 보다시피 궁수를 배치한 이후의 게임 진행은 정해져있다.
// 격자판의 상태가 주어졌을 때 궁수의 공격으로 제거할 수 있는 적의 최대 수를 계산해보자.

// 격자판의 두 위치 (r1, c1), (r2, c2)의 거리는 |r1-r2| + |c1-c2|이다.

class Grid
{
public:
    Grid(int rows, int cols) : _rows(rows),
                               _cols(cols),
                               _enemyExistsMatrix(
                                   std::vector<std::vector<int>>(rows,
                                                                 std::vector<int>(cols)))
    {
    }

    void setEnemyExists(int row, int col)
    {
        _enemyExistsMatrix[row][col] = 1;
    }

    bool killEnemy(int row, int col)
    {
        auto isEnemyExists = _enemyExistsMatrix.at(row).at(col) == 1;
        _enemyExistsMatrix[row][col] = false;
        return isEnemyExists;
    }
    bool isEnemyExists(int row, int col)
    {
        return _enemyExistsMatrix[row][col] == 1;
    }
    int cols()
    {
        return _cols;
    }
    int rows()
    {
        return _rows;
    }
    void moveEnemiesDown()
    {
        _enemyExistsMatrix.erase(_enemyExistsMatrix.end());
        _enemyExistsMatrix.insert(_enemyExistsMatrix.begin(),
                                  std::vector<int>(_cols));
    }

private:
    int _rows;
    int _cols;

    std::vector<std::vector<int>> _enemyExistsMatrix;
};

struct InputResult
{
    Grid grid;
    int archorRangeLimit;
};

InputResult processInput()
{
    int rows, cols, archorRangeLimit;
    std::cin >> rows >> cols >> archorRangeLimit;

    Grid grid(rows, cols);

    for (int row = 0; row < rows; row++)
    {
        for (int col = 0; col < cols; col++)
        {
            int isEnemyExists;
            std::cin >> isEnemyExists;

            if (isEnemyExists == 1)
            {
                grid.setEnemyExists(row, col);
            }
        }
    }

    return InputResult{
        .grid = grid,
        .archorRangeLimit = archorRangeLimit};
}

std::vector<std::vector<int>> getAllArchorPositionsCases(Grid &grid)
{
    std::vector<std::vector<int>> result;

    for (
        auto firstArchorPosition = 0;
        firstArchorPosition < grid.cols();
        firstArchorPosition += 1)
    {
        for (
            auto secondArchorPosition = firstArchorPosition + 1;
            secondArchorPosition < grid.cols();
            secondArchorPosition += 1)
        {
            for (
                auto thirdArchorPosition = secondArchorPosition + 1;
                thirdArchorPosition < grid.cols();
                thirdArchorPosition += 1)
            {
                std::vector<int> archorPositions = {
                    firstArchorPosition,
                    secondArchorPosition,
                    thirdArchorPosition,
                };
                result.push_back(archorPositions);
            }
        }
    }

    return result;
}

struct Position
{
    int row;
    int col;
};

struct GetAttackPositionResult
{
    Position attackPosition;
    bool isAttackPositionValid;
};

GetAttackPositionResult getAttackPosition(Grid grid,
                                          int archorRangeLimit,
                                          int archorCol)
{
    // 궁수가 공격하는 적은 거리가 D이하인 적 중에서 가장 가까운 적이다.
    // 궁수가 공격할 적이 여럿일 경우에는 가장 왼쪽에 있는 적을 공격한다.

    int closestEnemyDistance = -1;
    Position closestEnemyPosition;

    for (
        auto row = 0;
        row < grid.rows();
        row += 1)
    {
        for (
            auto col = 0;
            col < grid.cols();
            col += 1)
        {
            if (!grid.isEnemyExists(row, col))
            {
                continue;
            }

            int archorRow = grid.rows();
            int distance = std::abs(row - archorRow) + std::abs(col - archorCol);

            if (distance <= archorRangeLimit && (closestEnemyDistance == -1 || distance < closestEnemyDistance || col < closestEnemyPosition.col))
            {
                closestEnemyDistance = distance;
                closestEnemyPosition = Position{row, col};
            }
        }
    }

    auto hasEnemyToAttack = closestEnemyDistance != -1;
    return hasEnemyToAttack
               ? GetAttackPositionResult{
                     .attackPosition = closestEnemyPosition,
                     .isAttackPositionValid = true}
               : GetAttackPositionResult{.isAttackPositionValid = false};
}

std::vector<Position> getAttackPositions(Grid grid,
                                         int archorRangeLimit,
                                         std::vector<int> archorPositions)
{

    std::vector<Position> result;

    for (auto archorPosition : archorPositions)
    {
        auto getAttackPositionResult = getAttackPosition(grid, archorRangeLimit, archorPosition);
        if (getAttackPositionResult.isAttackPositionValid)
        {
            result.push_back(getAttackPositionResult.attackPosition);
        }
    }

    return result;
}

int getKilledEnemyCount(
    Grid grid,
    int archorRangeLimit,
    std::vector<int> archorPositions)
{
    auto killedEnemyCount = 0;

    for (auto turn = 0; turn < grid.rows(); turn += 1)
    {
        auto attackPositions = getAttackPositions(grid,
                                                  archorRangeLimit, archorPositions);

        for (auto &attackPosition : attackPositions)
        {
            if (grid.killEnemy(attackPosition.row, attackPosition.col))
            {
                killedEnemyCount += 1;
            }
        }
        grid.moveEnemiesDown();
    }

    return killedEnemyCount;
}

std::vector<int> getAllKilledEnemyCounts(
    Grid grid,
    int archorRangeLimit,
    std::vector<std::vector<int>> archorPositionsCases)
{
    std::vector<int> killedEnemyCounts;

    for (auto archorPositionsCase : archorPositionsCases)
    {
        auto killedEnemyCount = getKilledEnemyCount(grid, archorRangeLimit, archorPositionsCase);
        killedEnemyCounts.push_back(killedEnemyCount);
    }

    return killedEnemyCounts;
}

int main()
{
    // 격자판과 궁수의 공격 거리 제한 등을 입력받아 준비한다.
    auto inputResult = processInput();

    // 궁수 배치의 모든 경우의 수를 구한다.
    auto allArchorPositionsCases = getAllArchorPositionsCases(inputResult.grid);

    // 각 궁수 배치마다 제거할 수 있는 적의 수를 구한다.
    auto allKilledEnemyCounts = getAllKilledEnemyCounts(
        inputResult.grid, inputResult.archorRangeLimit, allArchorPositionsCases);

    // 그 중 가장 큰 수를 구해 출력한다.
    int maxKilledEnemyCount = -1;
    for (auto &killedEnemyCount : allKilledEnemyCounts)
    {
        if (maxKilledEnemyCount < killedEnemyCount)
        {
            maxKilledEnemyCount = killedEnemyCount;
        }
    }
    std::cout << maxKilledEnemyCount;
}
