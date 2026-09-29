class Solution {
    public int numberOfSubstrings(String s) {
        int n = s.length();
        int[] hash = new int[3];
        int l = 0;
        int cnt = 0;
        for (int r = 0; r < n; r++) {
            hash[s.charAt(r) - 'a']++;
            while (hash[0] > 0 && hash[1] > 0 && hash[2] > 0) {
                cnt += n - r;
                hash[s.charAt(l) - 'a']--;
                l++;
            }
        }
        return cnt;
    }
}