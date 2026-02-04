# Trees and Graphs

Trees and graphs are fundamental hierarchical and networked data structures that appear frequently in coding interviews. They model relationships, hierarchies, and connections between entities.

## 📖 What Are Trees?

A **tree** is a hierarchical data structure consisting of nodes connected by edges, with one node designated as the root. Each node can have zero or more children, and there are no cycles.

### Key Properties

- **Root** - The topmost node with no parent
- **Parent/Child** - Nodes connected by edges (parent above, children below)
- **Leaf** - A node with no children
- **Height** - Length of longest path from root to leaf
- **Depth** - Length of path from root to a specific node
- **Subtree** - A node and all its descendants

### Tree Terminology

```
         1          <- Root (height = 3, depth = 0)
        / \
       2   3        <- Internal nodes (depth = 1)
      / \   \
     4   5   6      <- Leaves (depth = 2)
    /
   7                <- Leaf (depth = 3)
```

## 🌳 Binary Trees

A **binary tree** is a tree where each node has at most two children (left and right).

### Types of Binary Trees

**1. Full Binary Tree**
- Every node has 0 or 2 children (no node has only 1 child)

```
     1
    / \
   2   3
  / \
 4   5
```

**2. Complete Binary Tree**
- All levels filled except possibly the last
- Last level filled from left to right
- Used in heaps!

```
     1
    / \
   2   3
  / \  /
 4  5 6
```

**3. Perfect Binary Tree**
- All internal nodes have 2 children
- All leaves at same level
- Total nodes = 2^(h+1) - 1

```
     1
    / \
   2   3
  / \ / \
 4  5 6  7
```

**4. Balanced Binary Tree**
- Height difference between left and right subtrees is at most 1
- Ensures O(log n) operations

### Binary Tree Implementation

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Creating a simple tree
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)
```

## 🔍 Binary Search Trees (BST)

A **Binary Search Tree** is a binary tree with the ordering property:
- All values in left subtree < node value
- All values in right subtree > node value
- Both subtrees are also BSTs

```
      8
     / \
    3   10
   / \    \
  1   6    14
     / \   /
    4   7 13
```

### BST Operations

```python
class BST:
    def search(self, root, target):
        """Search for a value in BST."""
        if not root or root.val == target:
            return root

        if target < root.val:
            return self.search(root.left, target)
        else:
            return self.search(root.right, target)

    def insert(self, root, val):
        """Insert a value into BST."""
        if not root:
            return TreeNode(val)

        if val < root.val:
            root.left = self.insert(root.left, val)
        else:
            root.right = self.insert(root.right, val)

        return root

    def find_min(self, root):
        """Find minimum value (leftmost node)."""
        while root.left:
            root = root.left
        return root

    def delete(self, root, val):
        """Delete a value from BST."""
        if not root:
            return None

        if val < root.val:
            root.left = self.delete(root.left, val)
        elif val > root.val:
            root.right = self.delete(root.right, val)
        else:
            # Found node to delete
            # Case 1: No children or one child
            if not root.left:
                return root.right
            if not root.right:
                return root.left

            # Case 2: Two children
            # Replace with inorder successor (min in right subtree)
            successor = self.find_min(root.right)
            root.val = successor.val
            root.right = self.delete(root.right, successor.val)

        return root
```

## 🌲 Tree Traversals

### 1. Depth-First Search (DFS)

**Inorder Traversal (Left -> Root -> Right)**
- For BST, gives sorted order!

```python
def inorder(root):
    if not root:
        return []

    result = []
    result.extend(inorder(root.left))
    result.append(root.val)
    result.extend(inorder(root.right))
    return result

# Iterative using stack
def inorder_iterative(root):
    result = []
    stack = []
    current = root

    while current or stack:
        # Go to leftmost node
        while current:
            stack.append(current)
            current = current.left

        # Process node
        current = stack.pop()
        result.append(current.val)

        # Move to right subtree
        current = current.right

    return result
```

**Preorder Traversal (Root -> Left -> Right)**
- Useful for creating copy of tree

```python
def preorder(root):
    if not root:
        return []

    result = [root.val]
    result.extend(preorder(root.left))
    result.extend(preorder(root.right))
    return result

# Iterative using stack
def preorder_iterative(root):
    if not root:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)

        # Push right first so left is processed first
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result
```

**Postorder Traversal (Left -> Right -> Root)**
- Useful for deleting tree (children before parent)

```python
def postorder(root):
    if not root:
        return []

    result = []
    result.extend(postorder(root.left))
    result.extend(postorder(root.right))
    result.append(root.val)
    return result

