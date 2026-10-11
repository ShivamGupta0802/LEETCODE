class Solution {
    public int[] sortedSquares(int[] nums) {
        int arr[] = new int [nums.length];
        int i = 0,j = nums.length - 1;
        int k = nums.length-1;
        while(i<=j){
           if(Math.abs(nums[i])>Math.abs(nums[j])){
                arr[k] = nums[i]*nums[i];
                i++;
            }else{
                arr[k] = nums[j]*nums[j];
                j--;
            }
            k--;
        }
        return arr;
    }
}
// Using abs cause Array is sorted and we can just compare absloute vale cause bigger abs valuse = bigger square so when we fing bigger abs value , we square it normal value and update our new Array Right to Left


// My First Approach
// class Solution {
//     public int[] sortedSquares(int[] nums) {
//         int arr[] = new int [nums.length];
//         int i = 0,j = nums.length - 1;
//         int k = nums.length-1;
//         while(i<=j){
//             int left = nums[i]*nums[i];
//             int right = nums[j]*nums[j];
//             if(left>right){
//                 arr[k] = left;
//                 i++;
//             }else{
//                 arr[k] = right;
//                 j--;
//             }
//             k--;
//         }
//         return arr;
//     }
// }