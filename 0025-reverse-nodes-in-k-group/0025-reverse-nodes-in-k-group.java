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
    private ListNode getKnode(ListNode temp, int k) {
        k -= 1;
        while (temp != null && k > 0) {
            k--;
            temp = temp.next;
        }
        return temp;
    }

    private ListNode reverse(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode front = curr.next;
            curr.next = prev;
            prev = curr;
            curr = front;
        }
        return prev;
    }

    public ListNode reverseKGroup(ListNode head, int k) {
        ListNode temp = head;
        ListNode nextNode;
        ListNode prevNode = null;
        while (temp != null) {
            ListNode Knode = getKnode(temp, k);
            if (Knode == null) {
                if (prevNode != null) {
                    prevNode.next = temp;
                }
                break;
            }
            nextNode = Knode.next;
            Knode.next = null;
            reverse(temp);
            if (temp == head) {
                head = Knode;
            } else {
                prevNode.next = Knode;
            }
            prevNode = temp;
            temp = nextNode;
        }
        return head;
    }
}