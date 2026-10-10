class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        int[] merge = new int[nums1.length+nums2.length];
        int i = 0;
        while(i<nums1.length){
            merge[i] = nums1[i];
            i++;
        }
        int j = 0;
        while(j<nums2.length){
            merge[i] = nums2[j];
            i++;
            j++;
    }
    Arrays.sort(merge);
    int n = merge.length;
   if(n%2 == 0){
    return (merge[n/2] + merge[n/2-1])/2.0;
        }else{
             return (merge[n/2]);
        }
    }
}
