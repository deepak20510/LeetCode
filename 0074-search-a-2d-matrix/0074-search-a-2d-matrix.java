class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        int rn = matrix.length;
        int cn = matrix[0].length;
        int low = 0;
        int high = (rn*cn) - 1;
        while(low <= high){
            int mid = (low + high) / 2;
            int nr = mid / cn;
            int nc = mid % cn;
            if(matrix[nr][nc] > target){
                high = mid - 1;
            }else if(matrix[nr][nc] < target){
                low = mid + 1;
            }else{
                return true;
            }
        }
        return false;
    }
}
