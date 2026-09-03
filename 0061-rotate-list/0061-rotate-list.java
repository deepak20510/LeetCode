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
    ListNode findNnode(ListNode temp,int k){
        int count = 1;
        while(temp != null){
            if(count == k) return temp;
            count++;
            temp = temp.next;
        }
        return temp;
    }
    public ListNode rotateRight(ListNode head, int k) {
        if(head == null || k == 0) return head;
        ListNode tail = head;
        int len = 1; 
        while(tail.next != null){
            tail = tail.next;
            len += 1;
        }
        if(k % len == 0) return head;
        k = k % len;
        tail.next = head;
        ListNode newLastNode = findNnode(head, len - k);
        head = newLastNode.next;
        newLastNode.next = null;
        return head;
    }
}