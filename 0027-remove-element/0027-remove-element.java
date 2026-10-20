class Solution {
    public int removeElement(int[] nums, int val) {
        int i = 0;
        int j = nums.length-1;
        int temp = 0;
        while(i<=j){
            if(nums[i] != val){
                i++;
            } else if(nums[j] == val){
                j--;
            }else{
                temp = nums[j];
                nums[j] = nums[i];
                nums[i] = temp;
                j--;
            }
        }
        return i;
    }
}