class Solution {
    public int[] findNse(int[] heights) {
        int n = heights.length;
        int[] nse = new int[n];
        Stack<Integer> st = new Stack<>();
        for (int i = n - 1; i >= 0; i--) {
            while (!st.isEmpty() && heights[st.peek()] >= heights[i]) {
                st.pop();
            }
            nse[i] = st.isEmpty() ? n : st.peek();
            st.push(i);
        }
        return nse;
    }

    public int[] findPsee(int[] heights) {
        int n = heights.length;
        int[] psee = new int[n];
        Stack<Integer> st = new Stack<>();
        for (int i = 0; i < n; i++) {
            while (!st.isEmpty() && heights[st.peek()] > heights[i]) {
                st.pop();
            }
            psee[i] = st.isEmpty() ? -1 : st.peek();
            st.push(i);
        }
        return psee;
    }
    public int largestRectangleArea(int[] heights) {
        int n = heights.length;
        int [] nse = findNse(heights);
        int [] psee = findPsee(heights);
        int max = 0;
        for(int i = 0;i <= n-1;i++){
            max = Math.max(max,heights[i] * (nse[i] - psee[i] - 1));
        }
        return max;
    }
}