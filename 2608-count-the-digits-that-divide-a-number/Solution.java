class Solution {
    public int countDigits(int num) {
        int count = 0;
        int org = num;
        while(num>0){
           int ld = num % 10;
            num = num / 10;
            if(org % ld == 0 ){
                count++;
            }
        }
        return count;
    }
}