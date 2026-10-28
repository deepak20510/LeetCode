class Solution {

    public int minEatingSpeed(int[] piles, int h) {
        int max = Integer.MIN_VALUE;
        int n = piles.length;
        for(int i = 0; i < n; i++){
            max = Math.max(piles[i], max);
        }
        int low = 1;
        int high = max;
        int ans = max;
        while(low <= high){
            int mid = (low + high)/2;
            long sum = 0;
            for(int i = 0; i < n; i++){
                sum += ((long)piles[i] + mid - 1) / mid;
            }
            if(sum <= h){
                ans = mid;
                high = mid - 1;
            }else{
                low = mid + 1;
            }
        }
        return ans;
    }
}