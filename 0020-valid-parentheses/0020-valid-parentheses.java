class Solution {
    public boolean isValid(String s) {
        Stack<Character> st = new Stack<>();

        char[] arr = s.toCharArray();

        for (char ch : arr) {
            if (ch == '(' || ch == '{' || ch == '[') {
                st.push(ch);
            } else {

                if (st.isEmpty())
                    return false;
                char top = st.pop();

                if (ch == ')' && top != '(')
                    return false;

                if (ch == '}' && top != '{')
                    return false;
                if (ch == ']' && top != '[')
                    return false;
            }
        }
        return st.isEmpty();
    }
}