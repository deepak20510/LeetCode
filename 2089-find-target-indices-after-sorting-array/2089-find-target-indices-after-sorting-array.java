class Solution {
    public List<Integer> targetIndices(int[] nums, int target) {
        int n = nums.length;
        Arrays.sort(nums);
        int low = 0;
        int high = n - 1;
        int ans = n;
        while (low <= high) {
            int mid = (high + low) / 2;
            if (nums[mid] >= target) {
                ans = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        List<Integer> result = new ArrayList<>();
        while (ans < n && nums[ans] == target) {
            result.add(ans);
            ans++;
        }
        return result;
    }
}