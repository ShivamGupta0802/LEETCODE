class Solution {
    public boolean checkPerfectNumber(int num) { 
       int temp = 0;
       int div = 1;
       int sum = 0;
       
       while(num != div){
           temp = num % div;
           if(num%div == 0){
               sum = sum+div;
           }
           div++;
       }
       if(num==sum){
           return true;
       }else{
          return false;
       }
    }
}