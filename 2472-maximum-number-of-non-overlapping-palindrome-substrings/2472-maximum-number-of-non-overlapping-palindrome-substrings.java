class Solution {
    public int maxPalindromes(String s, int k) {
        int n = s.length();
        boolean[][] pal = new boolean[n][n];
        for (int i = n - 1; i >= 0; i--) {
            for (int j = i; j < n; j++) {
                if (s.charAt(i) == s.charAt(j)) {
                    if (j - i <= 2 || pal[i + 1][j - 1]) {
                        pal[i][j] = true;
                    }
                }
            }
        }
        int[] dp = new int[n + 1];
        for (int i = n - 1; i >= 0; i--) {
            dp[i] = dp[i + 1];
            if (i + k - 1 < n && pal[i][i + k - 1]) {
                dp[i] = Math.max(dp[i], 1 + dp[i + k]);
            }
            if (i + k < n && pal[i][i + k]) {
                dp[i] = Math.max(dp[i], 1 + dp[i + k + 1]);
            }
        }
        return dp[0];
    }
}