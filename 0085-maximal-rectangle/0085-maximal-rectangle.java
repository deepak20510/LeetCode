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

    public int maximalRectangle(char[][] matrix) {
        int m = matrix.length;
        int n = matrix[0].length;
        int[] heights = new int[n];
        int maxArea = 0;
        for(int i = 0; i< m;i++){
            for(int j = 0; j < n; j++){
                if(matrix[i][j] == '1')   heights[j]++;
                else    heights[j] = 0;
            }
            int area = largestRectangleArea(heights);
            maxArea = Math.max(maxArea, area);
        }
        return maxArea;
    }
}