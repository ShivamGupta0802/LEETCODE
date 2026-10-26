class Solution {
    public int[] buildArray(int[] nums) {
     int i = 0;
     int[] ans = new int [nums.length];
     while(i<nums.length){
        ans[i] = nums[nums[i]];
        i++;
     }
     return ans;   
    }
}