class Solution {
    public int numIdenticalPairs(int[] n) {
      int i = 0;
      int c = 0;
      while(i<n.length){
        int j = i+1;
        while(j<n.length){
            if(n[i] == n[j]){
                c++;
            }
            j++;
        }
        i++;
      }
      return c;
    }
}