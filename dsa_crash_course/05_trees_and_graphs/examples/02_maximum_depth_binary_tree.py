"""
Maximum Depth of Binary Tree (LeetCode #104)

Problem:
Given the root of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path
from the root node down to the farthest leaf node.

Example 1:
Input: root = [3,9,20,null,null,15,7]
        3
       / \
      9  20
         / \
        15  7
Output: 3

Example 2:
Input: root = [1,null,2]
Output: 2

Example 3:
Input: root = []
Output: 0

Example 4:
Input: root = [0]
Output: 1

Constraints:
- The number of nodes in the tree is in the range [0, 10^4]
- -100 <= Node.val <= 100
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth_recursive(root):
    """
    Recursive DFS approach - most intuitive solution.

    Approach:
    1. Base case: empty tree has depth 0
    2. Recursive case: depth = 1 + max(left_depth, right_depth)
    3. The +1 accounts for the current node

    This is a classic example of bottom-up recursion where we
    build the answer from the leaves upward.

    Time Complexity: O(n) - visit each node exactly once
    Space Complexity: O(h) - recursion stack where h is height
                      O(n) worst case for skewed tree
                      O(log n) for balanced tree

    Args:
        root: Root node of binary tree

    Returns:
        Integer representing maximum depth
    """
    if not root:
        return 0

    left_depth = max_depth_recursive(root.left)
    right_depth = max_depth_recursive(root.right)

    return 1 + max(left_depth, right_depth)


def max_depth_iterative_dfs(root):
    """
    Iterative DFS approach using stack.

    Approach:
    1. Use stack to store (node, depth) pairs
    2. Track maximum depth seen so far
    3. For each node, push children with incremented depth

    Time Complexity: O(n) - visit each node once
    Space Complexity: O(h) - stack size proportional to height

    Args:
        root: Root node of binary tree

    Returns:
        Integer representing maximum depth
    """
    if not root:
        return 0

    stack = [(root, 1)]
    max_depth = 0

    while stack:
        node, depth = stack.pop()
        max_depth = max(max_depth, depth)

        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))

    return max_depth


def max_depth_bfs(root):
    """
    BFS (Level Order) approach using queue.

    Approach:
    1. Process tree level by level
    2. Count the number of levels
    3. Number of levels = maximum depth

    This is particularly intuitive because we literally count
    how many levels deep the tree goes.

    Time Complexity: O(n) - visit each node once
    Space Complexity: O(w) - queue size, where w is max width
                      O(n) worst case for complete tree
                      (last level can have n/2 nodes)

    Args:
        root: Root node of binary tree

    Returns:
        Integer representing maximum depth
    """
    if not root:
        return 0

    from collections import deque

    queue = deque([root])
    depth = 0

    while queue:
        depth += 1
        level_size = len(queue)

        # Process all nodes at current level
        for _ in range(level_size):
            node = queue.popleft()

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return depth


def max_depth_one_liner(root):
    """
    Pythonic one-liner solution.

    This is essentially the recursive solution but compressed.
    While elegant, prefer the explicit version in interviews
    for clarity and discussion.

    Time Complexity: O(n)
    Space Complexity: O(h)

    Args:
        root: Root node of binary tree

    Returns:
        Integer representing maximum depth
    """
    return 1 + max(max_depth_one_liner(root.left), max_depth_one_liner(root.right)) if root else 0


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


def test_max_depth():
    """Test cases covering various scenarios."""

    # Test case 1: Example tree [3,9,20,null,null,15,7]
    root1 = build_tree([3, 9, 20, None, None, 15, 7])
    expected1 = 3

    assert max_depth_recursive(root1) == expected1
    assert max_depth_iterative_dfs(root1) == expected1
    assert max_depth_bfs(root1) == expected1
    assert max_depth_one_liner(root1) == expected1

    # Test case 2: Two nodes [1,null,2]
    root2 = build_tree([1, None, 2])
    expected2 = 2

    assert max_depth_recursive(root2) == expected2
    assert max_depth_iterative_dfs(root2) == expected2
    assert max_depth_bfs(root2) == expected2
    assert max_depth_one_liner(root2) == expected2

    # Test case 3: Empty tree
    root3 = None
    expected3 = 0

    assert max_depth_recursive(root3) == expected3
    assert max_depth_iterative_dfs(root3) == expected3
    assert max_depth_bfs(root3) == expected3
    assert max_depth_one_liner(root3) == expected3

    # Test case 4: Single node
    root4 = TreeNode(0)
    expected4 = 1

    assert max_depth_recursive(root4) == expected4
    assert max_depth_iterative_dfs(root4) == expected4
    assert max_depth_bfs(root4) == expected4
    assert max_depth_one_liner(root4) == expected4

    # Test case 5: Left-skewed tree (worst case)
    root5 = TreeNode(1)
    root5.left = TreeNode(2)
    root5.left.left = TreeNode(3)
    root5.left.left.left = TreeNode(4)
    root5.left.left.left.left = TreeNode(5)
    expected5 = 5

    assert max_depth_recursive(root5) == expected5
    assert max_depth_iterative_dfs(root5) == expected5
    assert max_depth_bfs(root5) == expected5
    assert max_depth_one_liner(root5) == expected5

    # Test case 6: Right-skewed tree
    root6 = TreeNode(1)
    root6.right = TreeNode(2)
    root6.right.right = TreeNode(3)
    expected6 = 3

    assert max_depth_recursive(root6) == expected6
    assert max_depth_iterative_dfs(root6) == expected6
    assert max_depth_bfs(root6) == expected6
    assert max_depth_one_liner(root6) == expected6

    # Test case 7: Complete binary tree
    root7 = build_tree([1, 2, 3, 4, 5, 6, 7])
    expected7 = 3

    assert max_depth_recursive(root7) == expected7
    assert max_depth_iterative_dfs(root7) == expected7
    assert max_depth_bfs(root7) == expected7
    assert max_depth_one_liner(root7) == expected7

    # Test case 8: Unbalanced tree
    root8 = build_tree([1, 2, 3, 4, None, None, 5, 6, None, None, 7])
    expected8 = 4

    assert max_depth_recursive(root8) == expected8
    assert max_depth_iterative_dfs(root8) == expected8
    assert max_depth_bfs(root8) == expected8
    assert max_depth_one_liner(root8) == expected8

    print("All test cases passed!")


if __name__ == "__main__":
    test_max_depth()

    # Example usage with visualization
    print("\nExample: Maximum Depth of Binary Tree")
    print("=" * 50)

    # Create example tree: [3,9,20,null,null,15,7]
    root = build_tree([3, 9, 20, None, None, 15, 7])

    print("\nTree structure:")
    visualize_tree(root)

    print(f"\nMaximum depth (recursive): {max_depth_recursive(root)}")
    print(f"Maximum depth (iterative DFS): {max_depth_iterative_dfs(root)}")
    print(f"Maximum depth (BFS): {max_depth_bfs(root)}")
    print(f"Maximum depth (one-liner): {max_depth_one_liner(root)}")

    # Different tree shapes
    print("\n" + "=" * 50)
    print("Comparison: Different Tree Shapes")
    print("=" * 50)

    # Balanced tree
    balanced = build_tree([1, 2, 3, 4, 5, 6, 7])
    print("\nBalanced tree (7 nodes):")
    visualize_tree(balanced)
    print(f"Depth: {max_depth_recursive(balanced)}")

    # Skewed tree
    skewed = TreeNode(1)
    skewed.left = TreeNode(2)
    skewed.left.left = TreeNode(3)
    skewed.left.left.left = TreeNode(4)
    print("\nLeft-skewed tree (4 nodes):")
    visualize_tree(skewed)
    print(f"Depth: {max_depth_recursive(skewed)}")

    print("\nNote: Balanced trees have log(n) depth,")
    print("      skewed trees have n depth (worst case)")
