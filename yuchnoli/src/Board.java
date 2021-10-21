import java.util.Map;

public class Board {
    public final Map<Integer, Base> bases;
    public final int startBaseId;
    public final int endBaseId;

    public Board(Map<Integer, Base> bases, int startBaseId, int endBaseId) {
        this.bases = bases;
        this.startBaseId = startBaseId;
        this.endBaseId = endBaseId;
    }

    public int getPoint(Integer baseId) {
        return getBase(baseId).point;
    }

    public Base getBase(Integer baseId) {
        return bases.get(baseId);
    }
}