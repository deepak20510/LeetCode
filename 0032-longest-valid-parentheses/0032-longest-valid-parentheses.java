class Solution {
    public int longestValidParentheses(String s) {
        int n = s.length();
        int answer = 0;
        int open = 0;
        int close = 0;
        for(int i = 0; i <= n-1; i++){
            if(s.charAt(i) == '('){
                open++;
            }else{
                close++;
            }
            if(open == close){
                answer = Math.max(answer,2*close);
            }else if(close > open){
                open = close = 0;
            }
        }
        open = close = 0;
        for(int i = n-1; i >= 0; i--){
            if(s.charAt(i) == '('){
                open++;
            }else{
                close++;
            }
            if(open == close){
                answer = Math.max(answer,2*open);
            }else if(open > close){
                open = close = 0;
            }
        }
        return answer;
    }
}