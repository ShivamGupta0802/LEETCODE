class Solution {
    public int[] twoSum(int[] nums, int target) {
      int i;
      for(i=0;i<nums.length;i++){
        for(int j = i+1;j<nums.length;j++){
            if(target==nums[i]+nums[j]){
                // arr[0] = i;
                // arr[1] = j;
                return new int[]{i,j};
            }
        }
      }
      return new int[]{};
    }
}