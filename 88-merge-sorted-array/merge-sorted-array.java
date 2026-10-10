class Solution {
    public void merge(int[] nums1, int m, int[] nums2, int n) {
        for(int j = 0,i=m;j<n;j++){
            nums1[i]=nums2[j];
            i++;
        }
        Arrays.sort(nums1);
    }
}
//         int[] merged = new int[m+n];
//         int i;
//         for(i = 0;i<m;i++){
//             merged[i] = nums1[i];
//         }
//         for(int j=0;j<n;j++){
//             merged[i] = nums2[j];
//             i++;
//         }
//         Arrays.sort(merged);
//         for(int k = 0;k<merged.length;k++){
//             nums1[k] = merged[k];
//         }
//     }
// }
