class Solution {
    public int maximumWealth(int[][] ac) {
        int h = 0;
        for(int i = 0;i<ac.length;i++){
            int t = 0;
            for(int j = 0;j<ac[i].length;j++){
                t += ac[i][j];
            }
            if(t>h){
                    h = t;
                }
        }
        return h;
    }
}