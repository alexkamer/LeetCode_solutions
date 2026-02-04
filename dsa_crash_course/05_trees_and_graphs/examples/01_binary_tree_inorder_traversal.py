"""
Binary Tree Inorder Traversal (LeetCode #94)

Problem:
Given the root of a binary tree, return the inorder traversal of its nodes' values.

Inorder traversal visits nodes in the order: Left -> Root -> Right
For a BST, this gives values in sorted order.

Example 1:
Input: root = [1,null,2,3]
        1
         \
          2
         /
        3
Output: [1,3,2]

Example 2:
Input: root = []
Output: []

Example 3:
Input: root = [1]
Output: [1]

Constraints:
- The number of nodes in the tree is in the range [0, 100]
- -100 <= Node.val <= 100

Follow up: Recursive solution is trivial, could you do it iteratively?
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def inorder_traversal_recursive(root):
    """
    Recursive approach - most natural and intuitive.

    Approach:
    1. Recursively traverse left subtree
    2. Visit current node
    3. Recursively traverse right subtree

    For BST, this produces values in sorted order!

    Time Complexity: O(n) - visit each node exactly once
    Space Complexity: O(h) - recursion stack, where h is height
                      O(n) worst case for skewed tree
                      O(log n) for balanced tree

    Args:
        root: Root node of binary tree

    Returns:
        List of node values in inorder sequence
    """
    if not root:
        return []

    result = []

    # Left -> Root -> Right
    result.extend(inorder_traversal_recursive(root.left))
    result.append(root.val)
    result.extend(inorder_traversal_recursive(root.right))

    return result


def inorder_traversal_iterative(root):
    """
    Iterative approach using explicit stack.

    Approach:
    1. Use stack to simulate recursion
    2. Go as far left as possible, pushing nodes onto stack
    3. When can't go left, pop node, process it, go right
    4. Repeat until stack is empty and no more nodes

    This is the standard iterative DFS pattern for inorder traversal.

    Time Complexity: O(n) - visit each node once
    Space Complexity: O(h) - stack size proportional to tree height

    Args:
        root: Root node of binary tree

    Returns:
        List of node values in inorder sequence
    """
    result = []
    stack = []
    current = root

    while current or stack:
        # Go to the leftmost node
        while current:
            stack.append(current)
            current = current.left

        # Current is None, so we've reached leftmost
        # Pop node from stack and process it
        current = stack.pop()
        result.append(current.val)

        # Now try the right subtree
        current = current.right

    return result


def inorder_traversal_morris(root):
    """
    Morris traversal - O(1) space complexity!

    Approach:
    Uses threading to traverse without stack or recursion.
    1. For each node, find its inorder predecessor
    2. Create temporary thread from predecessor to current
    3. Use thread to get back to current after left subtree
    4. Remove threads as we process nodes

    This is advanced but impressive in interviews for space optimization.

    Time Complexity: O(n) - although we visit some nodes multiple times,
                     amortized time is O(n)
    Space Complexity: O(1) - no stack or recursion!

    Args:
        root: Root node of binary tree

    Returns:
        List of node values in inorder sequence
    """
    result = []
    current = root

    while current:
        if not current.left:
            # No left subtree, process current and go right
            result.append(current.val)
            current = current.right
        else:
            # Find inorder predecessor (rightmost node in left subtree)
            predecessor = current.left
            while predecessor.right and predecessor.right != current:
                predecessor = predecessor.right

            if not predecessor.right:
                # Create thread from predecessor to current
                predecessor.right = current
                current = current.left
            else:
                # Thread exists, we've processed left subtree
                # Remove thread and process current
                predecessor.right = None
                result.append(current.val)
                current = current.right

    return result


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


def test_inorder_traversal():
    """Test cases covering various scenarios."""

    # Test case 1: Example tree [1,null,2,3]
    root1 = TreeNode(1)
    root1.right = TreeNode(2)
    root1.right.left = TreeNode(3)
    expected1 = [1, 3, 2]

    assert inorder_traversal_recursive(root1) == expected1
    assert inorder_traversal_iterative(root1) == expected1
    assert inorder_traversal_morris(root1) == expected1

    # Test case 2: Empty tree
    root2 = None
    expected2 = []

    assert inorder_traversal_recursive(root2) == expected2
    assert inorder_traversal_iterative(root2) == expected2
    assert inorder_traversal_morris(root2) == expected2

    # Test case 3: Single node
    root3 = TreeNode(1)
    expected3 = [1]

    assert inorder_traversal_recursive(root3) == expected3
    assert inorder_traversal_iterative(root3) == expected3
    assert inorder_traversal_morris(root3) == expected3

    # Test case 4: Complete tree
    root4 = build_tree([1, 2, 3, 4, 5, 6, 7])
    expected4 = [4, 2, 5, 1, 6, 3, 7]

    assert inorder_traversal_recursive(root4) == expected4
    assert inorder_traversal_iterative(root4) == expected4
    assert inorder_traversal_morris(root4) == expected4

    # Test case 5: Left-skewed tree
    root5 = TreeNode(5)
    root5.left = TreeNode(4)
    root5.left.left = TreeNode(3)
    root5.left.left.left = TreeNode(2)
    root5.left.left.left.left = TreeNode(1)
    expected5 = [1, 2, 3, 4, 5]

    assert inorder_traversal_recursive(root5) == expected5
    assert inorder_traversal_iterative(root5) == expected5
    assert inorder_traversal_morris(root5) == expected5

    # Test case 6: Right-skewed tree
    root6 = TreeNode(1)
    root6.right = TreeNode(2)
    root6.right.right = TreeNode(3)
    root6.right.right.right = TreeNode(4)
    expected6 = [1, 2, 3, 4]

    assert inorder_traversal_recursive(root6) == expected6
    assert inorder_traversal_iterative(root6) == expected6
    assert inorder_traversal_morris(root6) == expected6

    # Test case 7: BST (should give sorted order)
    root7 = TreeNode(5)
    root7.left = TreeNode(3)
    root7.right = TreeNode(7)
    root7.left.left = TreeNode(1)
    root7.left.right = TreeNode(4)
    root7.right.left = TreeNode(6)
    root7.right.right = TreeNode(9)
    expected7 = [1, 3, 4, 5, 6, 7, 9]

    assert inorder_traversal_recursive(root7) == expected7
    assert inorder_traversal_iterative(root7) == expected7
    assert inorder_traversal_morris(root7) == expected7

    print("All test cases passed!")


if __name__ == "__main__":
    test_inorder_traversal()

    # Example usage with visualization
    print("\nExample: Binary Tree Inorder Traversal")
    print("=" * 50)

    # Create example tree: [1,null,2,3]
    root = TreeNode(1)
    root.right = TreeNode(2)
    root.right.left = TreeNode(3)

    print("\nTree structure:")
    visualize_tree(root)

    print("\nInorder traversal (recursive):", inorder_traversal_recursive(root))
    print("Inorder traversal (iterative):", inorder_traversal_iterative(root))
    print("Inorder traversal (Morris):", inorder_traversal_morris(root))

    # Create a BST to show sorted order
    print("\n" + "=" * 50)
    print("BST Example (inorder gives sorted values):")
    print("=" * 50)

    bst = TreeNode(5)
    bst.left = TreeNode(3)
    bst.right = TreeNode(7)
    bst.left.left = TreeNode(1)
    bst.left.right = TreeNode(4)
    bst.right.left = TreeNode(6)
    bst.right.right = TreeNode(9)

    print("\nBST structure:")
    visualize_tree(bst)

    print("\nInorder traversal:", inorder_traversal_recursive(bst))
    print("Notice: Values are in sorted order!")
