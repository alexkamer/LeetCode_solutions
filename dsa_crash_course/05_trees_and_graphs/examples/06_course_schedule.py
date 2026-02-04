"""
Course Schedule (LeetCode #207) and Course Schedule II (LeetCode #210)

Problem (Course Schedule):
There are a total of numCourses courses you have to take, labeled from 0 to
numCourses - 1. You are given an array prerequisites where
prerequisites[i] = [ai, bi] indicates that you must take course bi first if
you want to take course ai.

Return true if you can finish all courses. Otherwise, return false.

Problem (Course Schedule II):
Return the ordering of courses you should take to finish all courses.
If there are multiple valid answers, return any of them. If it's impossible
to finish all courses, return an empty array.

Example 1:
Input: numCourses = 2, prerequisites = [[1,0]]
Output (I): true
Output (II): [0,1]
Explanation: There are 2 courses. To take course 1, you must first take course 0.

Example 2:
Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output (I): false
Output (II): []
Explanation: Circular dependency - impossible to complete.

Example 3:
Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output (I): true
Output (II): [0,2,1,3] or [0,1,2,3]
Explanation: Multiple valid orderings exist.

Constraints:
- 1 <= numCourses <= 2000
- 0 <= prerequisites.length <= 5000
- prerequisites[i].length == 2
- 0 <= ai, bi < numCourses
- All pairs [ai, bi] are distinct

Key Insight: This is a topological sort problem on a directed graph!
Course dependencies form a DAG (must be acyclic to complete all courses).
"""

from collections import deque, defaultdict


def can_finish_dfs(num_courses, prerequisites):
    """
    Detect cycle using DFS with 3-color algorithm.

    This is the classic cycle detection algorithm for directed graphs.

    Approach:
    1. Build adjacency list from prerequisites
    2. Use 3 colors: WHITE (unvisited), GRAY (processing), BLACK (done)
    3. If we encounter a GRAY node during DFS, there's a cycle
    4. If no cycles found, all courses can be completed

    Time Complexity: O(V + E) where V = courses, E = prerequisites
    Space Complexity: O(V + E) for graph and recursion stack

    Args:
        num_courses: Number of courses
        prerequisites: List of [course, prerequisite] pairs

    Returns:
        Boolean indicating if all courses can be completed
    """
    # Build adjacency list
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    # 3-color DFS for cycle detection
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * num_courses

    def has_cycle(course):
        """Return True if cycle detected."""
        if color[course] == GRAY:
            # Back edge found - cycle exists
            return True

        if color[course] == BLACK:
            # Already processed, no cycle
            return False

        # Mark as processing
        color[course] = GRAY

        # Check all neighbors
        for neighbor in graph[course]:
            if has_cycle(neighbor):
                return True

        # Mark as done
        color[course] = BLACK
        return False

    # Check each course (handles disconnected components)
    for course in range(num_courses):
        if color[course] == WHITE:
            if has_cycle(course):
                return False

    return True


def find_order_dfs(num_courses, prerequisites):
    """
    Topological sort using DFS (postorder approach).

    Approach:
    1. Build adjacency list
    2. DFS from each unvisited node
    3. Add node to result AFTER visiting all neighbors
    4. Reverse result to get topological order

    The key: postorder DFS gives reverse topological order!

    Time Complexity: O(V + E)
    Space Complexity: O(V + E)

    Args:
        num_courses: Number of courses
        prerequisites: List of [course, prerequisite] pairs

    Returns:
        List of courses in valid order, or empty list if impossible
    """
    # Build adjacency list
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * num_courses
    order = []
    has_cycle = [False]

    def dfs(course):
        """DFS to detect cycle and build order."""
        if color[course] == GRAY:
            has_cycle[0] = True
            return

        if color[course] == BLACK:
            return

        color[course] = GRAY

        for neighbor in graph[course]:
            dfs(neighbor)

        color[course] = BLACK
        order.append(course)  # Add after processing all dependencies

    for course in range(num_courses):
        if color[course] == WHITE:
            dfs(course)

    if has_cycle[0]:
        return []

    return order[::-1]  # Reverse for topological order


def find_order_bfs(num_courses, prerequisites):
    """
    Topological sort using BFS (Kahn's algorithm).

    This is often preferred because it's more intuitive and easier
    to understand than the DFS approach.

    Approach:
    1. Calculate in-degree (number of prerequisites) for each course
    2. Start with courses that have no prerequisites (in-degree = 0)
    3. Process each course, reducing in-degree of dependent courses
    4. When a course's in-degree becomes 0, it can be taken
    5. If we process all courses, no cycle; otherwise cycle exists

    Time Complexity: O(V + E)
    Space Complexity: O(V + E)

    Args:
        num_courses: Number of courses
        prerequisites: List of [course, prerequisite] pairs

    Returns:
        List of courses in valid order, or empty list if impossible
    """
    # Build adjacency list and calculate in-degrees
    graph = defaultdict(list)
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    # Start with courses that have no prerequisites
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    order = []

    while queue:
        course = queue.popleft()
        order.append(course)

        # Remove this course (reduce in-degree of dependent courses)
        for neighbor in graph[course]:
            in_degree[neighbor] -= 1

            # If neighbor now has no prerequisites, can take it
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If we processed all courses, no cycle exists
    if len(order) == num_courses:
        return order
    else:
        return []  # Cycle detected


