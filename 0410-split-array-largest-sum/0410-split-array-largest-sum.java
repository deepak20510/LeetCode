class Solution {
    int fnc(int[] nums, int pages){
        int student = 1;
        int pagesstudent = 0;
        for(int i = 0; i < nums.length; i++){
            if(pagesstudent + nums[i] <= pages){
                pagesstudent += nums[i];
            }else{
                student++;
                pagesstudent = nums[i];
            }
        }
        return student;
    }
    public int splitArray(int[] nums, int k) {
        int max = 0;
        for(int i = 0; i < nums.length; i++){
            max = Math.max(nums[i], max);
        }
        int low = max;
        int sum = 0;
        for(int i = 0; i < nums.length; i++){
            sum += nums[i];
        }
        int high = sum;
        while(low <= high){
            int mid = (low + high)/2;
            int nostudent = fnc(nums,mid);
            if(nostudent > k)   low = mid + 1;
            else    high = mid - 1;
        }
        return low;
    }
}