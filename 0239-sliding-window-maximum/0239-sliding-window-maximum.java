class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        List <Integer> lt = new ArrayList<>();
        Deque <Integer> dq = new ArrayDeque<>();
        int n = nums.length;
        for(int i = 0; i <= n-1; i++){
            if(!dq.isEmpty() && dq.peekFirst() <= i - k){
                dq.pollFirst();
            }
            while(!dq.isEmpty() && nums[dq.peekLast()] <= nums[i]){
                dq.pollLast();;
            }
            dq.addLast(i);
            if(i >= k - 1)  lt.add(nums[dq.peekFirst()]);
        }
        return lt.stream().mapToInt(Integer::intValue).toArray();
    }
}