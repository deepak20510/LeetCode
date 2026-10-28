class Solution {
    boolean possible(int[] bloomDay, int m, int k, int day){
        int cnt = 0;
        int noOfB = 0;
        for(int i = 0; i < bloomDay.length;i++){
            if(bloomDay[i] <= day){
                cnt++;
            }else{
                noOfB += (cnt/k);
                cnt =  0;
            }
        }
        noOfB += (cnt/k);
        return noOfB >= m;
    }
    public int minDays(int[] bloomDay, int m, int k) {
        int n = bloomDay.length;
        int max = Integer.MIN_VALUE;
        int min = Integer.MAX_VALUE;
        if ((long) n < (long) m * k) return -1;
        for(int i = 0; i < n; i++){
            max = Math.max(bloomDay[i],max);
        }
        for(int i = 0; i < n; i++){
            min = Math.min(bloomDay[i],min);
        }
        int low = min;
        int high = max;
        while(low <= high){
            int mid = (low + high)/2;
            if(possible(bloomDay, m,  k, mid)){
                high = mid - 1;
            }else{
                low = mid + 1;
            }
        }
        return low;
    }
}