"""
LeetCode 2: Add Two Numbers

Problem:
You are given two non-empty linked lists representing two non-negative integers.
The digits are stored in reverse order, and each of their nodes contains a single digit.
Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Example 1:
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807

Example 2:
Input: l1 = [0], l2 = [0]
Output: [0]

Example 3:
Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]
Explanation: 9999999 + 9999 = 10009998

Constraints:
- The number of nodes in each linked list is in the range [1, 100]
- 0 <= Node.val <= 9
- It is guaranteed that the list represents a number that does not have leading zeros
"""


class ListNode:
    """Definition for singly-linked list node."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def add_two_numbers(l1, l2):
    """
    Add two numbers represented as linked lists.

    Approach:
    Similar to adding two numbers by hand:
    1. Start from least significant digit (head of list)
    2. Add corresponding digits plus any carry
    3. Create new node with (sum % 10)
    4. Update carry to (sum // 10)
    5. Continue until both lists exhausted and no carry remains

    Visualization for 342 + 465:
    l1: 2 -> 4 -> 3 (represents 342)
    l2: 5 -> 6 -> 4 (represents 465)

    Step 1: 2 + 5 = 7, carry = 0
    Result: 7

    Step 2: 4 + 6 + 0 = 10, carry = 1
    Result: 7 -> 0

    Step 3: 3 + 4 + 1 = 8, carry = 0
    Result: 7 -> 0 -> 8

    Time Complexity: O(max(m, n)) where m, n are lengths of l1, l2
    Space Complexity: O(max(m, n)) for result list (not counting output)

    Args:
        l1: ListNode - first number (least significant digit first)
        l2: ListNode - second number (least significant digit first)

    Returns:
        ListNode - sum as linked list (least significant digit first)
    """
    dummy = ListNode(0)
    current = dummy
    carry = 0

    # Process while either list has digits or there's a carry
    while l1 or l2 or carry:
        # Get values (0 if list is exhausted)
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0

        # Calculate sum and new carry
        total = val1 + val2 + carry
        carry = total // 10
        digit = total % 10

        # Create new node
        current.next = ListNode(digit)
        current = current.next

        # Move to next nodes if available
        if l1:
            l1 = l1.next
        if l2:
            l2 = l2.next

    return dummy.next


def add_two_numbers_recursive(l1, l2, carry=0):
    """
    Add two numbers recursively.

    Approach:
    Base case: both lists empty and no carry
    Recursive case: add current digits + carry, recurse with next nodes

    Time Complexity: O(max(m, n))
    Space Complexity: O(max(m, n)) for recursion stack + result

    Args:
        l1: ListNode - first number
        l2: ListNode - second number
        carry: int - carry from previous addition

    Returns:
        ListNode - sum as linked list
    """
    # Base case: all exhausted
    if not l1 and not l2 and carry == 0:
        return None

    # Get values
    val1 = l1.val if l1 else 0
    val2 = l2.val if l2 else 0

    # Calculate sum
    total = val1 + val2 + carry
    new_carry = total // 10
    digit = total % 10

    # Create node for current digit
    result = ListNode(digit)

    # Recurse for next digits
    next1 = l1.next if l1 else None
    next2 = l2.next if l2 else None
    result.next = add_two_numbers_recursive(next1, next2, new_carry)

    return result


def add_two_numbers_verbose(l1, l2):
    """
    Add two numbers with detailed comments for learning.

    This is the same algorithm but with more explicit variable names
    and step-by-step logic for educational purposes.

    Time Complexity: O(max(m, n))
    Space Complexity: O(max(m, n))

    Args:
        l1: ListNode - first number
        l2: ListNode - second number

    Returns:
        ListNode - sum as linked list
    """
    # Dummy node to simplify list building
    result_head = ListNode(0)
    current_result = result_head

    carry_over = 0
    current_l1 = l1
    current_l2 = l2

    # Continue while there are digits to process or a carry remains
    while current_l1 is not None or current_l2 is not None or carry_over > 0:
        # Get digit values (use 0 if list is exhausted)
        digit_from_l1 = current_l1.val if current_l1 is not None else 0
        digit_from_l2 = current_l2.val if current_l2 is not None else 0

        # Add the two digits plus any carry from previous addition
        sum_of_digits = digit_from_l1 + digit_from_l2 + carry_over

        # Extract the ones digit for current position
        ones_digit = sum_of_digits % 10

        # Extract the tens digit as carry for next position
        carry_over = sum_of_digits // 10

        # Create new node with the ones digit
        new_node = ListNode(ones_digit)
        current_result.next = new_node
        current_result = new_node

        # Move to next digits if available
        if current_l1 is not None:
            current_l1 = current_l1.next
        if current_l2 is not None:
            current_l2 = current_l2.next

    # Return head of result list (skip dummy node)
    return result_head.next


# Helper functions for testing

def create_list(values):
    """Create a linked list from a list of values."""
    if not values:
        return None

    head = ListNode(values[0])
    current = head
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next

    return head


def list_to_array(head):
    """Convert linked list to Python list."""
    result = []
    current = head
    while current:
        result.append(current.val)
        current = current.next
    return result


def list_to_number(head):
    """
    Convert linked list to integer (for verification).

    Args:
        head: ListNode - linked list representing number

    Returns:
        int - the actual number
    """
    number = 0
    multiplier = 1
    current = head

    while current:
        number += current.val * multiplier
        multiplier *= 10
        current = current.next

    return number


def number_to_list(num):
    """
    Convert integer to linked list representation.

    Args:
        num: int - number to convert

    Returns:
        ListNode - linked list with digits in reverse order
    """
    if num == 0:
        return ListNode(0)

    head = None
    current = None

    while num > 0:
        digit = num % 10
        node = ListNode(digit)

        if not head:
            head = node
            current = node
        else:
            current.next = node
            current = node

        num //= 10

    return head


def print_list(head):
    """Print linked list in readable format."""
    values = []
    current = head
    while current:
        values.append(str(current.val))
        current = current.next
    print(" -> ".join(values) if values else "Empty list")


def visualize_addition(num1, num2):
    """
    Visualize the addition process.

    Args:
        num1: int - first number
        num2: int - second number
    """
    print(f"\nAdding {num1} + {num2} = {num1 + num2}")
    print("="*50)

    # Convert to lists
    l1 = number_to_list(num1)
    l2 = number_to_list(num2)

    print(f"\nList 1 (reversed): {list_to_array(l1)} represents {num1}")
    print(f"List 2 (reversed): {list_to_array(l2)} represents {num2}")

    # Perform addition with step-by-step output
    print("\nAddition process:")
    dummy = ListNode(0)
    current = dummy
    carry = 0

    p1, p2 = l1, l2
    position = 0

    while p1 or p2 or carry:
        val1 = p1.val if p1 else 0
        val2 = p2.val if p2 else 0

        total = val1 + val2 + carry
        digit = total % 10
        new_carry = total // 10

        print(f"Position {position}: {val1} + {val2} + {carry}(carry) = {total} "
              f"-> digit={digit}, carry={new_carry}")

        current.next = ListNode(digit)
        current = current.next

        carry = new_carry
        position += 1

        if p1:
            p1 = p1.next
        if p2:
            p2 = p2.next

    result = dummy.next
    print(f"\nResult list: {list_to_array(result)} represents {list_to_number(result)}")


def test_add_two_numbers():
    """Test cases for adding two numbers."""

    approaches = [
        ("Iterative", add_two_numbers),
        ("Recursive", add_two_numbers_recursive),
        ("Verbose (educational)", add_two_numbers_verbose)
    ]

    for name, func in approaches:
        print(f"\nTesting {name}:")

        # Test 1: Normal addition
        l1 = create_list([2, 4, 3])  # 342
        l2 = create_list([5, 6, 4])  # 465
        result = func(l1, l2)
        assert list_to_array(result) == [7, 0, 8]  # 807
        assert list_to_number(result) == 807
        print("Test 1 (342 + 465): PASSED")

        # Test 2: Both zero
        l1 = create_list([0])
        l2 = create_list([0])
        result = func(l1, l2)
        assert list_to_array(result) == [0]
        print("Test 2 (0 + 0): PASSED")

        # Test 3: Different lengths with carry
        l1 = create_list([9, 9, 9, 9, 9, 9, 9])  # 9999999
        l2 = create_list([9, 9, 9, 9])  # 9999
        result = func(l1, l2)
        assert list_to_number(result) == 10009998
        print("Test 3 (9999999 + 9999): PASSED")

        # Test 4: One digit each
        l1 = create_list([5])
        l2 = create_list([5])
        result = func(l1, l2)
        assert list_to_array(result) == [0, 1]  # 10
        print("Test 4 (5 + 5): PASSED")

        # Test 5: Different lengths, no carry
        l1 = create_list([1, 2, 3])  # 321
        l2 = create_list([4, 5])  # 54
        result = func(l1, l2)
        assert list_to_number(result) == 375
        print("Test 5 (321 + 54): PASSED")

        # Test 6: Carry propagation
        l1 = create_list([9, 9])  # 99
        l2 = create_list([1])  # 1
        result = func(l1, l2)
        assert list_to_array(result) == [0, 0, 1]  # 100
        print("Test 6 (99 + 1 with carry propagation): PASSED")

    print("\nAll tests passed!")


if __name__ == "__main__":
    # Run tests
    test_add_two_numbers()

    print("\n" + "="*50)
    print("Visualization Examples")
    print("="*50)

    # Visualize additions
    visualize_addition(342, 465)
    visualize_addition(9999999, 9999)
    visualize_addition(99, 1)

    print("\n" + "="*50)
    print("Key Insights")
    print("="*50)
    print("\n1. Numbers stored in REVERSE order (least significant first)")
    print("2. Process is just like hand addition: digit by digit with carry")
    print("3. Handle different lengths by treating missing digits as 0")
    print("4. Don't forget final carry (e.g., 99 + 1 = 100)")
    print("5. Dummy node simplifies building the result list")

    print("\n" + "="*50)
    print("Common Mistakes")
    print("="*50)
    print("\n1. Forgetting to check for final carry after both lists exhausted")
    print("2. Not handling different list lengths correctly")
    print("3. Confusing the order (numbers are in REVERSE)")
    print("4. Creating result list in wrong order")
    print("5. Not using dummy node (makes code more complex)")

    print("\n" + "="*50)
    print("Extension: Forward Order")
    print("="*50)
    print("\nIf numbers were in forward order (most significant first):")
    print("- Would need to reverse both lists first")
    print("- Or use recursion to reach the end first")
    print("- Or use a stack to reverse the processing order")
    print("- More complex than reverse order!")
