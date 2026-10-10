class Solution {
    public int removeDuplicates(int[] nums) {
        int i =0;
        int j = 1;
        while(j<nums.length){
            if(nums[i] != nums[j]){
            i++;
            nums[i] = nums[j];
            }
              j++;
        }
        return i+1;
    }
}

// class Solution {
//     public int removeDuplicates(int[] nums) {
//         int i =0;
//         int j = 1;
//         while(j<nums.length){
//             if(nums[i] == nums[j]){
//               j++;  
//             }
//             if(j<nums.length && nums[i] != nums[j]){
//                 i++;
//                 nums[i] = nums[j];
//             }
//         }
//         return i+1;
//     }
// }