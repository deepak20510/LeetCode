class Solution {
    private void swapIfGreater(int[] nums1, int ind1, int[] nums2, int ind2){
        if(nums1[ind1] > nums2[ind2]){
            int temp = nums1[ind1];
            nums1[ind1] = nums2[ind2];
            nums2[ind2] = temp;
        }
    }
    public void merge(int[] nums1, int m, int[] nums2, int n) {
        int len = (n + m);
        int gap = (len / 2) + (len % 2);
        while(gap > 0){
            int left = 0;
            int right = left + gap;
            while(right < len){
                //nums1 and nums2
                if(left < m && right >= m){
                    swapIfGreater(nums1, left,nums2, right - m);
                }else if(left >= m){
                    swapIfGreater(nums2,  left - m,nums2, right - m);
                }else{
                    swapIfGreater(nums1,  left,nums1, right);
                }
                left++;
                right++;
            }
            if(gap == 1){
                break;
            }
            gap = (gap / 2) + (gap % 2);
        }
        for(int i = 0; i < n; i++) {
    nums1[m + i] = nums2[i];
}
    }
}