# Iterative (more complex)
def postorder_iterative(root):
    if not root:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)

        # Push left then right
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)

    # Reverse to get postorder
    return result[::-1]
```

### 2. Breadth-First Search (BFS) / Level Order

Process nodes level by level using a queue.

```python
from collections import deque

def level_order(root):
    """BFS traversal returning list of levels."""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result
```

## 📊 What Are Graphs?

A **graph** is a collection of nodes (vertices) connected by edges. Unlike trees, graphs can have cycles and multiple paths between nodes.

### Graph Types

**1. Directed vs Undirected**
- **Directed**: Edges have direction (A → B)
- **Undirected**: Edges are bidirectional (A ↔ B)

**2. Weighted vs Unweighted**
- **Weighted**: Edges have costs/weights
- **Unweighted**: All edges equal

**3. Cyclic vs Acyclic**
- **Cyclic**: Contains at least one cycle
- **Acyclic**: No cycles (DAG = Directed Acyclic Graph)

**4. Connected vs Disconnected**
- **Connected**: Path exists between any two nodes
- **Disconnected**: Some nodes unreachable from others

### Graph Representations

**1. Adjacency List (Most Common)**

Space efficient, fast neighbor iteration.

```python
# Using dictionary
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Using list of lists (for numbered nodes)
graph = [
    [1, 2],      # Node 0 connects to 1, 2
    [0, 3, 4],   # Node 1 connects to 0, 3, 4
    [0, 5],      # Node 2 connects to 0, 5
    [1],         # Node 3 connects to 1
    [1, 5],      # Node 4 connects to 1, 5
    [2, 4]       # Node 5 connects to 2, 4
]

# Weighted graph
weighted_graph = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('D', 5)],
    'C': [('A', 2), ('D', 1)],
    'D': [('B', 5), ('C', 1)]
}
```

**2. Adjacency Matrix**

Fast edge lookup, more space.

```python
# For n nodes, create n x n matrix
# matrix[i][j] = 1 if edge from i to j, else 0
matrix = [
    [0, 1, 1, 0, 0, 0],  # Node 0
    [1, 0, 0, 1, 1, 0],  # Node 1
    [1, 0, 0, 0, 0, 1],  # Node 2
    [0, 1, 0, 0, 0, 0],  # Node 3
    [0, 1, 0, 0, 0, 1],  # Node 4
    [0, 0, 1, 0, 1, 0]   # Node 5
]

# Weighted graph
weighted_matrix = [
    [0, 4, 2, 0],  # 0 means no edge
    [4, 0, 0, 5],
    [2, 0, 0, 1],
    [0, 5, 1, 0]
]
```

**3. Edge List**

Simple list of all edges.

```python
edges = [
    (0, 1),
    (0, 2),
    (1, 3),
    (1, 4),
    (2, 5),
    (4, 5)
]

# Weighted
weighted_edges = [
    (0, 1, 4),  # (from, to, weight)
    (0, 2, 2),
    (1, 3, 5),
    (2, 3, 1)
]
```

## 🔍 Graph Traversals

### 1. Depth-First Search (DFS)

Explore as far as possible along each branch before backtracking.

```python
def dfs_recursive(graph, node, visited=None):
    """DFS using recursion."""
    if visited is None:
        visited = set()

    visited.add(node)
    print(node, end=' ')

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

    return visited

def dfs_iterative(graph, start):
    """DFS using stack."""
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()

        if node not in visited:
            visited.add(node)
            print(node, end=' ')

            # Add neighbors to stack
            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)

    return visited
```

### 2. Breadth-First Search (BFS)

Explore all neighbors at current depth before moving deeper.

```python
from collections import deque

def bfs(graph, start):
    """BFS using queue."""
    visited = set([start])
    queue = deque([start])

    while queue:
        node = queue.popleft()
        print(node, end=' ')

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited

def bfs_shortest_path(graph, start, target):
    """Find shortest path using BFS."""
    if start == target:
        return [start]

    visited = {start}
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()

        for neighbor in graph[node]:
            if neighbor not in visited:
                new_path = path + [neighbor]

                if neighbor == target:
                    return new_path

                visited.add(neighbor)
                queue.append((neighbor, new_path))

    return []  # No path found
