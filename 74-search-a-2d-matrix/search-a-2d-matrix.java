class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        int low = 0;
        int high = (matrix[0].length*matrix.length) - 1;
        while(low <= high){
           int mid = (low + high)/2;
           int  col = matrix[0].length;
           int  row = mid/col;
           int column = mid%col;
        if(matrix[row][column] == target){
                  return true;
            }
            if(matrix[row][column]>target){
                high = mid-1;
            }else{
                    low = mid+1;
            }
        }
        return false;
    }
}
