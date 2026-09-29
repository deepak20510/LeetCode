class Solution {
    public boolean hasValidPath(char[][] A) {
        int m = A.length, n = A[0].length;
        if (((m + n) & 1) == 0 || (A[0][0] == ')'))
            return false;
        Set<Integer>[][] dp = new HashSet[m + 1][n + 1];
        for (int i = 0; i <= m; i++)
            Arrays.setAll(dp[i], _ -> new HashSet<>());
        dp[0][0].add(0);
        for (int i = 0; i < m; i++)
            for (int j = 0; j < n; j++) {
                int v = 1 - ((A[i][j] & 1) << 1);
                for (int d : dp[i][j]) {
                    int nk = d + v;
                    if (nk > -1) {
                        dp[i + 1][j].add(nk);
                        dp[i][j + 1].add(nk);
                    }
                }
            }
        return dp[m][n - 1].contains(0);
    }
}