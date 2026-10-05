class Solution {
    public void reverseString(char[] s) {
        int j = s.length-1;
        int i = 0;
        char temp = 0;
        for(;i<(s.length)/2;i++){
            temp = s[i];
            s[i] = s[j];
            s[j] = temp;
            j--;
            temp = s[i];
        }
    }
}