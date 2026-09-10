
class Solution {

    public int recurr(int index, int[] coins, int amount, int[][] dp) {

        if (index == 0) {

            if (amount % coins[index] == 0) {
                return amount / coins[index];
            } else {
                return (int) 1e9;
            }
        }

        if (dp[index][amount] != -1) {
            return dp[index][amount];
        }

        int nottake = recurr(index - 1, coins, amount, dp);

        int take = (int) 1e9;

        if (coins[index] <= amount) {
            take = 1 + recurr(index, coins, amount - coins[index], dp);
        }

        return dp[index][amount] = Math.min(take, nottake);
    }

    public int coinChange(int[] coins, int amount) {

        int n = coins.length;

        int[][] dp = new int[n][amount + 1];

        for (int i = 0; i < n; i++) {
            Arrays.fill(dp[i], -1);
        }

        int ans = recurr(n - 1, coins, amount, dp);

        if (ans >= 1e9) {
            return -1;
        }

        return ans;
    }
}
