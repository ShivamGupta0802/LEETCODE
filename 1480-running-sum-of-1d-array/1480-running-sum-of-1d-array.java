class Solution {
    public int[] runningSum(int[] nums) {
        int runsum = 0;
        int i = 1;
        while(i<nums.length){
            nums[i] += nums[runsum];
            runsum++;
            i++;
        }
        return nums;
    }
}