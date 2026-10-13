class Solution {
    public int numberOfEmployeesWhoMetTarget(int[] hours, int target) {
        int count = 0;
        for(int nums : hours){
            if(nums>=target){
                count++;
            }
        }
        return count;
    }
}