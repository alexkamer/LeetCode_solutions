# Trees and Graphs - Quick Reference

## Complexity Cheat Sheet

### Tree Operations (Binary Tree)
- **Access**: O(n) - no direct access, must traverse
- **Search (BST)**: O(log n) balanced, O(n) worst
- **Insert (BST)**: O(log n) balanced, O(n) worst
- **Delete (BST)**: O(log n) balanced, O(n) worst
- **Traversal**: O(n) - visit all nodes
- **Space (recursive)**: O(h) where h is height
- **Space (BFS)**: O(w) where w is max width

### Graph Operations
**Adjacency List:**
- **Add vertex**: O(1)
- **Add edge**: O(1)
- **Remove vertex**: O(V + E)
- **Check edge**: O(V)
- **DFS/BFS**: O(V + E)
- **Space**: O(V + E)

**Adjacency Matrix:**
- **Add/remove edge**: O(1)
- **Check edge**: O(1)
- **DFS/BFS**: O(V²)
- **Space**: O(V²)

## Tree Traversal Templates

### DFS Traversals (Recursive)

```python
# Inorder (Left -> Root -> Right)
# For BST: gives sorted order
def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

# Preorder (Root -> Left -> Right)
# Use for: copying tree, prefix expressions
def preorder(root):
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)

# Postorder (Left -> Right -> Root)
# Use for: deleting tree, postfix expressions
def postorder(root):
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]
```

### DFS Traversals (Iterative)

```python
# Inorder iterative
def inorder_iterative(root):
    result, stack = [], []
    current = root

    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.val)
        current = current.right

    return result

# Preorder iterative
def preorder_iterative(root):
    if not root:
        return []

    result, stack = [], [root]

    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result
```

### BFS (Level Order)

```python
from collections import deque

def level_order(root):
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

## Graph Traversal Templates

### DFS (Recursive)

```python
def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = set()

    visited.add(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

    return visited
```

### DFS (Iterative)

```python
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()

        if node not in visited:
            visited.add(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    stack.append(neighbor)

    return visited
```

### BFS

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])

    while queue:
        node = queue.popleft()

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited
```

## Common Patterns

### 1. Tree Path Sum

```python
def has_path_sum(root, target):
    if not root:
        return False

    if not root.left and not root.right:
        return root.val == target

    remaining = target - root.val
    return (has_path_sum(root.left, remaining) or
            has_path_sum(root.right, remaining))
```

### 2. Lowest Common Ancestor

```python
# Binary Tree
def lca(root, p, q):
    if not root or root == p or root == q:
        return root

    left = lca(root.left, p, q)
    right = lca(root.right, p, q)

    if left and right:
        return root

    return left if left else right

# BST (more efficient)
def lca_bst(root, p, q):
    while root:
        if root.val > q.val:
            root = root.left
        elif root.val < p.val:
            root = root.right
        else:
            return root
```

### 3. Validate BST

```python
def is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):
    if not root:
        return True

    if root.val <= min_val or root.val >= max_val:
        return False

    return (is_valid_bst(root.left, min_val, root.val) and
            is_valid_bst(root.right, root.val, max_val))
```

### 4. Connected Components

```python
def count_components(n, edges):
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

```python
# Undirected graph
def has_cycle_undirected(graph):
    visited = set()

    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        return False

    for node in graph:
        if node not in visited:
            if dfs(node, None):
                return True
    return False

# Directed graph (3-color)
def has_cycle_directed(graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}

    def dfs(node):
        if color[node] == GRAY:
            return True
        if color[node] == BLACK:
            return False

        color[node] = GRAY
        for neighbor in graph[node]:
            if dfs(neighbor):
                return True
        color[node] = BLACK
        return False

    for node in graph:
        if color[node] == WHITE:
            if dfs(node):
                return True
    return False
```

### 6. Topological Sort

```python
# Kahn's algorithm (BFS)
def topological_sort(graph):
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    queue = deque([node for node in graph if in_degree[node] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == len(graph) else []

# DFS-based
def topological_sort_dfs(graph):
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

    return stack[::-1]
```

### 7. Grid DFS/BFS

```python
# Count islands (DFS)
def num_islands(grid):
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = set()

    def dfs(r, c):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            (r, c) in visited or grid[r][c] == '0'):
            return

        visited.add((r, c))
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                dfs(r, c)
                count += 1

    return count

# Shortest path in grid (BFS)
def shortest_path_grid(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start[0], start[1], 0)])
    visited = {start}

    while queue:
        r, c, dist = queue.popleft()

        if (r, c) == end:
            return dist

        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols and
                (nr, nc) not in visited and grid[nr][nc] != 'X'):
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))

    return -1
