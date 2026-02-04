"""
Validate Binary Search Tree (LeetCode #98)

Problem:
Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys less than the node's key
- The right subtree of a node contains only nodes with keys greater than the node's key
- Both the left and right subtrees must also be binary search trees

Example 1:
Input: root = [2,1,3]
      2
     / \
    1   3
Output: true

Example 2:
Input: root = [5,1,4,null,null,3,6]
      5
     / \
    1   4
       / \
      3   6
Output: false
Explanation: The root node's value is 5 but its right child's value is 4.

Example 3:
Input: root = [5,4,6,null,null,3,7]
      5
     / \
    4   6
       / \
      3   7
Output: false
Explanation: The node with value 3 is in the right subtree of 5,
but 3 < 5, violating BST property.

Constraints:
- The number of nodes in the tree is in the range [1, 10^4]
- -2^31 <= Node.val <= 2^31 - 1
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_valid_bst_bounds(root, min_val=float('-inf'), max_val=float('inf')):
    """
    Recursive approach with min/max bounds - optimal solution.

    Approach:
    1. For each node, track valid range [min_val, max_val]
    2. Node value must be within this range
    3. Left child gets range [min_val, node.val)
    4. Right child gets range (node.val, max_val]

    This is the key insight: we need to track constraints from ALL
    ancestors, not just the immediate parent!

    Example why we need bounds:
          5
         / \
        1   6
           / \
          3   7
    The node 3 is in right subtree of 6, but also right of 5.
    It must satisfy 3 > 5 (from being right of 5) AND 3 < 6 (from being left of 6).
    Without bounds, we'd only check against parent 6.

    Time Complexity: O(n) - visit each node once
    Space Complexity: O(h) - recursion stack where h is height

    Args:
        root: Root node of binary tree
        min_val: Minimum valid value for current node
        max_val: Maximum valid value for current node

    Returns:
        Boolean indicating if tree is valid BST
    """
    if not root:
        return True

    # Check if current node violates bounds
    if root.val <= min_val or root.val >= max_val:
        return False

    # Check left subtree (must be < root.val)
    # and right subtree (must be > root.val)
    return (is_valid_bst_bounds(root.left, min_val, root.val) and
            is_valid_bst_bounds(root.right, root.val, max_val))


def is_valid_bst_inorder(root):
    """
    Inorder traversal approach - uses BST property.

    Key insight: Inorder traversal of BST gives sorted sequence!
    So if inorder traversal is strictly increasing, it's a valid BST.

    Approach:
    1. Perform inorder traversal (left -> root -> right)
    2. Track previous value seen
    3. Each value must be greater than previous
    4. If any value <= previous, not a valid BST

    Time Complexity: O(n) - visit each node once
    Space Complexity: O(h) - recursion stack

    Args:
        root: Root node of binary tree

    Returns:
        Boolean indicating if tree is valid BST
    """
    prev = [float('-inf')]  # Use list to allow modification in nested function

    def inorder(node):
        if not node:
            return True

        # Check left subtree
        if not inorder(node.left):
            return False

        # Check current node
        if node.val <= prev[0]:
            return False
        prev[0] = node.val

        # Check right subtree
        return inorder(node.right)

    return inorder(root)


def is_valid_bst_inorder_iterative(root):
    """
    Iterative inorder traversal approach.

    Same logic as recursive inorder, but using explicit stack.
    Good for showing mastery of both recursive and iterative patterns.

    Time Complexity: O(n)
    Space Complexity: O(h)

    Args:
        root: Root node of binary tree

    Returns:
        Boolean indicating if tree is valid BST
    """
    stack = []
    prev = float('-inf')
    current = root

    while current or stack:
        # Go to leftmost node
        while current:
            stack.append(current)
            current = current.left

        # Process node
        current = stack.pop()

        # Check if values are strictly increasing
        if current.val <= prev:
            return False

        prev = current.val
        current = current.right

    return True


def is_valid_bst_wrong(root):
    """
    Common WRONG approach - only compares with immediate children.

    This doesn't work because it doesn't check constraints from all ancestors!

    Example where this fails:
          5
         / \
        1   6
           / \
          3   7

    This would incorrectly return True because:
    - 5 > 1 and 5 < 6 ✓
    - 6 > 3 and 6 < 7 ✓

    But it's invalid because 3 < 5 (node 3 is in right subtree of 5).

    This is included to show a common mistake!

    Args:
        root: Root node of binary tree

    Returns:
        Boolean (INCORRECT for some cases)
    """
    if not root:
        return True

    # Only checks immediate children - WRONG!
    if root.left and root.left.val >= root.val:
        return False
    if root.right and root.right.val <= root.val:
        return False

    return (is_valid_bst_wrong(root.left) and
            is_valid_bst_wrong(root.right))


# Helper functions for testing
def build_tree(values):
    """Build tree from level-order list (None represents missing node)."""
    if not values:
        return None

    from collections import deque

    root = TreeNode(values[0])
    queue = deque([root])
    i = 1

    while queue and i < len(values):
        node = queue.popleft()

        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1

        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root


def visualize_tree(root, level=0, prefix="Root: "):
    """Print tree structure for visualization."""
    if not root:
        return

    print(" " * (level * 4) + prefix + str(root.val))

    if root.left or root.right:
        if root.left:
            visualize_tree(root.left, level + 1, "L--- ")
        else:
            print(" " * ((level + 1) * 4) + "L--- None")

        if root.right:
            visualize_tree(root.right, level + 1, "R--- ")
        else:
            print(" " * ((level + 1) * 4) + "R--- None")


def test_is_valid_bst():
    """Test cases covering various scenarios."""

    # Test case 1: Valid BST [2,1,3]
    root1 = build_tree([2, 1, 3])
    assert is_valid_bst_bounds(root1) == True
    assert is_valid_bst_inorder(root1) == True
    assert is_valid_bst_inorder_iterative(root1) == True

    # Test case 2: Invalid BST [5,1,4,null,null,3,6]
    root2 = build_tree([5, 1, 4, None, None, 3, 6])
    assert is_valid_bst_bounds(root2) == False
    assert is_valid_bst_inorder(root2) == False
    assert is_valid_bst_inorder_iterative(root2) == False

    # Test case 3: Single node
    root3 = TreeNode(1)
    assert is_valid_bst_bounds(root3) == True
    assert is_valid_bst_inorder(root3) == True
    assert is_valid_bst_inorder_iterative(root3) == True

    # Test case 4: Valid complete BST
    root4 = TreeNode(4)
    root4.left = TreeNode(2)
    root4.right = TreeNode(6)
    root4.left.left = TreeNode(1)
    root4.left.right = TreeNode(3)
    root4.right.left = TreeNode(5)
    root4.right.right = TreeNode(7)
    assert is_valid_bst_bounds(root4) == True
    assert is_valid_bst_inorder(root4) == True
    assert is_valid_bst_inorder_iterative(root4) == True

    # Test case 5: Invalid - duplicate values
    root5 = TreeNode(2)
    root5.left = TreeNode(2)
    root5.right = TreeNode(2)
    assert is_valid_bst_bounds(root5) == False
    assert is_valid_bst_inorder(root5) == False
    assert is_valid_bst_inorder_iterative(root5) == False

    # Test case 6: Tricky invalid case [5,4,6,null,null,3,7]
    # Node 3 is in right subtree of 5 but 3 < 5
    root6 = build_tree([5, 4, 6, None, None, 3, 7])
    assert is_valid_bst_bounds(root6) == False
    assert is_valid_bst_inorder(root6) == False
    assert is_valid_bst_inorder_iterative(root6) == False
    # Wrong approach incorrectly returns True for this!
    assert is_valid_bst_wrong(root6) == True  # WRONG!

    # Test case 7: Another tricky case [10,5,15,null,null,6,20]
    root7 = build_tree([10, 5, 15, None, None, 6, 20])
    assert is_valid_bst_bounds(root7) == False
    assert is_valid_bst_inorder(root7) == False
    assert is_valid_bst_inorder_iterative(root7) == False

    # Test case 8: Left-skewed valid BST
    root8 = TreeNode(5)
    root8.left = TreeNode(4)
    root8.left.left = TreeNode(3)
    root8.left.left.left = TreeNode(2)
    assert is_valid_bst_bounds(root8) == True
    assert is_valid_bst_inorder(root8) == True
    assert is_valid_bst_inorder_iterative(root8) == True

    # Test case 9: Right-skewed valid BST
    root9 = TreeNode(1)
    root9.right = TreeNode(2)
    root9.right.right = TreeNode(3)
    root9.right.right.right = TreeNode(4)
    assert is_valid_bst_bounds(root9) == True
    assert is_valid_bst_inorder(root9) == True
    assert is_valid_bst_inorder_iterative(root9) == True

    # Test case 10: Negative numbers
    root10 = TreeNode(0)
    root10.left = TreeNode(-1)
    root10.right = TreeNode(1)
    assert is_valid_bst_bounds(root10) == True
    assert is_valid_bst_inorder(root10) == True
    assert is_valid_bst_inorder_iterative(root10) == True

    print("All test cases passed!")


if __name__ == "__main__":
    test_is_valid_bst()

    # Example usage with visualization
    print("\nExample 1: Valid BST")
    print("=" * 50)
    root1 = build_tree([2, 1, 3])
    visualize_tree(root1)
    print(f"Is valid BST: {is_valid_bst_bounds(root1)}")

    print("\n" + "=" * 50)
    print("Example 2: Invalid BST")
    print("=" * 50)
    root2 = build_tree([5, 1, 4, None, None, 3, 6])
    visualize_tree(root2)
    print(f"Is valid BST: {is_valid_bst_bounds(root2)}")
    print("Why invalid: Node 4 < 5, but 4 is in right subtree")

    print("\n" + "=" * 50)
    print("Example 3: Tricky Invalid BST")
    print("=" * 50)
    root3 = build_tree([5, 4, 6, None, None, 3, 7])
    visualize_tree(root3)
    print(f"Is valid BST: {is_valid_bst_bounds(root3)}")
    print(f"Wrong approach says: {is_valid_bst_wrong(root3)}")
    print("Why invalid: Node 3 is in right subtree of 5, but 3 < 5")
    print("This shows why we need to track bounds from ALL ancestors!")

    print("\n" + "=" * 50)
    print("Example 4: Valid Complete BST")
    print("=" * 50)
    root4 = TreeNode(4)
    root4.left = TreeNode(2)
    root4.right = TreeNode(6)
    root4.left.left = TreeNode(1)
    root4.left.right = TreeNode(3)
    root4.right.left = TreeNode(5)
    root4.right.right = TreeNode(7)
    visualize_tree(root4)
    print(f"Is valid BST: {is_valid_bst_bounds(root4)}")
    print("Inorder traversal (should be sorted): ", end="")

    def print_inorder(node):
        if node:
            print_inorder(node.left)
            print(node.val, end=" ")
            print_inorder(node.right)

    print_inorder(root4)
    print()
