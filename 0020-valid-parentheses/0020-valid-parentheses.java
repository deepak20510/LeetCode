class Solution {
    public boolean isValid(String s) {
        Stack<Character> st = new Stack<>();
        int n = s.length();
        for (int i = 0; i < n; i++) {
            if (s.charAt(i) == '(' || s.charAt(i) == '[' || s.charAt(i) == '{') {
                st.push(s.charAt(i));
            } else {
                if (st.empty())
                    return false;
                char ch = st.pop();
                if ((s.charAt(i) == ')' && ch == '(') ||
                        (s.charAt(i) == ']' && ch == '[') ||
                        (s.charAt(i) == '}' && ch == '{')) {
                } else {
                    return false;
                }
            }
        }
        return st.isEmpty();
    }
}