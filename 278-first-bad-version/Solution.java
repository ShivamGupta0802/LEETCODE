/* The isBadVersion API is defined in the parent class VersionControl.
      boolean isBadVersion(int version); */

public class Solution extends VersionControl {
    public int firstBadVersion(int n) {
        int low = 1;
        int h = n;
        while(low<h){
            int mid = (low) + (h-low)/2;
            if(isBadVersion(mid)){
                 h = mid;
            }else{
                low = mid+1;
            }
        }
        return low;
    }
}