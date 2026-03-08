class Solution {
    public int addDigits(int num) {
        int lastdigit = 0;
        int sum = 0;
        int finalsum1 = 0;
        while (num > 0) {
            lastdigit = num % 10;
            num = num / 10;
            sum = sum + lastdigit;
        }
        int n2= sum , n3= sum;
        while(n3 > 9)
        {       
             int lastdigit2 = 0;
             int finalsum = 0;
            while (n2 > 0) {
            lastdigit2 = n2 % 10;
            n2 = n2 / 10;
            finalsum = finalsum + lastdigit2;
        }
         n2 = finalsum;
        n3 = finalsum;
        }
       return n3;
    }
}
