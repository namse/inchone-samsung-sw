type Board = {};
type Magic = {
  direction: number;
  distance: number;
};
// 함수 : 데이터 입력받아 구슬판 만들기

function processInput(): {
  board: Board;
  magics: Magic[];
} {}

// 함수 - 중앙으로부터 di 방향으로 si 이하인 모든 칸에 얼음 파편 던지기
function useMagic(board: Board, magic: Magic): void {}

// 함수 - 빈칸 없이 앞으로 꽉꽉 채우기
function pushForward(board: Board): void {}

// 함수 - 4개 연속 구슬 폭발하기
function tryExplode4ContinuousBead(board: Board): boolean {}

// 함수 - 그룹 변환하기
function convertGroup(board: Board): void {}

function main(): void {
  const { board, magics } = processInput();
  for (const magic of magics) {
    useMagic(board, magic);
    pushForward(board);

    while (tryExplode4ContinuousBead(board)) {
      pushForward(board);
    }

    convertGroup(board);
  }
}

main();
