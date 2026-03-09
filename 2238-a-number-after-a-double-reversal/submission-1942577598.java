class Solution {
    public boolean isSameAfterReversals(int num) {
        int orignal = num;
        int lastdigit = 0;
        int reverse = 0;
        int y = 0;
        int finalrev = 0;
        while (num != 0) {
            lastdigit = num % 10;
            num = num / 10;
            reverse = reverse * 10 + (lastdigit);
            y = reverse;
        }
        while (y != 0) {
            lastdigit = y % 10;
            y = y / 10;
            finalrev = finalrev * 10 + (lastdigit);
        }
        if (finalrev == orignal) {
            return true;
        } else {
            return false;
        }
    }
}