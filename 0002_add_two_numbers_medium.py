from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        """
        Add two numbers represented as linked lists.

        Approach:
        - Traverse both lists simultaneously
        - Add corresponding digits plus carry
        - Create new nodes for the result
        - Handle carry at the end if needed

        Time Complexity: O(max(m, n)) where m and n are lengths of l1 and l2
        Space Complexity: O(max(m, n)) for the result list
        """
        dummy = ListNode(0)  # Dummy head for result list
        current = dummy
        carry = 0

        # Process both lists while either has nodes or there's a carry
        while l1 or l2 or carry:
            # Get values from current nodes (or 0 if node is None)
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            # Calculate sum and new carry
            total = val1 + val2 + carry
            carry = total // 10
            digit = total % 10

            # Create new node with the digit
            current.next = ListNode(digit)
            current = current.next

            # Move to next nodes if they exist
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next

        return dummy.next  # Return the actual head (skip dummy)
        
def list_to_linkedlist(arr):
    """Helper function to convert a list to a linked list."""
    dummy = ListNode(0)
    current = dummy
    for val in arr:
        current.next = ListNode(val)
        current = current.next
    return dummy.next

def linkedlist_to_list(node):
    """Helper function to convert a linked list to a list."""
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result

if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    l1 = list_to_linkedlist([2, 4, 3])
    l2 = list_to_linkedlist([5, 6, 4])
    result = linkedlist_to_list(solution.addTwoNumbers(l1, l2))
    print(f"Input: l1 = [2, 4, 3], l2 = [5, 6, 4]")
    print(f"Output: {result}")
    print(f"Expected: [7, 0, 8]")
    print(f"Explanation: 342 + 465 = 807\n")

    # Test case 2
    l1 = list_to_linkedlist([0])
    l2 = list_to_linkedlist([0])
    result = linkedlist_to_list(solution.addTwoNumbers(l1, l2))
    print(f"Input: l1 = [0], l2 = [0]")
    print(f"Output: {result}")
    print(f"Expected: [0]")
    print(f"Explanation: 0 + 0 = 0\n")

    # Test case 3
    l1 = list_to_linkedlist([9, 9, 9, 9, 9, 9, 9])
    l2 = list_to_linkedlist([9, 9, 9, 9])
    result = linkedlist_to_list(solution.addTwoNumbers(l1, l2))
    print(f"Input: l1 = [9, 9, 9, 9, 9, 9, 9], l2 = [9, 9, 9, 9]")
    print(f"Output: {result}")
    print(f"Expected: [8, 9, 9, 9, 0, 0, 0, 1]")
    print(f"Explanation: 9999999 + 9999 = 10009998\n")