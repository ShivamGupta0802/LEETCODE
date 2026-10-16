class Solution {
    public boolean canAliceWin(int[] nums) {
        int s = 0;
        int ts = 0;
        int d = 0;
     for(int i = 0;i<nums.length;i++){
        if(nums[i]<=9){
          s += nums[i];  
        }
        ts += nums[i];
        
     }
     d = (ts - s);
     return s!=d;
    }
}