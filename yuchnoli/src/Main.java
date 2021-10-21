import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Scanner;

public class Main {
    private static final int horseCount = 4;

    public static void main(String[] args) throws Exception {
        var startTime = System.nanoTime();

        var board = CreateBoard();

        // 주사위 수 리스트를 가져온다.
        var diceList = getDiceList();

        var allDiceAndHorseCases = generateAllDiceAndHorsesCases(diceList);

        var maxPoint = 0;

        for (var diceAndHorses : allDiceAndHorseCases) {
            var point = calculateYuchnoliPlayPoint(board, diceAndHorses);
            if (point > maxPoint) {
                maxPoint = point;
            }
        }
        System.out.println(maxPoint);
        var endTime = System.nanoTime();
        System.out.println("TIME : " + (endTime - startTime) / 1000000.0 + "(ms)");
    }

    // 주사위 수 리스트에 각 주사위 수마다 몇번째 말을 이동시킬 것인지 할당한 것을 모든 경우의 수에 대해 만들어내는 함수
    public static List<List<DiceAndHorse>> generateAllDiceAndHorsesCases(List<Integer> diceList) {
        var diceAndHorsesCases = new ArrayList<List<DiceAndHorse>>();

        // 첫 dice에 모든 horse를 붙여서 리스트에 넣는다.
        // 리스트를 horse개만큼 복사하고, 각각의 리스트에 각 diceAndHorse를 넣고, 그걸로 리스트를 만든다.

        for (var dice : diceList) {
            var nextDiceAndHorsesCases = new ArrayList<List<DiceAndHorse>>();

            for (var horse = 0; horse < horseCount; horse++) {
                var diceAndHorse = new DiceAndHorse(dice, horse);

                if (diceAndHorsesCases.size() == 0) {
                    nextDiceAndHorsesCases.add(new ArrayList<DiceAndHorse>() {
                        {
                            add(diceAndHorse);
                        }
                    });
                } else {
                    for (var diceAndHorsesCase : diceAndHorsesCases) {
                        var nextDiceAndHorsesCase = new ArrayList<DiceAndHorse>();
                        nextDiceAndHorsesCase.addAll(diceAndHorsesCase);
                        nextDiceAndHorsesCase.add(diceAndHorse);
                        nextDiceAndHorsesCases.add(nextDiceAndHorsesCase);
                    }
                }
            }

            diceAndHorsesCases = nextDiceAndHorsesCases;
        }

        return diceAndHorsesCases;
    }

    // 주사위 수와 할당된 말 리스트를 가지고 말을 이동시키면서 점수를 알아내는 함수
    public static int calculateYuchnoliPlayPoint(Board board, List<DiceAndHorse> diceAndHorses) {
        var points = 0;

        var horseBaseIds = new ArrayList<Integer>();
        for (var horse = 0; horse < horseCount; horse += 1) {
            horseBaseIds.add(board.startBaseId);
        }

        for (var diceAndHorse : diceAndHorses) {
            var dice = diceAndHorse.dice;
            var horse = diceAndHorse.horse;

            var startBaseId = horseBaseIds.get(horse);
            if (startBaseId == board.endBaseId) {
                return -1;
            }

            for (var movingIndex = 0; movingIndex < dice; movingIndex += 1) {
                var nextBaseId = getNextBaseId(board, horseBaseIds.get(horse), movingIndex);

                horseBaseIds.set(horse, nextBaseId);
                if (nextBaseId == board.endBaseId) {
                    break;
                }
            }

            var destinationBaseId = horseBaseIds.get(horse);
            var horseCountOnDestinationBase = 0;
            for (var horseBaseId : horseBaseIds) {
                if (horseBaseId == destinationBaseId) {
                    horseCountOnDestinationBase += 1;
                }
            }
            if (destinationBaseId != board.endBaseId && horseCountOnDestinationBase > 1) {
                return -1;
            }

            var point = board.getPoint(horseBaseIds.get(horse));
            points += point;
        }

        return points;
    }

    private static int getNextBaseId(Board board, Integer currentBaseId, int movingIndex) {
        var base = board.getBase(currentBaseId);
        var nextBaseId = movingIndex == 0 && base.blueArrowBaseId != null ? base.blueArrowBaseId : base.redArrowBaseId;
        return nextBaseId;
    }

    public static List<Integer> getDiceList() {
        var diceList = new ArrayList<Integer>();

        try (var scanner = new Scanner(System.in)) {
            for (var i = 0; i < 10; i += 1) {
                var dice = scanner.nextInt();
                diceList.add(dice);
            }
        }
        return diceList;
    }

    public static Board CreateBoard() {
        var base0 = new Base(0, null, null);

        var base1 = new Base(40, 0, null);
        var base2 = new Base(35, 1, null);
        var base3 = new Base(30, 2, null);
        var base4 = new Base(25, 3, null);

        var base5 = new Base(38, 1, null);
        var base6 = new Base(36, 5, null);
        var base7 = new Base(34, 6, null);
        var base8 = new Base(32, 7, null);
        var base9 = new Base(30, 8, 15);

        var base10 = new Base(28, 9, null);
        var base11 = new Base(26, 10, null);
        var base12 = new Base(24, 11, null);
        var base13 = new Base(22, 12, null);
        var base14 = new Base(20, 13, 31);

        var base15 = new Base(28, 16, null);
        var base16 = new Base(27, 17, null);
        var base17 = new Base(26, 4, null);
        var base18 = new Base(19, 4, null);
        var base19 = new Base(16, 18, null);

        var base20 = new Base(13, 19, null);
        var base21 = new Base(18, 14, null);
        var base22 = new Base(16, 21, null);
        var base23 = new Base(14, 22, null);
        var base24 = new Base(12, 23, null);

        var base25 = new Base(10, 24, 20);
        var base26 = new Base(8, 25, null);
        var base27 = new Base(6, 26, null);
        var base28 = new Base(4, 27, null);
        var base29 = new Base(2, 28, null);

        var base30 = new Base(24, 4, null);
        var base31 = new Base(22, 30, null);
        var base32 = new Base(0, 29, null);

        var bases = new HashMap<Integer, Base>();
        bases.put(0, base0);
        bases.put(1, base1);
        bases.put(2, base2);
        bases.put(3, base3);
        bases.put(4, base4);
        bases.put(5, base5);
        bases.put(6, base6);
        bases.put(7, base7);
        bases.put(8, base8);
        bases.put(9, base9);
        bases.put(10, base10);
        bases.put(11, base11);
        bases.put(12, base12);
        bases.put(13, base13);
        bases.put(14, base14);
        bases.put(15, base15);
        bases.put(16, base16);
        bases.put(17, base17);
        bases.put(18, base18);
        bases.put(19, base19);
        bases.put(20, base20);
        bases.put(21, base21);
        bases.put(22, base22);
        bases.put(23, base23);
        bases.put(24, base24);
        bases.put(25, base25);
        bases.put(26, base26);
        bases.put(27, base27);
        bases.put(28, base28);
        bases.put(29, base29);
        bases.put(30, base30);
        bases.put(31, base31);
        bases.put(32, base32);

        return new Board(bases, 32, 0);
    }

}