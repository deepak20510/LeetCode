class Solution {
    public int lengthOfLongestSubstring(String s) {
        int[] hash = new int[256];
        Arrays.fill(hash, -1);
        int n = s.length();
        int left = 0;
        int right = 0;
        int max_length = 0;
        while (right < n) {
            char c = s.charAt(right);
            if (hash[c] != -1) {
                if (hash[c] >= left) {
                    left = hash[c] + 1;
                }
            }
            int length = right - left + 1;
            max_length = Math.max(length, max_length);
            hash[c] = right;
            right++;
        }
        return max_length;
    }
}