def find_all_orders(num_courses, prerequisites):
    """
    Find ALL possible valid course orderings.

    This uses backtracking to explore all valid topological sorts.
    Note: Can be exponential in time!

    Time Complexity: O(V! * E) in worst case
    Space Complexity: O(V + E)

    Args:
        num_courses: Number of courses
        prerequisites: List of [course, prerequisite] pairs

    Returns:
        List of all valid course orderings
    """
    # Build adjacency list and calculate in-degrees
    graph = defaultdict(list)
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    all_orders = []

    def backtrack(current_order, remaining_in_degree):
        """Backtrack to find all valid orderings."""
        if len(current_order) == num_courses:
            all_orders.append(current_order[:])
            return

        # Try all courses with no remaining prerequisites
        for course in range(num_courses):
            if remaining_in_degree[course] == 0 and course not in current_order:
                # Take this course
                current_order.append(course)

                # Update in-degrees
                new_in_degree = remaining_in_degree[:]
                new_in_degree[course] = -1  # Mark as taken

                for neighbor in graph[course]:
                    new_in_degree[neighbor] -= 1

                backtrack(current_order, new_in_degree)

                # Backtrack
                current_order.pop()

    backtrack([], in_degree)
    return all_orders


def visualize_dependencies(num_courses, prerequisites):
    """Visualize course dependency graph."""
    print(f"Courses: {list(range(num_courses))}")
    print("Prerequisites (course <- prerequisite):")
    for course, prereq in prerequisites:
        print(f"  {course} <- {prereq}")


def test_course_schedule():
    """Test cases covering various scenarios."""

    # Test case 1: Possible (linear dependency)
    assert can_finish_dfs(2, [[1, 0]]) == True
    assert find_order_dfs(2, [[1, 0]]) == [0, 1]
    assert find_order_bfs(2, [[1, 0]]) == [0, 1]

    # Test case 2: Impossible (cycle)
    assert can_finish_dfs(2, [[1, 0], [0, 1]]) == False
    assert find_order_dfs(2, [[1, 0], [0, 1]]) == []
    assert find_order_bfs(2, [[1, 0], [0, 1]]) == []

    # Test case 3: Complex valid case
    assert can_finish_dfs(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) == True
    order = find_order_bfs(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    assert len(order) == 4
    assert order.index(0) < order.index(1)
    assert order.index(0) < order.index(2)
    assert order.index(1) < order.index(3)
    assert order.index(2) < order.index(3)

    # Test case 4: No prerequisites
    assert can_finish_dfs(3, []) == True
    order = find_order_bfs(3, [])
    assert sorted(order) == [0, 1, 2]

    # Test case 5: Single course
    assert can_finish_dfs(1, []) == True
    assert find_order_bfs(1, []) == [0]

    # Test case 6: Complex cycle
    assert can_finish_dfs(4, [[1, 0], [2, 1], [0, 2]]) == False
    assert find_order_bfs(4, [[1, 0], [2, 1], [0, 2]]) == []

    # Test case 7: Diamond dependency
    prereqs = [[1, 0], [2, 0], [3, 1], [3, 2]]
    assert can_finish_dfs(4, prereqs) == True
    order = find_order_bfs(4, prereqs)
    assert order[0] == 0  # Must start with 0
    assert order[-1] == 3  # Must end with 3

    print("All test cases passed!")


if __name__ == "__main__":
    test_course_schedule()

    # Example usage with visualization
    print("\nExample 1: Valid Course Schedule")
    print("=" * 50)

    num_courses = 4
    prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]

    visualize_dependencies(num_courses, prerequisites)

    print(f"\nCan finish all courses: {can_finish_dfs(num_courses, prerequisites)}")

    order_bfs = find_order_bfs(num_courses, prerequisites)
    print(f"Valid order (BFS/Kahn's): {order_bfs}")

    order_dfs = find_order_dfs(num_courses, prerequisites)
    print(f"Valid order (DFS): {order_dfs}")

    # Show all possible orders
    if num_courses <= 5:  # Only for small inputs
        all_orders = find_all_orders(num_courses, prerequisites)
        print(f"\nAll valid orderings ({len(all_orders)} total):")
        for i, order in enumerate(all_orders, 1):
            print(f"  {i}. {order}")

    print("\n" + "=" * 50)
    print("Example 2: Impossible (Cycle)")
    print("=" * 50)

    num_courses2 = 3
    prerequisites2 = [[1, 0], [2, 1], [0, 2]]

    visualize_dependencies(num_courses2, prerequisites2)

    print(f"\nCan finish all courses: {can_finish_dfs(num_courses2, prerequisites2)}")
    print("Cycle detected: 0 -> 1 -> 2 -> 0")

    order = find_order_bfs(num_courses2, prerequisites2)
    print(f"Valid order: {order if order else 'None (impossible)'}")

    print("\n" + "=" * 50)
    print("Algorithm Comparison:")
    print("=" * 50)
    print("1. DFS (3-color): Good for cycle detection")
    print("   - Uses recursion")
    print("   - Natural for finding topological order (postorder)")
    print()
    print("2. BFS (Kahn's): More intuitive")
    print("   - Uses queue and in-degrees")
    print("   - Processes nodes level-by-level")
    print("   - Often preferred in interviews")
    print()
    print("Both: O(V + E) time, O(V + E) space")

    print("\n" + "=" * 50)
    print("Real-world Applications:")
    print("=" * 50)
    print("- Course prerequisites (this problem!)")
    print("- Build systems (compile dependencies)")
    print("- Task scheduling with dependencies")
    print("- Package managers (npm, pip, etc.)")
    print("- Spreadsheet formula evaluation")
