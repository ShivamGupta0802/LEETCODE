class Solution {
    public int reverse(int x) {
        if (x<=-2147483648 || x>=2147483647){
            return 0;
        }
        int lastdigit = 0;
        int reverse = 0;
        while (x != 0) {
            lastdigit = x % 10;
            x = x / 10;
            if (reverse>214748364 || reverse<-214748364){
                return 0;
            }
            reverse = reverse * 10 + (lastdigit);
        }
        return reverse;
    }
}