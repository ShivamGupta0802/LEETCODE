class Solution {
    public boolean checkPerfectNumber(int num) { 
       int div = 1;
       int sum = 0;
       
       while(num != div){
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