```

## ⏱️ Time and Space Complexity

### Tree Operations

| Operation | Average (Balanced) | Worst (Unbalanced) | Notes |
|-----------|-------------------|-------------------|-------|
| **BST Search** | O(log n) | O(n) | O(n) when tree is like linked list |
| **BST Insert** | O(log n) | O(n) | Same as search |
| **BST Delete** | O(log n) | O(n) | Same as search |
| **Tree Traversal** | O(n) | O(n) | Visit all nodes once |
| **Tree Height** | O(n) | O(n) | Must check all nodes |
| **Space (recursive)** | O(h) | O(n) | Call stack depth = height |
| **Space (iterative)** | O(w) | O(n) | w = max width for BFS |

### Graph Operations

| Operation | Adjacency List | Adjacency Matrix | Notes |
|-----------|---------------|------------------|-------|
| **Add Vertex** | O(1) | O(V²) | Matrix needs resize |
| **Add Edge** | O(1) | O(1) | Direct insertion |
| **Remove Vertex** | O(V + E) | O(V²) | Must update all edges |
| **Remove Edge** | O(E) | O(1) | List needs search |
| **Check Edge** | O(V) | O(1) | List needs search |
| **Get Neighbors** | O(1) | O(V) | Matrix scans row |
| **DFS/BFS** | O(V + E) | O(V²) | Visit all vertices/edges |
| **Space** | O(V + E) | O(V²) | Matrix always V² |

**V** = number of vertices, **E** = number of edges

## 🎯 Common Patterns and Techniques

### 1. Tree Path Problems

Finding paths in trees (root to leaf, node to node).

```python
def has_path_sum(root, target_sum):
    """Check if root-to-leaf path sums to target."""
    if not root:
        return False

    # Leaf node - check if sum matches
    if not root.left and not root.right:
        return root.val == target_sum

    # Recursively check left and right subtrees
    remaining = target_sum - root.val
    return (has_path_sum(root.left, remaining) or
            has_path_sum(root.right, remaining))

def all_paths(root):
    """Return all root-to-leaf paths."""
    if not root:
        return []

    # Leaf node
    if not root.left and not root.right:
        return [[root.val]]

    paths = []

    # Get paths from left and right subtrees
    for path in all_paths(root.left) + all_paths(root.right):
        paths.append([root.val] + path)

    return paths
```

### 2. Tree Level Problems

Processing nodes by level.

```python
def level_order_traversal(root):
    """Process tree level by level."""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result

