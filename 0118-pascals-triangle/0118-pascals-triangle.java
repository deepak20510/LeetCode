class Solution {
    public List<List<Integer>> generate(int numRows) {
        List<List<Integer>> result = new ArrayList<>();
        for(int row = 0;row < numRows;row++){
            List<Integer> currentRow = new ArrayList<>();
            long value = 1;
            for(int i = 0;i <= row;i++){
                currentRow.add((int) value);
                value = value * (row - i)/(i + 1);
            }
            result.add(currentRow);
        }
        return result;
    }
}