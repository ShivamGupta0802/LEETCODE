class Solution {
    public int mySqrt(int x) {
        if(x==1 || x == 2){
            return 1;
        }
        for(int i = 0 ; i<x; i++){
            long sqr = (long) i * i ;
            if(x == sqr){
                return i;
            }
            if(sqr>x){
                return i-1;
            }
        }
        return 0;
    }
}