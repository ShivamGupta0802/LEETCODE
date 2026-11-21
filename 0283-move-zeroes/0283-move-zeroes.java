class Solution {
    public void moveZeroes(int[] nums) {
        int[] arr = new int[nums.length];
        int j = 1;
        int k = 0;
        int z = nums.length - 1;
        for(int i=0;i<nums.length;i++){
            if(nums[i] == 0){
                arr[z] = nums[i];
                z--; 
            }else{
                arr[k] = nums[i];
                k++;
            }
        }
        for(int i = 0;i<nums.length;i++){
            nums[i] = arr[i];
        }
    }
}