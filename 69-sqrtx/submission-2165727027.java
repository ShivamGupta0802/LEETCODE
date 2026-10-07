class Solution {
    public int mySqrt(int x) {
        // if(x==1 || x == 2){
        //     return 1;
        // }
        int high = x;
        int low = 0;
        while(low<=high){
            int mid = (low + high)/2;
            long sqr = (long)mid * mid;
            if(sqr == x){
                return mid;
            }
            if(sqr>x){
                high = mid-1;
            }else{
                low = mid +1;
            }
        }
        return high;
    }
}