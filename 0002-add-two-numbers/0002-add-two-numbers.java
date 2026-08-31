/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dnode = new ListNode(0);
        ListNode temp = dnode;
        int carry = 0;
        ListNode h1 = l1;
        ListNode h2 = l2;
        int sum = 0;
        while (h1 != null || h2 != null) {


             sum = 0;
            if (h1 != null) {
                sum = sum + h1.val;
                h1 = h1.next;
            }

            if (h2 != null) {
                sum = sum + h2.val;
                h2 = h2.next;
            }
            sum += carry;
            int digit = sum % 10;
            carry = sum / 10;
            temp.next = new ListNode(digit);

            temp = temp.next;
        }
        

        if (carry > 0) {
            temp.next = new ListNode(carry);
        }
        return dnode.next;
    }
}