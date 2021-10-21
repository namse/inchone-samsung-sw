import fs from "fs";

const inputString = fs.readFileSync("input.txt");
const lines = inputString.toString().split("\n");

function input(): string {
  return lines.shift()!;
}

type Board = {
  readonly n: number;
  readonly data: number[][];
  readonly center: number;
};

enum MagicDirection {
  Up = 1,
  Down = 2,
  Left = 3,
  Right = 4,
}

type Magic = {
  direction: MagicDirection;
  distance: number;
};

// 함수 : 데이터 입력받아 구슬판 만들기
function processInput(): {
  board: Board;
  magics: Magic[];
} {
  const [n, m] = input()
    .split(" ")
    .map((x) => parseInt(x));

  const boardData: number[][] = [];
  for (let row = 0; row < n; row++) {
    const columns = input()
      .split(" ")
      .map((x) => parseInt(x));
    boardData.push(columns);
  }

  const board: Board = {
    n,
    data: boardData,
    center: Math.floor(n / 2),
  };

  const magics: Magic[] = [];
  for (let i = 0; i < m; i++) {
    const [direction, distance] = input()
      .split(" ")
      .map((x) => parseInt(x));
    magics.push({ direction, distance });
  }

  return { board, magics };
}

// 함수 - 중앙으로부터 di 방향으로 si 이하인 모든 칸에 얼음 파편 던지기
function useMagic(board: Board, magic: Magic): void {
  const destroyingTargets: { x: number; y: number }[] = getDestroyingTargets(
    board,
    magic
  );

  for (const { x, y } of destroyingTargets) {
    board.data[y][x] = 0;
  }
}

function getDestroyingTargets(
  board: Board,
  magic: Magic
): { x: number; y: number }[] {
  const targets: { x: number; y: number }[] = [];
  const { center } = board;
  for (let i = 1; i <= magic.distance; i++) {
    let deltaXy: { x: number; y: number };
    switch (magic.direction) {
      case MagicDirection.Up:
        deltaXy = { x: 0, y: -i };
        break;
      case MagicDirection.Down:
        deltaXy = { x: 0, y: i };
        break;
      case MagicDirection.Left:
        deltaXy = { x: -i, y: 0 };
        break;
      case MagicDirection.Right:
        deltaXy = { x: i, y: 0 };
        break;
    }
    const target = {
      x: center + deltaXy.x,
      y: center + deltaXy.y,
    };
    targets.push(target);
  }
  return targets;
}

// 함수 - 빈칸 없이 앞으로 꽉꽉 채우기
type Position = { x: number; y: number };
function pushForward(board: Board): void {
  let position = getNextPosition(board, { x: board.center, y: board.center });
  while (position) {
    const isZero = board.data[position.y][position.x] === 0;
    if (isZero) {
      const nextNotZeroPosition = getNextNotZeroPosition(board, position);
      if (nextNotZeroPosition) {
        board.data[position.y][position.x] =
          board.data[nextNotZeroPosition.y][nextNotZeroPosition.x];
        board.data[nextNotZeroPosition.y][nextNotZeroPosition.x] = 0;
      }
    }
    position = getNextPosition(board, position);
  }
}

function getNextPosition(
  board: Board,
  position: Position
): Position | undefined {
  const { x, y } = position;
  const { center } = board;

  if (x === 0 && y === 0) {
    return undefined;
  }
  if (center < y && 2 * center - y <= x && x <= y - 1) {
    return {
      x: x + 1,
      y,
    };
  }
  if (x < center && x + 1 <= y && y <= 2 * center - x - 1) {
    return {
      x,
      y: y + 1,
    };
  }
  if (y <= center && y <= x && x <= 2 * center - y) {
    return {
      x: x - 1,
      y,
    };
  }
  return {
    x,
    y: y - 1,
  };
}

