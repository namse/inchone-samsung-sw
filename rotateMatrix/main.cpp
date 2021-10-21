#include <iostream>
#include <vector>

struct Rotation
{
    int centerCol;
    int centerRow;
    int squareRadius;
};

using RotationSequence = std::vector<Rotation>;

// 모든 회전 연산 순서를 만들어내는 함수
std::vector<RotationSequence> makeAllRotationSequences(std::vector<Rotation> rotations)
{
    if (rotations.size() == 1)
    {
        RotationSequence sequence;
        sequence.push_back(rotations[0]);
        return {sequence};
    }

    std::vector<RotationSequence> result;

    for (int i = 0; i < rotations.size(); i++)
    {
        auto subRotations = rotations;
        auto rotation = rotations[i];
        subRotations.erase(subRotations.begin() + i);

        auto subRotationSequences = makeAllRotationSequences(subRotations);
        for (auto subRotationSequence : subRotationSequences)
        {
            subRotationSequence.insert(subRotationSequence.begin(), rotation);
            result.push_back(subRotationSequence);
        }
    }

    return result;
}

// 회전 연산 순서를 행렬에 적용하여 새 행렬을 내보내는 함수
class Matrix
{
public:
    Matrix(int rows, int cols)
        : _rows(rows),
          _cols(cols),
          _data(std::vector<std::vector<int>>(rows, std::vector<int>(cols)))
    {
    }

    void setValue(int row, int col, int value)
    {
        _data[row - 1][col - 1] = value;
    }
    int getValue(int row, int col)
    {
        return _data[row - 1][col - 1];
    }
    int rows()
    {
        return _rows;
    }
    int cols()
    {
        return _cols;
    }
    void print()
    {
        std::cout << "-----" << std::endl;
        for (int i = 0; i < _rows; i++)
        {
            for (int j = 0; j < _cols; j++)
            {
                std::cout << _data[i][j] << " ";
            }
            std::cout << std::endl;
        }
        std::cout << "-----" << std::endl;
    }

private:
    int _rows;
    int _cols;
    std::vector<std::vector<int>> _data;
};

Matrix rotate(Matrix matrix, Rotation rotation);

Matrix rotate(Matrix matrix, RotationSequence rotationSequence)
{
    auto rotatedMatrix = matrix;
    for (auto rotation : rotationSequence)
    {
        rotatedMatrix = rotate(rotatedMatrix, rotation);
    }
    return rotatedMatrix;
}

// 한 회전 연산을 행렬에 적용하여 새 행렬을 내보내는 함수
Matrix rotate(Matrix matrix, int centerCol, int centerRow, int distance);

Matrix rotate(Matrix matrix, Rotation rotation)
{
    auto rotatedMatrix = matrix;
    int centerCol = rotation.centerCol;
    int centerRow = rotation.centerRow;
    int squareRadius = rotation.squareRadius;

    for (int distance = 1; distance <= squareRadius; distance++)
    {
        rotatedMatrix = rotate(rotatedMatrix, centerCol, centerRow, distance);
    }

    return rotatedMatrix;
}

struct Position
{
    int col;
    int row;
};

std::vector<Position> getRotationTargetPositions(int centerCol, int centerRow, int distance);

Matrix rotate(Matrix matrix, int centerCol, int centerRow, int distance)
{
    auto rotatedMatrix = matrix;
    std::vector<Position> rotationTargetPositions = getRotationTargetPositions(centerCol, centerRow, distance);

    for (auto it = rotationTargetPositions.begin(); it != rotationTargetPositions.end(); it++)
    {
        auto previousPosition = it == rotationTargetPositions.begin()
                                    ? rotationTargetPositions.back()
                                    : *(it - 1);

        auto previousPositionValue = matrix.getValue(previousPosition.row, previousPosition.col);

        auto currentPosition = *it;
        rotatedMatrix.setValue(currentPosition.row, currentPosition.col, previousPositionValue);
    }

    return rotatedMatrix;
}

std::vector<Position> getRotationTargetPositions(int centerCol, int centerRow, int distance)
{
    std::vector<Position> result;

    auto vertexAndDirections = {
        std::make_pair(Position{
                           .col = centerCol - distance,
                           .row = centerRow - distance,
                       },
                       Position{
                           .col = 1,
                           .row = 0,
                       }),
        std::make_pair(Position{
                           .col = centerCol + distance,
                           .row = centerRow - distance,
                       },
                       Position{
                           .col = 0,
                           .row = 1,
                       }),
        std::make_pair(Position{
                           .col = centerCol + distance,
                           .row = centerRow + distance,
                       },
                       Position{
                           .col = -1,
                           .row = 0,
                       }),
        std::make_pair(Position{
                           .col = centerCol - distance,
                           .row = centerRow + distance,
                       },
                       Position{
                           .col = 0,
                           .row = -1,
                       })};
    for (auto &vertexAndDirection : vertexAndDirections)
    {
        auto vertex = vertexAndDirection.first;
        auto direction = vertexAndDirection.second;
        for (int i = 0; i < distance * 2; i += 1)
        {
            result.push_back(Position{
                .col = vertex.col + i * direction.col,
                .row = vertex.row + i * direction.row,
            });
        }
    }

    return result;
}

// 입력 받아 문제 풀이에 필요한 데이터 만들기
struct Context
{
    Matrix matrix;
    RotationSequence rotationSequence;
};

Context makeContextFromInput()
{
    int matrixRows, matrixCols, rotationSequenceSize;
    std::cin >> matrixRows >> matrixCols >> rotationSequenceSize;

    auto matrix = Matrix(matrixRows, matrixCols);

    for (int row = 1; row <= matrixRows; row += 1)
    {
        for (int col = 1; col <= matrixCols; col += 1)
        {
            int value;
            std::cin >> value;
            matrix.setValue(row, col, value);
        }
    }

    RotationSequence rotationSequence;

    for (int i = 0; i < rotationSequenceSize; i += 1)
    {
        int centerCol, centerRow, squareRadius;
        std::cin >> centerRow >> centerCol >> squareRadius;

        rotationSequence.push_back({.centerCol = centerCol,
                                    .centerRow = centerRow,
                                    .squareRadius = squareRadius});
    }

    return Context{
        .matrix = matrix,
        .rotationSequence = rotationSequence};
}

const int MIN_MATRIX_VALUE = 100 * 50;

int getMatrixValue(Matrix matrix)
{
    int minRowSum = MIN_MATRIX_VALUE;
    for (auto row = 1; row <= matrix.rows(); row += 1)
    {
        int sum = 0;
        for (auto col = 1; col <= matrix.cols(); col += 1)
        {
            sum += matrix.getValue(row, col);
        }
        if (sum < minRowSum)
        {
            minRowSum = sum;
        }
    }
    return minRowSum;
}

int main()
{
    auto context = makeContextFromInput();

    // 모든 회전 연산 순서의 경우의 수를 만들어내기
    auto allRotationSequences = makeAllRotationSequences(context.rotationSequence);

    int minMatrixValue = MIN_MATRIX_VALUE;

    // 모든 회전 연산 순서의 경우의 수에 대해
    for (auto &rotationSequence : allRotationSequences)
    {
        // 각 회전 연산 순서를 적용한 행렬의 값을 구하기
        auto rotatedMatrix = rotate(context.matrix, rotationSequence);

        // 그 중 최소 값을 저장하기
        auto matrixValue = getMatrixValue(rotatedMatrix);
        if (matrixValue < minMatrixValue)
        {
            minMatrixValue = matrixValue;
        }
    }

    std::cout << minMatrixValue << std::endl;
    return 0;
}
