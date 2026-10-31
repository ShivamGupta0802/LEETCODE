class Solution {
    public int numTeams(int[] rating) {
        int Finalteams = 0;
        for (int j = 1; j < rating.length - 1; j++) {
        int leftSmaller = 0;
        int leftGreater = 0;
        int rightSmaller = 0;
        int rightGreater = 0;
            for (int i = 0; i < j; i++) {
                if(rating[i]<rating[j]){
                    leftSmaller++;
                }else{
                    leftGreater++;
                }
            }
            for (int k = j + 1; k < rating.length; k++) {
                if(rating[k]>rating[j]){
                    rightGreater++;
                }else{
                    rightSmaller++;
                }
            }
            int NewTeams = (leftSmaller * rightGreater) + (leftGreater * rightSmaller);
            Finalteams += NewTeams;
        }
        return Finalteams;
    }
}