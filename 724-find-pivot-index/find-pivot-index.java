class Solution {
    public int pivotIndex(int[] nums) {
        int i = 0;
        int tsum = 0;
        int rsum = 0;
        int lsum = 0;
        for(;i<nums.length;i++){
            tsum += nums[i];
        }
        i = 0;
        for(;i<nums.length;i++){
            rsum = tsum-lsum-nums[i];
            if(rsum==lsum){
            return i;
        }
            lsum +=nums[i];
        }
        return -1;
    }
}
