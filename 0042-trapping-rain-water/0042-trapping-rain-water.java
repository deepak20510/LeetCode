class Solution {

    public int[] getPrefixMax(int[] height) {
        int n = height.length;
        int[] prefixMax = new int[n];

        prefixMax[0] = height[0];

        for (int i = 1; i < n; i++) {
            prefixMax[i] = Math.max(prefixMax[i - 1], height[i]);
        }

        return prefixMax;
    }

    public int[] getPostfixMax(int[] height) {
        int n = height.length;
        int[] postfixMax = new int[n];

        postfixMax[n - 1] = height[n - 1];

        for (int i = n - 2; i >= 0; i--) {
            postfixMax[i] = Math.max(postfixMax[i + 1], height[i]);
        }

        return postfixMax;
    }

    public int trap(int[] height) {

        int total = 0;
        int n = height.length;

        int[] prefixMax = getPrefixMax(height);
        int[] postfixMax = getPostfixMax(height);

        for (int i = 0; i < n; i++) {
            total += Math.min(prefixMax[i], postfixMax[i]) - height[i];
        }

        return total;
    }
}