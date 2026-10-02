class Solution {
    public int eraseOverlapIntervals(int[][] intervals) {
        int n = intervals.length;
        Arrays.sort(intervals, new Comparator<int[]>() {
            public int compare(int[] val1, int[] val2) {
                return val1[1] - val2[1];
            }
        });
        int cnt = 1;
        int lastendtime = intervals[0][1];
        for (int i = 1; i < n; i++) {
            if (intervals[i][0] >= lastendtime) {
                cnt++;
                lastendtime = intervals[i][1];
            }
        }
        return n - cnt;
    }
}