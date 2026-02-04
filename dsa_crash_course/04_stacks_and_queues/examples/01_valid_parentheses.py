"""
Valid Parentheses (LeetCode #20)

Problem:
Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

Example 1:
Input: s = "()"
Output: true

Example 2:
Input: s = "()[]{}"
Output: true

Example 3:
Input: s = "(]"
Output: false

Example 4:
Input: s = "([)]"
Output: false
Explanation: The brackets are interleaved incorrectly.

Example 5:
Input: s = "{[]}"
Output: true

Constraints:
- 1 <= s.length <= 10^4
- s consists of parentheses only '()[]{}'
"""


def is_valid(s):
    """
    Stack-based approach - optimal solution.

    Approach:
    1. Use a stack to track opening brackets
    2. For each opening bracket, push to stack
    3. For each closing bracket, check if it matches top of stack
    4. At the end, stack should be empty (all matched)

    Why this works:
    - Brackets must close in reverse order they opened (LIFO)
    - Stack is perfect for LIFO behavior
    - If closing bracket doesn't match top, it's invalid
    - If stack is empty when we see closing bracket, it's invalid
    - If stack is not empty at end, some brackets never closed

    Time Complexity: O(n) - single pass through string
    Space Complexity: O(n) - worst case all opening brackets

    Args:
        s: String containing only parentheses characters

    Returns:
        True if valid, False otherwise
    """
    # Map opening brackets to their corresponding closing brackets
    matching = {
        '(': ')',
        '[': ']',
        '{': '}'
    }

    stack = []

    for char in s:
        if char in matching:
            # Opening bracket - push to stack
            stack.append(char)
        else:
            # Closing bracket - check if matches top of stack
            if not stack:
                # No opening bracket for this closing bracket
                return False

            opening = stack.pop()
            if matching[opening] != char:
                # Wrong type of closing bracket
                return False

    # Stack should be empty if all brackets matched
    return len(stack) == 0


def is_valid_alternative(s):
    """
    Alternative approach storing closing brackets in stack.

    Same time/space complexity but slightly different implementation.
    Some people find this more intuitive.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    stack = []
    closing = {')': '(', ']': '[', '}': '{'}

    for char in s:
        if char in closing:
            # Closing bracket - check if matches
            if not stack or stack.pop() != closing[char]:
                return False
        else:
            # Opening bracket - push to stack
            stack.append(char)

    return not stack


def is_valid_replace(s):
    """
    String replacement approach - NOT recommended but worth knowing.

    Approach:
    Keep replacing matched pairs until no more replacements possible.
    If string becomes empty, it was valid.

    Time Complexity: O(n²) - potentially n replacements, each O(n)
    Space Complexity: O(n) - string creation

    Note: This is much slower than the stack approach!
    Good for demonstrating you understand alternatives.
    """
    while '()' in s or '[]' in s or '{}' in s:
        s = s.replace('()', '')
        s = s.replace('[]', '')
        s = s.replace('{}', '')

    return len(s) == 0


def test_valid_parentheses():
    """Test cases covering various scenarios."""

    # Test case 1: Single pair
    assert is_valid("()") == True

    # Test case 2: Multiple types
    assert is_valid("()[]{}") == True

    # Test case 3: Wrong type
    assert is_valid("(]") == False

    # Test case 4: Wrong order (interleaved)
    assert is_valid("([)]") == False

    # Test case 5: Nested brackets
    assert is_valid("{[]}") == True

    # Test case 6: Only opening brackets
    assert is_valid("(((") == False

    # Test case 7: Only closing brackets
    assert is_valid(")))") == False

    # Test case 8: Complex nested valid
    assert is_valid("{[()]}") == True

    # Test case 9: Complex nested invalid
    assert is_valid("{[(])}") == False

    # Test case 10: Long valid string
    assert is_valid("(){}[](){}[]") == True

    # Test case 11: Closing bracket first
    assert is_valid(")(") == False

    # Test case 12: Single opening
    assert is_valid("(") == False

    # Test case 13: Single closing
    assert is_valid(")") == False

    # Test case 14: Deep nesting
    assert is_valid("(((())))") == True

    # Test case 15: Mixed deep nesting
    assert is_valid("({[]})") == True

    print("All test cases passed!")


def demonstrate_edge_cases():
    """Demonstrate important edge cases."""

    print("\n=== Edge Cases Demonstration ===\n")

    # Edge case 1: Empty-like (single pair)
    s = "()"
    print(f"Single pair '{s}': {is_valid(s)}")
    print("- Simplest valid case\n")

    # Edge case 2: Wrong order
    s = "([)]"
    print(f"Wrong order '{s}': {is_valid(s)}")
    print("- Opens ( then [, but closes ) before ]\n")

    # Edge case 3: Unmatched opening
    s = "((("
    print(f"Unmatched opening '{s}': {is_valid(s)}")
    print("- Stack not empty at end\n")

    # Edge case 4: Unmatched closing
    s = ")))"
    print(f"Unmatched closing '{s}': {is_valid(s)}")
    print("- Trying to pop from empty stack\n")

    # Edge case 5: Correct nesting
    s = "{[()]}"
    print(f"Correct nesting '{s}': {is_valid(s)}")
    print("- Each bracket closes in reverse order opened\n")


def visualize_stack_operations(s):
    """Visualize how the stack changes for a given string."""

    print(f"\n=== Stack Operations for '{s}' ===\n")

    matching = {'(': ')', '[': ']', '{': '}'}
    stack = []

    for i, char in enumerate(s):
        print(f"Step {i+1}: Processing '{char}'")

        if char in matching:
            stack.append(char)
            print(f"  Opening bracket -> Push to stack")
        else:
            if not stack:
                print(f"  Closing bracket but stack is empty -> INVALID")
                return False

            opening = stack.pop()
            if matching[opening] != char:
                print(f"  Mismatch: '{opening}' vs '{char}' -> INVALID")
                return False

            print(f"  Closing bracket matches '{opening}' -> Pop from stack")

        print(f"  Stack: {stack if stack else '(empty)'}")
        print()

    if stack:
        print(f"Final check: Stack not empty {stack} -> INVALID")
        return False
    else:
        print(f"Final check: Stack empty -> VALID")
        return True


if __name__ == "__main__":
    # Run tests
    test_valid_parentheses()

    # Demonstrate edge cases
    demonstrate_edge_cases()

    # Visualize some examples
    print("\n" + "="*50)
    visualize_stack_operations("()[]{}")

    print("\n" + "="*50)
    visualize_stack_operations("([)]")

    print("\n" + "="*50)
    visualize_stack_operations("{[]}")
