class Solution {
    public boolean threeConsecutiveOdds(int[] arr) {
        for(int i = 0 ,j = i + 1,k = i+2;i<arr.length && j<arr.length && k<arr.length;i++,j++,k++){
            if(arr[i]%2 != 0 && arr[j] % 2 != 0 && arr[k]  % 2 != 0){
                return true;
            }
        }
        return false;
    }
}