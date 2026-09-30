class Solution {
    public int numSubarraysWithSum(int[] nums, int goal) {
        return atMost(nums, goal) - atMost(nums, goal - 1);
    }

    public int atMost(int[] nums, int goal) {
        if (goal < 0)
            return 0;
        int n = nums.length;
        int l = 0;
        int r = 0;
        int sum = 0;
        int cnt = 0;
        while (r < n) {
            sum += nums[r];
            while (sum > goal) {
                sum = sum - nums[l];
                l = l + 1;
            }
            cnt = cnt + (r - l + 1);
            r = r + 1;
        }
        return cnt;
    }
}