function getNextNotZeroPosition(
  board: Board,
  position: Position
): Position | undefined {
  let nextPosition = getNextPosition(board, position);
  while (true) {
    if (!nextPosition) {
      return undefined;
    }
    if (board.data[nextPosition.y][nextPosition.x] !== 0) {
      return nextPosition;
    }
    nextPosition = getNextPosition(board, nextPosition);
  }
}

// 함수 - 4개 연속 구슬 폭발하기
function tryExplode4ContinuousBead(board: Board, context: Context): boolean {
  let isExploded = false;

  let position = getNextPosition(board, { x: board.center, y: board.center });
  while (position) {
    const bead = board.data[position.y][position.x];
    if (!bead) {
      position = getNextPosition(board, position);
      continue;
    }

    const sameContiguousBeadCount = getSameContiguousBeadCount(board, position);
    if (sameContiguousBeadCount < 4) {
      position = getNextPosition(board, position);
      continue;
    }

    isExploded = true;
    for (let i = 0; i < sameContiguousBeadCount; i++) {
      context.explodedBeads[bead] += 1;
      console.log(
        `magic on ${position.x}, ${position.y}. bead is ${bead}, by explosion`
      );
      board.data[position.y][position.x] = 0;
      position = getNextPosition(board, position)!;
    }
  }

  return isExploded;
}
function getSameContiguousBeadCount(board: Board, position: Position): number {
  const bead = board.data[position.y][position.x];
  let count = 1;

  let nextPosition = getNextPosition(board, position);
  while (nextPosition) {
    const nextPositionBead = board.data[nextPosition.y][nextPosition.x];
    if (nextPositionBead !== bead) {
      break;
    }
    count += 1;

    nextPosition = getNextPosition(board, nextPosition);
  }

  return count;
}

// 함수 - 그룹 변환하기
type Group = {
  bead: number;
  count: number;
};
function convertGroup(board: Board): void {
  const groups = getGroups(board);

  clearBoard(board);

  const queue: number[] = groups.reduce((prev, current) => {
    return [...prev, current.count, current.bead];
  }, [] as number[]);

  fillData(board, queue);
}

function getGroups(board: Board): Group[] {
  const groups: Group[] = [];
  let position = getNextPosition(board, { x: board.center, y: board.center });
  while (position) {
    const bead = board.data[position.y][position.x];
    if (!bead) {
      position = getNextPosition(board, position);
      continue;
    }

    const sameContiguousBeadCount = getSameContiguousBeadCount(board, position);
    groups.push({
      bead,
      count: sameContiguousBeadCount,
    });
    position = jumpPosition(board, position, sameContiguousBeadCount);
  }
  return groups;
}

function jumpPosition(
  board: Board,
  position: Position,
  jumpCount: number
): Position | undefined {
  let nextPosition: Position | undefined = position;
  for (let i = 0; i < jumpCount; i++) {
    nextPosition = getNextPosition(board, nextPosition);
    if (!nextPosition) {
      return undefined;
    }
  }
  return nextPosition;
}

function clearBoard(board: Board): void {
  board.data.forEach((row) => {
    row.fill(0);
  });
}

function fillData(board: Board, data: number[]): void {
  let index = 0;
  let position = getNextPosition(board, { x: board.center, y: board.center });
  while (position) {
    const bead = data[index] ?? 0;
    board.data[position.y][position.x] = bead;
    index += 1;
    position = getNextPosition(board, position);
  }
}

type Context = {
  explodedBeads: number[];
};
function main(): void {
  const context: Context = {
    explodedBeads: [0, 0, 0, 0],
  };
  const { board, magics } = processInput();
  for (const magic of magics) {
    useMagic(board, magic);
    pushForward(board);

    while (tryExplode4ContinuousBead(board, context)) {
      pushForward(board);
    }

    convertGroup(board);

    console.log("---after blizzard---");
    board.data.forEach((x) => console.log(JSON.stringify(x)));
    console.log("----------------");
  }
  const answer = [1, 2, 3]
    .map((i) => context.explodedBeads[i] * i)
    .reduce((prev, current) => prev + current);
  console.log(answer);
}

main();
