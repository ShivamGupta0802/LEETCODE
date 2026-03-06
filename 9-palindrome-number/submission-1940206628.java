class Solution {
    public boolean isPalindrome(int x) {
        int orignal = x;
        int lastdigit = 0;
        int reverse = 0;
        while (x!=0){
            lastdigit = x%10;
            x = x/10;
           reverse = reverse*10+lastdigit;
        }
        if (orignal<0)
        return false;
        if (orignal==reverse){
            return true;
        }
        else
            return false;
        }
        
    }