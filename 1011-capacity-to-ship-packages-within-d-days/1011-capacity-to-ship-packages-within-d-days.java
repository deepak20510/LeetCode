class Solution {
    int fnc(int[] weights, int capacity){
        int day = 1;
        int load = 0;
        for(int i = 0; i < weights.length; i++){
            if(load + weights[i] > capacity){
                day = day + 1;
                load = weights[i];
            }else{
                load += weights[i];
            }
        }
        return day;
    }
    public int shipWithinDays(int[] weights, int days) {
        int max = 0;
        for(int i = 0; i < weights.length; i++){
            max = Math.max(weights[i], max);
        }
        int low = max;
        int sum = 0;
        for(int i = 0; i < weights.length; i++){
            sum += weights[i];
        }
        int high = sum;
        while(low <= high){
            int mid = (low + high)/2;
            int daysReq = fnc(weights,mid);
            if(daysReq <= days){    
                high = mid - 1;
            }else{
                low = mid + 1;
            }
        }
        return low;
    }
}