class Solution {
    public int[] smallerNumbersThanCurrent(int[] nums) {
        int i = 0;
        int[] arr = new int[nums.length];
        while (i < nums.length) {
            int j = 0;
            int count = 0;
            while (j < nums.length) {
                if (nums[i] > nums[j]) {
                    count++;
                }
                j++;
            }
            arr[i] = count;
            i++;
        }
        return arr;
    }
}