"""
Lowest Common Ancestor of a Binary Tree (LeetCode #236)

Problem:
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes.

According to the definition of LCA: "The lowest common ancestor is defined
between two nodes p and q as the lowest node in T that has both p and q as
descendants (where we allow a node to be a descendant of itself)."

Example 1:
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
          3
         / \
        5   1
       / \ / \
      6  2 0  8
        / \
       7   4
Output: 3
Explanation: The LCA of nodes 5 and 1 is 3.

Example 2:
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
Output: 5
Explanation: The LCA of nodes 5 and 4 is 5, since a node can be a
descendant of itself.

Example 3:
Input: root = [1,2], p = 1, q = 2
Output: 1

Constraints:
- The number of nodes in the tree is in the range [2, 10^5]
- -10^9 <= Node.val <= 10^9
- All Node.val are unique
- p != q
- p and q exist in the tree
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lca_binary_tree(root, p, q):
    """
    Recursive approach for general binary tree - optimal solution.

    Approach:
    1. Base case: if root is None or equals p or q, return root
    2. Recursively find LCA in left and right subtrees
    3. If both sides return non-None, current node is LCA
    4. Otherwise, return whichever side found a node

    Key insights:
    - If we find p or q, we return it immediately
    - If left returns p and right returns q (or vice versa), current is LCA
    - If only one side returns a node, that side contains both p and q

    This is an elegant bottom-up approach that builds the answer
    as we return from recursion.

    Time Complexity: O(n) - may need to visit all nodes
    Space Complexity: O(h) - recursion stack where h is height

    Args:
        root: Root of binary tree
        p: First node
        q: Second node

    Returns:
        TreeNode representing the LCA
    """
    # Base case: empty tree or found one of the target nodes
    if not root or root == p or root == q:
        return root

    # Search in left and right subtrees
    left = lca_binary_tree(root.left, p, q)
    right = lca_binary_tree(root.right, p, q)

    # If both sides found nodes, current node is LCA
    if left and right:
        return root

    # Otherwise return whichever side found a node
    # (or None if neither found anything)
    return left if left else right


def lca_bst(root, p, q):
    """
    Optimized approach for Binary Search Tree.

    For BST, we can use the ordering property to avoid searching both subtrees!

    Approach:
    1. If both p and q are smaller than root, LCA is in left subtree
    2. If both p and q are larger than root, LCA is in right subtree
    3. Otherwise, root is the split point and thus the LCA

    This is much more efficient as we only explore one path down the tree.

    Time Complexity: O(h) - only traverse one path, where h is height
                     O(log n) for balanced tree, O(n) for skewed
    Space Complexity: O(1) - iterative solution uses constant space

    Args:
        root: Root of BST
        p: First node
        q: Second node

    Returns:
        TreeNode representing the LCA
    """
    # Ensure p has smaller value for easier comparison
    if p.val > q.val:
        p, q = q, p

    current = root

    while current:
        # Both nodes in left subtree
        if current.val > q.val:
            current = current.left
        # Both nodes in right subtree
        elif current.val < p.val:
            current = current.right
        # Split point found - this is LCA
        else:
            return current

    return None


def lca_with_parent_pointers(p, q):
    """
    Alternative approach if nodes have parent pointers.

    Approach:
    1. Traverse from p to root, storing all ancestors in a set
    2. Traverse from q to root, return first node found in set

    This is like finding the intersection point of two linked lists!

    Time Complexity: O(h) - traverse at most height twice
    Space Complexity: O(h) - store ancestors in set

    Args:
        p: First node (with parent pointer)
        q: Second node (with parent pointer)

    Returns:
        TreeNode representing the LCA

    Note: This assumes nodes have a 'parent' attribute
    """
    # Store all ancestors of p
    ancestors = set()
    current = p
    while current:
        ancestors.add(current)
        current = current.parent

    # Find first ancestor of q that's also an ancestor of p
    current = q
    while current:
        if current in ancestors:
            return current
        current = current.parent

    return None


def lca_with_paths(root, p, q):
    """
    Approach using paths from root to each node.

    Approach:
    1. Find path from root to p
    2. Find path from root to q
    3. Compare paths to find last common node

    Time Complexity: O(n) - find both paths
    Space Complexity: O(h) - store paths

    Args:
        root: Root of binary tree
        p: First node
        q: Second node

    Returns:
        TreeNode representing the LCA
    """

    def find_path(root, target, path):
        """Find path from root to target node."""
        if not root:
            return False

        path.append(root)

        if root == target:
            return True

        if find_path(root.left, target, path) or find_path(root.right, target, path):
            return True

        path.pop()
        return False

    # Find paths to both nodes
    path_p = []
    path_q = []

    find_path(root, p, path_p)
    find_path(root, q, path_q)

    # Find last common node in paths
    lca = None
    for i in range(min(len(path_p), len(path_q))):
        if path_p[i] == path_q[i]:
            lca = path_p[i]
        else:
            break

    return lca


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


def find_node(root, val):
    """Find node with given value in tree."""
    if not root:
        return None
    if root.val == val:
        return root

    left = find_node(root.left, val)
    if left:
        return left

    return find_node(root.right, val)


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


def test_lca():
    """Test cases covering various scenarios."""

    # Test case 1: Example tree from problem
    root1 = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    p1 = find_node(root1, 5)
    q1 = find_node(root1, 1)
    assert lca_binary_tree(root1, p1, q1).val == 3
    assert lca_with_paths(root1, p1, q1).val == 3

    # Test case 2: One node is ancestor of the other
    p2 = find_node(root1, 5)
    q2 = find_node(root1, 4)
    assert lca_binary_tree(root1, p2, q2).val == 5
    assert lca_with_paths(root1, p2, q2).val == 5

    # Test case 3: Simple tree [1,2]
    root3 = build_tree([1, 2])
    p3 = find_node(root3, 1)
    q3 = find_node(root3, 2)
    assert lca_binary_tree(root3, p3, q3).val == 1
    assert lca_with_paths(root3, p3, q3).val == 1

    # Test case 4: Nodes at same level
    root4 = build_tree([3, 5, 1, 6, 2, 0, 8])
    p4 = find_node(root4, 6)
    q4 = find_node(root4, 2)
    assert lca_binary_tree(root4, p4, q4).val == 5
    assert lca_with_paths(root4, p4, q4).val == 5

    # Test case 5: Nodes in different subtrees at different levels
    p5 = find_node(root4, 6)
    q5 = find_node(root4, 0)
    assert lca_binary_tree(root4, p5, q5).val == 3
    assert lca_with_paths(root4, p5, q5).val == 3

    # Test case 6: BST example
    bst = TreeNode(6)
    bst.left = TreeNode(2)
    bst.right = TreeNode(8)
    bst.left.left = TreeNode(0)
    bst.left.right = TreeNode(4)
    bst.left.right.left = TreeNode(3)
    bst.left.right.right = TreeNode(5)
    bst.right.left = TreeNode(7)
    bst.right.right = TreeNode(9)

    p6 = find_node(bst, 2)
    q6 = find_node(bst, 8)
    assert lca_bst(bst, p6, q6).val == 6
    assert lca_binary_tree(bst, p6, q6).val == 6

    p7 = find_node(bst, 2)
    q7 = find_node(bst, 4)
    assert lca_bst(bst, p7, q7).val == 2
    assert lca_binary_tree(bst, p7, q7).val == 2

    print("All test cases passed!")


if __name__ == "__main__":
    test_lca()

    # Example usage with visualization
    print("\nExample 1: LCA in Binary Tree")
    print("=" * 50)

    root = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    visualize_tree(root)

    p = find_node(root, 5)
    q = find_node(root, 1)
    lca_node = lca_binary_tree(root, p, q)
    print(f"\nLCA of {p.val} and {q.val}: {lca_node.val}")

    p = find_node(root, 5)
    q = find_node(root, 4)
    lca_node = lca_binary_tree(root, p, q)
    print(f"LCA of {p.val} and {q.val}: {lca_node.val}")
    print("(Node 5 is ancestor of itself)")

    # BST example
    print("\n" + "=" * 50)
    print("Example 2: LCA in Binary Search Tree")
    print("=" * 50)

    bst = TreeNode(6)
    bst.left = TreeNode(2)
    bst.right = TreeNode(8)
    bst.left.left = TreeNode(0)
    bst.left.right = TreeNode(4)
    bst.left.right.left = TreeNode(3)
    bst.left.right.right = TreeNode(5)
    bst.right.left = TreeNode(7)
    bst.right.right = TreeNode(9)

    visualize_tree(bst)

    p = find_node(bst, 2)
    q = find_node(bst, 8)
    lca_node = lca_bst(bst, p, q)
    print(f"\nLCA of {p.val} and {q.val} (using BST property): {lca_node.val}")

    p = find_node(bst, 2)
    q = find_node(bst, 4)
    lca_node = lca_bst(bst, p, q)
    print(f"LCA of {p.val} and {q.val} (using BST property): {lca_node.val}")

    print("\nNote: BST approach is O(h) vs O(n) for general binary tree!")
