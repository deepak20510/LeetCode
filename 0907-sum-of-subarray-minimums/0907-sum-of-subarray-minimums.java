class Solution {
    public int[] findNse(int[] arr) {
        int n = arr.length;
        int[] nse = new int[n];
        Stack<Integer> st = new Stack<>();
        for (int i = n - 1; i >= 0; i--) {
            while (!st.isEmpty() && arr[st.peek()] >= arr[i]) {
                st.pop();
            }
            nse[i] = st.isEmpty() ? n : st.peek();
            st.push(i);
        }
        return nse;
    }
    public int[] findPsee(int[] arr) {
        int n = arr.length;
        int[] psee = new int[n];
        Stack<Integer> st = new Stack<>();
        for (int i = 0; i < n; i++) {
            while (!st.isEmpty() && arr[st.peek()] > arr[i]) {
                st.pop();
            }
            psee[i] = st.isEmpty() ? -1 : st.peek();
            st.push(i);
        }
        return psee;
    }
    public int sumSubarrayMins(int[] arr) {
        int n = arr.length;
        int[] nse = findNse(arr);
        int[] psee = findPsee(arr);
        long total = 0;
        long mod = 1000000007L;
        for (int i = 0; i < n; i++) {
            long left = i - psee[i];
            long right = nse[i] - i;
            total = (total + (left * right % mod) * arr[i]) % mod;
        }
        return (int) total;
    }
}