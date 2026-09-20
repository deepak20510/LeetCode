class MinStack {

    Stack <Long> st = new Stack<>();
    long min;
    
    public void push(int value) {
        if(st.isEmpty()){
            st.push((long) value);
            min = value;
        }else if(value < min){
            st.push(2L * value - min);
            min = value;
        }else{
            st.push((long) value);
        }
    }
    public void pop() {
        long top = st.pop();
        if(top < min){
            min = 2 * min - top;
        }
    }
    
    public int top() {
        long top = st.peek();
        if(top < min){
            return (int)min;
        }
        return (int) top;
    }
    
    public int getMin() {
        return (int) min;
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