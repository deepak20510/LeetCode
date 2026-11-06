class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        int n = matrix.length;
        int cn = matrix[0].length;
        int row = 0;
        int col = cn - 1;
        while(row < n && col >= 0){
            if(matrix[row][col] == target){
                return true;
            }else if(matrix[row][col] < target){
                row++;
            }else{
                col--;
            }
        }
        return false;
    }
}