class Solution {
    public int[][] merge(int[][] intervals) {
        int n = intervals.length;
        Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
        List<int[]> result= new ArrayList<>(); 
        for(int i = 0;i < n;i++){
            int start = intervals[i][0];
            int end = intervals[i][1];
            if(result.isEmpty()){
                result.add(new int[]{start,end});
            }else if(start <= result.get(result.size() - 1)[1]){
                result.get(result.size() - 1)[1] =
                    Math.max(result.get(result.size() - 1)[1], end);
            }
            else{
                result.add(new int[]{start,end});
            }
        }
        return result.toArray(new int[result.size()][]);
    }
}