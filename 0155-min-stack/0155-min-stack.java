class MinStack {
    Stack <Integer> st = new Stack<>();
    Stack <Integer> minst = new Stack<>();
    public void push(int value) {
        st.push(value);
        minst.push(minst.isEmpty() ? value : Math.min(value,minst.peek()));
    }
    
    public void pop() {
        st.pop();
        minst.pop();
    }
    
    public int top() {
        return st.peek();
    }
    
    public int getMin() {
        return minst.peek();
    }
}

/**
 * Your MinStack object will be instantiated and called as such:
 * MinStack obj = new MinStack();
 * obj.push(value);
 * obj.pop();
 * int param_3 = obj.top();
 * int param_4 = obj.getMin();
 */