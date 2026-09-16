class Solution {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length;
        int maxArea = 0;
        int nse = 0;
        int pse = 0;
        int element = 0;
        Stack<Integer> st = new Stack<>();
        for (int i = 0; i <= n - 1; i++) {
            while (!st.isEmpty() && heights[st.peek()] > heights[i]) {
                element = st.peek();
                st.pop();
                nse = i;
                pse = st.isEmpty() ? -1 : st.peek();
                maxArea = Math.max(maxArea, heights[element] * (nse - pse - 1));
            }
            st.push(i);
        }
        while (!st.isEmpty()) {
            nse = n;
            element = st.peek();
            st.pop();
            pse = st.isEmpty() ? -1 : st.peek();
            maxArea = Math.max(maxArea, heights[element] * (nse - pse - 1));
        }
        return maxArea;
    }
}