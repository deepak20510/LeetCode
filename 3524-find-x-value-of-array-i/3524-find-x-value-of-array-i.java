import java.util.*;
class Solution {
    public long[] resultArray(int[] nums, int k) {
        int n = nums.length;
        long[] ans = new long[k];
        long[] prev = new long[k];
        for (int num : nums) {
            long[] curr = new long[k];
            int rem = num % k;
            curr[rem]++;
            for (int r = 0; r < k; r++) {
                if (prev[r] > 0) {
                    int newRem = (int)((long) r * rem % k);
                    curr[newRem] += prev[r];
                }
            }
            prev = curr;
            for (int r = 0; r < k; r++) {
                ans[r] += curr[r];
            }
        }
        return ans;
    }
}