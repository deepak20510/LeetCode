class Solution {
    public int lowerBound(int[] nums, int target) {
        int low = 0;
        int high = nums.length;
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] >= target) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }
        return low;
    }
    public int upperBound(int[] nums, int target) {
        int low = 0;
        int high = nums.length;
        while (low < high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] > target) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }
        return low;
    }
    public int[] searchRange(int[] nums, int target) {
        int lb = lowerBound(nums, target);
        if (lb == nums.length || nums[lb] != target) {
            return new int[]{-1, -1};
        }
        int ub = upperBound(nums, target);
        return new int[]{lb, ub - 1};
    }
}