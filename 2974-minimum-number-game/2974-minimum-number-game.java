class Solution {
    public int[] numberGame(int[] nums) {
        Arrays.sort(nums);
        int alice = 0;
        int bob = 1;
        int temp = 0;
        while(bob<nums.length){
            temp = nums[alice];
            nums[alice] = nums[bob];
            nums[bob] = temp;
            alice+=2;
            bob+=2;
        }
        return nums;
    }
}