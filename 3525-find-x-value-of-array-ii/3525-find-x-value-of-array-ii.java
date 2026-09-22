import java.util.*;

class Solution {

    class Node {
        int product;
        int[] count;

        Node(int k) {
            count = new int[k];
        }
    }

    int k;
    Node[] tree;

    public int[] resultArray(int[] nums, int k, int[][] queries) {
        this.k = k;

        int n = nums.length;
        tree = new Node[4 * n];

        build(1, 0, n - 1, nums);

        int[] ans = new int[queries.length];

        for (int i = 0; i < queries.length; i++) {

            int index = queries[i][0];
            int value = queries[i][1];
            int start = queries[i][2];
            int x = queries[i][3];

            update(1, 0, n - 1, index, value);

            Node result = query(1, 0, n - 1, start, n - 1);

            ans[i] = result.count[x];
        }

        return ans;
    }

    void build(int node, int left, int right, int[] nums) {

        tree[node] = new Node(k);

        if (left == right) {
            int rem = nums[left] % k;

            tree[node].product = rem;
            tree[node].count[rem] = 1;

            return;
        }

        int mid = (left + right) / 2;

        build(node * 2, left, mid, nums);
        build(node * 2 + 1, mid + 1, right, nums);

        tree[node] = merge(tree[node * 2], tree[node * 2 + 1]);
    }

    Node merge(Node a, Node b) {

        Node res = new Node(k);

        res.product = (a.product * b.product) % k;

        for (int r = 0; r < k; r++) {
            res.count[r] += a.count[r];
        }

        for (int r = 0; r < k; r++) {
            int newRemainder = (a.product * r) % k;

            res.count[newRemainder] += b.count[r];
        }

        return res;
    }

    void update(int node, int left, int right,
                int index, int value) {

        if (left == right) {

            int rem = value % k;

            tree[node] = new Node(k);
            tree[node].product = rem;
            tree[node].count[rem] = 1;

            return;
        }

        int mid = (left + right) / 2;

        if (index <= mid) {
            update(node * 2, left, mid, index, value);
        } else {
            update(node * 2 + 1, mid + 1, right, index, value);
        }

        tree[node] = merge(tree[node * 2], tree[node * 2 + 1]);
    }

    Node query(int node, int left, int right,
               int ql, int qr) {

        if (ql <= left && right <= qr) {
            return tree[node];
        }

        int mid = (left + right) / 2;

        if (qr <= mid) {
            return query(node * 2, left, mid, ql, qr);
        }

        if (ql > mid) {
            return query(node * 2 + 1, mid + 1, right, ql, qr);
        }

        Node a = query(node * 2, left, mid, ql, qr);
        Node b = query(node * 2 + 1, mid + 1, right, ql, qr);

        return merge(a, b);
    }
}