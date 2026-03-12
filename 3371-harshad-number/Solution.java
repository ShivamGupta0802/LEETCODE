class Solution {
    public int sumOfTheDigitsOfHarshadNumber(int x) {
      int sum = 0;
      int orignal = x;
      while(x>0){
        sum = sum + x%10;
         x = x/10;
      }  
      if (orignal % sum == 0){
        return sum;
      }else{
        return -1;
      }
    }
}