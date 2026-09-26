class Solution {
    public int longestOnes(int[] nums, int k) {
        int n = nums.length;
        int len = 0;
        int maxlen = 0;
        for (int i = 0; i <= n - 1; i++) {
            int zeros = 0;
            for (int j = i; j <= n - 1; j++) {
                if (nums[j] == 0) {
                zeros++;
                }
                if (zeros <= k) {
                    len = j - i + 1;
                    maxlen = Math.max(maxlen, len);
                } else
                    break;
            }
        }
        return maxlen;
    }
}