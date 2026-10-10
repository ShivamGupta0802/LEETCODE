class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        int i = 0;
        while (i< matrix.length){
            int j = 0;
            while (j<matrix[i].length){
                if(matrix[i][j] == target){
                    return true;
                }
                j++;
            }
            i++;
        }
        return false;
    }
}
