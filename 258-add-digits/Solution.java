class Solution {
    public int addDigits(int num) {
        int lastdigit = 0;
        int sum = 0;
        int finalsum = 0;
        int finalsum1 = 0;
        while (num > 0) {
            lastdigit = num % 10;
            num = num / 10;
            sum = sum + lastdigit;
        }
        int n2 = sum;
        int lastdigit2 = 0;
        while (n2 > 0) {
            lastdigit2 = n2 % 10;
            n2 = n2 / 10;
            finalsum = finalsum + lastdigit2;
        }
        int n3 = finalsum;
        int lastdigit3 =0;
        while (n3>0){
            lastdigit3 = n3%10;
            n3 = n3/10;
            finalsum1 = finalsum1 + lastdigit3;

        }
       return finalsum1;
    }
}