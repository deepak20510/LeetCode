class Solution {
    public int maxProfit(int[] prices) {
        int minPrice = prices[0];
        int n = prices.length;
        int maxProfit = 0;
        for(int i = 0; i <= n-1;i++){
            maxProfit = Math.max(maxProfit,prices[i] - minPrice);
            minPrice = Math.min(minPrice, prices[i]);
        }
        return maxProfit;
    }
}