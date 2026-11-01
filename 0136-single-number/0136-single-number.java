class Solution {
    public int singleNumber(int[] nums) {
        int i = 0;
        while(i<nums.length){
            int j = 0;
            int count = 0;
            while(j<nums.length){
                if(nums[i] == nums[j]){
                    count++;
                }
                j++;
            }
            if(count == 1){
                return nums[i];
            }
            i++;
        }
        return 0;
    }
}