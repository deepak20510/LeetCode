class Solution {
    public boolean isRectangleOverlap(int[] rec1, int[] rec2) {


        if (rec1[2] <= rec2[0]) return false; // left
        if (rec2[2] <= rec1[0]) return false; // right
        if (rec1[3] <= rec2[1]) return false; // below
        if (rec2[3] <= rec1[1]) return false; // above

        return true;

    }
}