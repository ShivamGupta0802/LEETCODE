class Solution {
    public int maximumCount(int[] nums) {
        int pos = 0;
        int neg = 0;
        int i = 0;
        while(i<nums.length){
            if(nums[i]<0){
                pos = pos+1;
            }
            if(nums[i]>0){
                neg = neg+1;
            }
            i++;
        }
        return Math.max(pos,neg);
    }
}