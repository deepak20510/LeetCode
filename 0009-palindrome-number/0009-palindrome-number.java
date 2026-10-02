class Solution {
    public boolean isPalindrome(int x) {
        int digits = 0;
        int reverse = 0;
        int original = x;
        while(x > 0){
            digits = x % 10;
            x = x / 10;
            reverse = reverse * 10 + digits;
        }
        if(reverse == original){
            return true;
        }else{
            return false;
        }
    }
}