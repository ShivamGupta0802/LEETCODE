// class Solution {
//     public int pivotIndex(int[] nums) {
//       for(int i = 0;i<nums.length;i++){
//               int sumr = 0;
//               int suml = 0;
//         for(int j = i+1;j < nums.length;j++){
//        sumr  += nums[j];
//       }
//        for(int j = i-1;j>=0;j--){
//         suml +=nums[j];
//        }
//        if(sumr == suml){
//         return i;
//        }
//       }
//       return -1;
//     }
// }
class Solution {
    public int pivotIndex(int[] nums) {

        int i = 0;

        while (i < nums.length) {

            int suml = 0;
            int sumr = 0;

            int j = i + 1;
            while (j < nums.length) {
                sumr += nums[j];
                j++;
            }

            j = i - 1;
            while (j >= 0) {
                suml += nums[j];
                j--;
            }

            if (suml == sumr) {
                return i;
            }

            i++;
        }

        return -1;
    }
}