```

## Tree Node Definition

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

## Graph Representations

```python
# Adjacency list (dict)
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A'],
    'D': ['B']
}

# Adjacency list (list)
graph = [
    [1, 2],    # Node 0 connects to 1, 2
    [0, 3],    # Node 1 connects to 0, 3
    [0],       # Node 2 connects to 0
    [1]        # Node 3 connects to 1
]

# Build from edges
def build_graph(n, edges):
    graph = {i: [] for i in range(n)}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)  # Remove for directed
    return graph
```

## Common Edge Cases

### Trees
- Empty tree (root = None)
- Single node
- Skewed tree (all left or all right)
- Balanced vs unbalanced
- Duplicate values
- Negative values

### Graphs
- Empty graph
- Single node (no edges)
- Disconnected components
- Self-loops
- Cycles
- Directed vs undirected

## Problem Recognition

| Keywords | Pattern | Approach |
|----------|---------|----------|
| "level by level", "level order" | Level traversal | BFS |
| "path from root to leaf" | Tree path | DFS |
| "all paths", "combinations" | Backtracking | DFS |
| "validate BST" | Tree validation | DFS with bounds |
| "lowest common ancestor" | LCA | DFS |
| "shortest path" (unweighted) | Shortest path | BFS |
| "connected components" | Components | DFS/BFS |
| "cycle detection" | Cycle | DFS with colors |
| "topological order" | Topo sort | Kahn's / DFS |
| "islands", "regions" | Grid DFS/BFS | DFS/BFS |

## When to Use DFS vs BFS

### Use DFS when:
- Finding any path (not necessarily shortest)
- Exploring all possibilities (backtracking)
- Checking connectivity
- Topological sort
- Detecting cycles
- Tree traversals (inorder, preorder, postorder)
- Space is limited (can be O(h) for trees)

### Use BFS when:
- Finding shortest path (unweighted)
- Level-by-level processing
- Finding all nodes at distance k
- Checking if graph is bipartite
- Finding connected components (either works)

## Recursion vs Iteration

### Recursion Pros:
- Cleaner, more readable code
- Natural for tree problems
- Less code to write

### Recursion Cons:
- Stack overflow for deep trees
- O(h) space for call stack
- Harder to debug

### Iteration Pros:
- No stack overflow
- More control over space
- Easier to see state

### Iteration Cons:
- More complex code
- Need explicit stack/queue
- More lines of code

## Quick Wins

1. **Choose right traversal**: BFS for shortest path, DFS for paths/cycles
2. **Track visited**: Always use set for O(1) lookup
3. **Use deque**: For BFS, use `collections.deque` for O(1) popleft
4. **BST properties**: Use ordering to optimize (like binary search)
5. **Level order**: Remember to capture level size before loop
6. **Grid as graph**: Treat (row, col) as nodes, use directions array
7. **Validate BST**: Pass min/max bounds down, not just comparing neighbors
8. **LCA**: If both sides return nodes, current node is LCA

## Python Tips

```python
from collections import deque, defaultdict

# Build graph with defaultdict
graph = defaultdict(list)
graph['A'].append('B')  # No KeyError

# Directions for grid traversal
directions = [(0,1), (0,-1), (1,0), (-1,0)]
# Or with diagonals
directions = [(0,1), (0,-1), (1,0), (-1,0),
              (1,1), (1,-1), (-1,1), (-1,-1)]

# Swap values
p.val, q.val = q.val, p.val

# Check if leaf node
if not node.left and not node.right:
    # It's a leaf
```

## Interview Template

```python
# Tree problem
def solve_tree(root):
    # Base case
    if not root:
        return base_value

    # Recursive case
    left_result = solve_tree(root.left)
    right_result = solve_tree(root.right)

    # Combine results
    return combine(root.val, left_result, right_result)

# Graph problem
def solve_graph(graph, start):
    visited = set()

    def dfs(node):
        if node in visited:
            return

        visited.add(node)

        for neighbor in graph[node]:
            dfs(neighbor)

    dfs(start)
    return visited
```
