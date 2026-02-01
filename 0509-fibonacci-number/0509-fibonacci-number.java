class Solution {
    public int fib(int n) {
        if(n <= 1)
        {
            return n;
        }
        return fib(n-1) + fib(n-2);
    }
    public static void main(String args[])
    {
        int n = 3;
        Solution obj = new Solution();
        int result = obj.fib(n);
        System.out.println(result);
    }
}