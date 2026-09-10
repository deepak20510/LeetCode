/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    int nodmatcnt = 0;

    class Pair {
        int sum;
        int count;

        Pair(int sum, int count) {
            this.sum = sum;
            this.count = count;
        }
    }

    public Pair pathsumAvg(TreeNode root) {

        if (root == null)
            return new Pair(0, 0);
        Pair left = pathsumAvg(root.left);
        Pair right = pathsumAvg(root.right);

        int sum = left.sum + right.sum + root.val;
        int cnt = left.count + right.count + 1;

        int avg = sum / cnt;
        if (avg == root.val) {
            nodmatcnt++;
        }
        return new Pair(sum, cnt);
    }

    public int averageOfSubtree(TreeNode root) {
        pathsumAvg(root);
        return nodmatcnt;
    }
}