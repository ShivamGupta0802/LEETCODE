class Solution {
    public void merge(int[] nums1, int m, int[] nums2, int n) {
        int[] merged = new int[m+n];
        int i = 0;
        while(i<m){
            merged[i] = nums1[i];
            i++;
        }
        int j = 0;
        while(j<n){
            merged[i] = nums2[j];
            i++;
            j++;
        }
        Arrays.sort(merged);
        int k = 0;
        while(k<merged.length){
            nums1[k] = merged[k];
            k++;
        }
    }
}