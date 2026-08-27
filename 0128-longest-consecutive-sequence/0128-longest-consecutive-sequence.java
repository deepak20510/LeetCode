class Solution {
    public int longestConsecutive(int[] nums) {
        int n = nums.length;
        if (n == 0) {
            return 0;
        }
        Arrays.sort(nums);
        int last_longest = Integer.MIN_VALUE;
        int longest = 1;
        int count = 0;
        for(int i = 0;i < n;i++){
            if(nums[i] - 1 == last_longest){
                count = count + 1;
                last_longest = nums[i];
            }else if(nums[i] != last_longest){
                count = 1;
                last_longest = nums[i];
            }
            longest = Math.max(longest,count);
        }
        return longest;
    }
}