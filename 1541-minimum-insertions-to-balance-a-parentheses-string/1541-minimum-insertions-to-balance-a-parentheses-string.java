class Solution {
    public int minInsertions(String s) {
        int res = 0, need = 0;
        for (char c : s.toCharArray()) {
            if (c == '(') {
                need += 2;
                if (need % 2 == 1) {
                    res++;
                    need--;
                }
            } else {
                need--;
                if (need < 0) {
                    res++;
                    need = 1;
                }
            }
        }
        return res + need;
    }
}