def zigzag_level_order(root):
    """Alternate direction each level."""
    if not root:
        return []

    result = []
    queue = deque([root])
    left_to_right = True

    while queue:
        level_size = len(queue)
        level = deque()

        for _ in range(level_size):
            node = queue.popleft()

            # Add to appropriate end based on direction
            if left_to_right:
                level.append(node.val)
            else:
                level.appendleft(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(list(level))
        left_to_right = not left_to_right

    return result
```

### 3. Lowest Common Ancestor (LCA)

Finding common ancestor of two nodes.

```python
def lca(root, p, q):
    """Find LCA in binary tree."""
    if not root or root == p or root == q:
        return root

    left = lca(root.left, p, q)
    right = lca(root.right, p, q)

    # If both sides found nodes, current is LCA
    if left and right:
        return root

    # Return whichever side found a node
    return left if left else right

def lca_bst(root, p, q):
    """Find LCA in BST (more efficient)."""
    # Ensure p <= q
    if p.val > q.val:
        p, q = q, p

    while root:
        # Both in left subtree
        if root.val > q.val:
            root = root.left
        # Both in right subtree
        elif root.val < p.val:
            root = root.right
        # Split point - this is LCA
        else:
            return root

    return None
```

### 4. Graph Connected Components

Finding groups of connected nodes.

```python
def count_components(n, edges):
    """Count connected components in undirected graph."""
    # Build adjacency list
    graph = {i: [] for i in range(n)}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    count = 0

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    for node in range(n):
        if node not in visited:
            dfs(node)
            count += 1

    return count
```

### 5. Cycle Detection

Detecting cycles in graphs.

```python
def has_cycle_undirected(graph):
    """Detect cycle in undirected graph using DFS."""
    visited = set()

    def dfs(node, parent):
        visited.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                # Visited non-parent neighbor = cycle
                return True

        return False

    # Check all components
    for node in graph:
        if node not in visited:
            if dfs(node, None):
                return True

    return False

def has_cycle_directed(graph):
    """Detect cycle in directed graph using DFS."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}

    def dfs(node):
        if color[node] == GRAY:
            # Back edge found = cycle
            return True

        if color[node] == BLACK:
            return False

        color[node] = GRAY  # Mark as processing

        for neighbor in graph[node]:
            if dfs(neighbor):
                return True

        color[node] = BLACK  # Mark as done
        return False

    for node in graph:
        if color[node] == WHITE:
            if dfs(node):
                return True

    return False
```

### 6. Topological Sort

Ordering nodes in DAG such that all edges go left to right.

```python
def topological_sort(graph):
    """Kahn's algorithm using BFS."""
    # Calculate in-degrees
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    # Start with nodes having no incoming edges
    queue = deque([node for node in graph if in_degree[node] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        # Remove edge by decreasing in-degree
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If result has all nodes, no cycle exists
    return result if len(result) == len(graph) else []

def topological_sort_dfs(graph):
    """DFS-based topological sort."""
    visited = set()
    stack = []

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)

    for node in graph:
        if node not in visited:
            dfs(node)

    return stack[::-1]  # Reverse postorder
```

### 7. Grid as Graph

Treating 2D grids as implicit graphs.

```python
def num_islands(grid):
    """Count islands using DFS on grid."""
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = set()
    count = 0

    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            (r, c) in visited or grid[r][c] == '0'):
            return

        visited.add((r, c))

        # Explore 4 directions
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                dfs(r, c)
                count += 1

    return count
```

## 🚨 Edge Cases to Consider

### Trees
1. **Empty tree** - `root = None`
2. **Single node** - Root with no children
3. **Only left children** - Skewed tree (like linked list)
4. **Only right children** - Skewed tree
5. **Duplicate values** - Especially in BST
6. **Large negative values** - In path sum problems
7. **Deep tree** - Stack overflow with recursion

### Graphs
1. **Empty graph** - No nodes
2. **Single node** - No edges
3. **Disconnected components** - Multiple subgraphs
4. **Self-loops** - Edge from node to itself
5. **Parallel edges** - Multiple edges between same nodes
6. **Negative weights** - In weighted graphs
7. **Very large graphs** - Memory constraints

## 🎓 When to Use Trees vs Graphs

**Use Trees when:**
- Natural hierarchy exists (file systems, org charts)
- Need sorted data with fast operations (BST)
- Need priority operations (heap)
- Parsing expressions or hierarchical data
- No cycles in relationships

**Use Graphs when:**
- Complex many-to-many relationships
- Need to find paths between any two nodes
- Modeling networks (social, computer, transportation)
- Cycles are possible or meaningful
- No clear hierarchy

## 📚 LeetCode Problem Categories

### Trees - Easy
- Maximum Depth of Binary Tree
- Invert Binary Tree
- Same Tree
- Symmetric Tree
- Binary Tree Paths

### Trees - Medium
- Binary Tree Level Order Traversal
- Validate Binary Search Tree
- Lowest Common Ancestor
- Binary Tree Right Side View
- Path Sum II

### Trees - Hard
- Binary Tree Maximum Path Sum
- Serialize and Deserialize Binary Tree
- Vertical Order Traversal

### Graphs - Easy
- Find Center of Star Graph
- Find if Path Exists in Graph

### Graphs - Medium
- Number of Islands
- Clone Graph
- Course Schedule (I & II)
- Pacific Atlantic Water Flow
- Rotting Oranges

### Graphs - Hard
- Word Ladder II
- Alien Dictionary
- Critical Connections in Network

## 🔧 Python-Specific Tips

```python
# Creating trees easily
from collections import deque

def build_tree(values):
    """Build tree from level-order list."""
    if not values:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    i = 1

    while queue and i < len(values):
        node = queue.popleft()

        if values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1

        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root

# Useful imports
from collections import deque, defaultdict
from typing import Optional, List

# Default dict for graphs
graph = defaultdict(list)
graph['A'].append('B')  # No KeyError!

# Set for visited tracking
visited = set()

# Deque for efficient queue operations
queue = deque()
```

## 💡 Interview Tips

1. **Clarify the problem**
   - Tree or graph?
   - Directed or undirected?
   - Weighted or unweighted?
   - Can there be cycles?
   - Connected or disconnected?

2. **Choose traversal wisely**
   - Level-by-level → BFS
   - Explore all paths → DFS
   - BST operations → Take advantage of ordering
   - Shortest path (unweighted) → BFS

3. **Consider recursion vs iteration**
   - Recursion: Cleaner code, but stack overflow risk
   - Iteration: More control, but more complex

4. **Track visited nodes**
   - Always prevent revisiting in graphs
   - Use set for O(1) lookups

5. **Watch for edge cases**
   - Empty input
   - Single node
   - Disconnected components
   - Cycles

6. **Optimize space**
   - Can you traverse without extra visited set?
   - Can you modify input to mark visited?

## 🔗 Related Topics

- **Heaps** - Complete binary trees with heap property
- **Tries** - Tree for string operations
- **Union-Find** - For connected components
- **Dynamic Programming** - Tree DP problems
- **Backtracking** - Path finding, combinations

---

Ready to practice? Check out the [examples](./examples/) folder for fully solved problems!
