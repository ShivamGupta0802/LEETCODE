class Solution {
    public void merge(int[] nums1, int m, int[] nums2, int n) {
        int[] merged = new int[m+n];
        int i;
        // while(i<m){
        //     merged[i] = nums1[i];
        //     i++;
        for(i = 0;i<m;i++){
            merged[i] = nums1[i];
        }
        // int j = 0;
        // while(j<n){
        //     merged[i] = nums2[j];
        //     i++;
        //     j++;
        for(int j=0;j<n;i++){
            merged[i] = nums2[j];
            j++;
        }
        Arrays.sort(merged);
        // int k = 0;
        // while(k<merged.length){
        //     nums1[k] = merged[k];
        //     k++;
        // }
        for(int k = 0;k<merged.length;k++){
            nums1[k] = merged[k];
        }
    }
}