class Solution {
    public int subtractProductAndSum(int n) {
        int product =1;
        int sum = 0;
        int lastdigit = 0;
        while(n>0){
            lastdigit = n % 10;
            n = n / 10;
            sum = sum + lastdigit;
            product = product * lastdigit;
        }
        return product-sum;
    }
}
