"""
Task Scheduler (LeetCode #621)

Problem:
You are given an array of CPU tasks, each represented by letters A to Z, and
a cooling time, n. Each cycle or interval allows the completion of one task.
Tasks can be completed in any order, but there's a constraint: identical tasks
must be separated by at least n intervals due to cooling time.

Return the minimum number of intervals required to complete all tasks.

Example 1:
Input: tasks = ["A","A","A","B","B","B"], n = 2
Output: 8
Explanation: A possible sequence is: A -> B -> idle -> A -> B -> idle -> A -> B.
After completing A, you must wait 2 cycles before doing A again. Same for B.

Example 2:
Input: tasks = ["A","C","A","B","D","B"], n = 1
Output: 6
Explanation: A possible sequence is: A -> B -> C -> D -> A -> B.

Example 3:
Input: tasks = ["A","A","A","B","B","B"], n = 3
Output: 10
Explanation: A possible sequence is: A -> B -> idle -> idle -> A -> B -> idle
-> idle -> A -> B.

Constraints:
- 1 <= tasks.length <= 10^4
- tasks[i] is an uppercase English letter
- 0 <= n <= 100
"""


def least_interval_naive(tasks, n):
    """
    Naive simulation approach.

    Approach:
    1. Track when each task was last executed
    2. Simulate each time unit
    3. Pick available task with highest frequency
    4. Continue until all tasks done

    Time Complexity: O(time * m) where time is result, m is unique tasks
    Space Complexity: O(m)

    This is correct but not optimal.
    """
    from collections import Counter

    freq = Counter(tasks)
    last_used = {}
    time = 0
    total_tasks = len(tasks)

    while total_tasks > 0:
        # Find available task with highest frequency
        best_task = None
        best_freq = 0

        for task, count in freq.items():
            if count > 0:
                # Check if task is available (cooled down)
                if task not in last_used or time - last_used[task] > n:
                    if count > best_freq:
                        best_freq = count
                        best_task = task

        if best_task:
            # Execute task
            freq[best_task] -= 1
            last_used[best_task] = time
            total_tasks -= 1
        # else: idle time

        time += 1

    return time


def least_interval_heap(tasks, n):
    """
    Max-heap with cooldown queue approach.

    Approach:
    1. Count task frequencies
    2. Use max-heap for available tasks
    3. Use queue for tasks in cooldown
    4. Each cycle:
       - Execute up to n+1 different tasks
       - Move cooled tasks back to heap
    5. Continue until all tasks done

    Time Complexity: O(m log m) where m is unique tasks
    Space Complexity: O(m)

    Args:
        tasks: List of task letters
        n: Cooldown period

    Returns:
        Minimum intervals needed
    """
    from collections import Counter
    import heapq

    # Count frequencies
    freq = Counter(tasks)

    # Max-heap of frequencies (negate for max-heap)
    heap = [-count for count in freq.values()]
    heapq.heapify(heap)

    time = 0

    while heap:
        # Tasks to put back after this cycle
        temp = []

        # Execute n+1 tasks (one cycle with cooldown n)
        for _ in range(n + 1):
            if heap:
                # Get most frequent available task
                count = heapq.heappop(heap)

                # Decrement count (it's negative)
                if count < -1:
                    temp.append(count + 1)

        # Put tasks back in heap
        for count in temp:
            heapq.heappush(heap, count)

        # Add time for this cycle
        if heap:
            # More tasks remain, full cycle used
            time += n + 1
        else:
            # Last cycle, only count executed tasks
            time += len(temp)

    return time


def least_interval_math(tasks, n):
    """
    Mathematical formula approach (optimal).

    Approach:
    1. Find most frequent task and its count
    2. Calculate minimum intervals based on most frequent task
    3. Account for tasks that can fill idle slots

    Key insight:
    - Most frequent task determines minimum time
    - It must be executed with n intervals between
    - Other tasks can fill idle slots
    - If no idle slots remain, time = total tasks

    Formula:
    - max_freq = frequency of most common task
    - num_max = number of tasks with max_freq
    - idle_slots = (max_freq - 1) * (n + 1) + num_max
    - return max(idle_slots, len(tasks))

    Time Complexity: O(m) where m is unique tasks
    Space Complexity: O(m)

    This is the optimal solution!

    Args:
        tasks: List of task letters
        n: Cooldown period

    Returns:
        Minimum intervals needed
    """
    from collections import Counter

    # Count frequencies
    freq = Counter(tasks)

    # Find maximum frequency and count of tasks with max frequency
    max_freq = max(freq.values())
    num_max = sum(1 for f in freq.values() if f == max_freq)

    # Calculate minimum intervals
    # Pattern: [max_task, other, other, ..., max_task, ...]
    # Number of gaps between max_freq tasks: max_freq - 1
    # Each gap needs n slots minimum
    # Last position has num_max tasks
    intervals = (max_freq - 1) * (n + 1) + num_max

    # If we have enough tasks to fill all slots, no idle needed
    return max(intervals, len(tasks))


def visualize_task_scheduler(tasks, n):
    """
    Visualize task scheduling process.

    Shows how tasks are scheduled with cooldown.
    """
    from collections import Counter
    import heapq

    print(f"\nScheduling tasks: {tasks}")
    print(f"Cooldown period: {n}")
    print("=" * 60)

    # Count frequencies
    freq = Counter(tasks)
    print(f"\nTask frequencies: {dict(freq)}")

    # Max-heap
    heap = [(-count, task) for task, count in freq.items()]
    heapq.heapify(heap)

    schedule = []
    time = 0

    print("\nScheduling process:")
    print("-" * 60)

    while heap:
        print(f"\nCycle starting at time {time}:")
        print(f"  Available tasks (heap): {sorted(heap)}")

        temp = []
        cycle_schedule = []

        # Execute n+1 tasks
        for i in range(n + 1):
            if heap:
                neg_count, task = heapq.heappop(heap)
                cycle_schedule.append(task)

                # If task has more executions, save for later
                if neg_count < -1:
                    temp.append((neg_count + 1, task))
            elif temp:
                # Heap empty but more tasks remain = idle
                cycle_schedule.append("idle")

        # Put tasks back
        for item in temp:
            heapq.heappush(heap, item)

        # Update schedule
        schedule.extend(cycle_schedule)
        time += len(cycle_schedule)

        print(f"  Executed: {' -> '.join(cycle_schedule)}")
        print(f"  Cooldown queue: {sorted(temp)}")
        print(f"  Total time: {time}")

    print(f"\n{'=' * 60}")
    print(f"Final schedule ({len(schedule)} intervals):")
    print(f"  {' -> '.join(schedule)}")

    return len(schedule)


def explain_math_approach(tasks, n):
    """
    Explain the mathematical formula approach.

    Shows why the formula works.
    """
    from collections import Counter

    print(f"\nTasks: {tasks}")
    print(f"Cooldown: {n}")
    print("=" * 60)

    # Count frequencies
    freq = Counter(tasks)
    print(f"\nTask frequencies: {dict(freq)}")

    # Find maximum frequency
    max_freq = max(freq.values())
    num_max = sum(1 for f in freq.values() if f == max_freq)
    max_tasks = [task for task, f in freq.items() if f == max_freq]

    print(f"\nMost frequent task(s): {max_tasks}")
    print(f"  Frequency: {max_freq}")
    print(f"  Number with max frequency: {num_max}")

    # Calculate intervals
    print(f"\nCalculation:")
    print(f"  Most frequent tasks create a skeleton:")
    print(f"  [Task] [n slots] [Task] [n slots] ... [Task]")
    print(f"  ")
    print(f"  Number of gaps: {max_freq - 1}")
    print(f"  Slots per gap: {n + 1} (including task itself)")
    print(f"  Last position has {num_max} task(s)")
    print(f"  ")
    print(f"  Formula: (max_freq - 1) * (n + 1) + num_max")
    print(f"         = ({max_freq} - 1) * ({n} + 1) + {num_max}")

    intervals = (max_freq - 1) * (n + 1) + num_max
    print(f"         = {intervals}")

    print(f"\n  Total tasks: {len(tasks)}")

    if intervals >= len(tasks):
        print(f"  Result: {intervals} (need idle time)")
    else:
        print(
            f"  Result: {len(tasks)} (enough tasks to fill all slots, "
            f"no idle needed)"
        )

    return max(intervals, len(tasks))


def compare_approaches(tasks, n):
    """Compare different task scheduling approaches."""
    import time

    approaches = [
        ("Heap with Cooldown", least_interval_heap),
        ("Mathematical Formula", least_interval_math),
    ]

    print(f"\nInput: tasks = {tasks}, n = {n}")
    print("=" * 60)

    results = []
    for name, func in approaches:
        start = time.perf_counter()
        result = func(tasks[:], n)
        elapsed = time.perf_counter() - start

        results.append((name, result, elapsed))
        print(f"{name:25s}: {result} intervals ({elapsed * 1000000:.2f} µs)")

    # Verify all give same result
    assert all(r[1] == results[0][1] for r in results), "Results don't match!"


def test_task_scheduler():
    """Test cases covering various scenarios."""

    # Test case 1: Basic example
    assert least_interval_heap(["A", "A", "A", "B", "B", "B"], 2) == 8
    assert least_interval_math(["A", "A", "A", "B", "B", "B"], 2) == 8

    # Test case 2: No cooldown needed
    assert least_interval_heap(["A", "C", "A", "B", "D", "B"], 1) == 6
    assert least_interval_math(["A", "C", "A", "B", "D", "B"], 1) == 6

    # Test case 3: Long cooldown
    assert least_interval_heap(["A", "A", "A", "B", "B", "B"], 3) == 10
    assert least_interval_math(["A", "A", "A", "B", "B", "B"], 3) == 10

    # Test case 4: No cooldown (n=0)
    assert least_interval_heap(["A", "A", "A", "B", "B", "B"], 0) == 6
    assert least_interval_math(["A", "A", "A", "B", "B", "B"], 0) == 6

    # Test case 5: Single task type
    assert least_interval_heap(["A", "A", "A"], 2) == 7
    assert least_interval_math(["A", "A", "A"], 2) == 7

    # Test case 6: All different tasks
    assert least_interval_heap(["A", "B", "C", "D"], 2) == 4
    assert least_interval_math(["A", "B", "C", "D"], 2) == 4

    # Test case 7: Many tasks, small cooldown
    tasks = ["A"] * 6 + ["B"] * 5 + ["C"] * 4 + ["D"] * 3
    result = least_interval_heap(tasks, 2)
    assert result >= len(tasks)

    # Test case 8: One very frequent task
    tasks = ["A"] * 10 + ["B"] * 2
    result = least_interval_math(tasks, 3)
    assert result >= len(tasks)

    # Test case 9: Multiple max frequency
    tasks = ["A", "A", "A", "B", "B", "B", "C", "C", "C"]
    result = least_interval_math(tasks, 2)
    assert result >= len(tasks)

    # Test case 10: Large cooldown
    tasks = ["A", "A", "A"]
    assert least_interval_math(tasks, 10) == 23

    print("All test cases passed!")


if __name__ == "__main__":
    # Run tests
    test_task_scheduler()

    # Visualization
    print("\n" + "=" * 60)
    print("EXAMPLE WITH VISUALIZATION")
    print("=" * 60)
    tasks = ["A", "A", "A", "B", "B", "B"]
    n = 2
    visualize_task_scheduler(tasks, n)

    # Mathematical explanation
    print("\n" + "=" * 60)
    print("MATHEMATICAL APPROACH EXPLANATION")
    print("=" * 60)
    explain_math_approach(tasks, n)

    # Compare approaches
    print("\n" + "=" * 60)
    print("COMPARING APPROACHES")
    print("=" * 60)

    test_cases = [
        (["A", "A", "A", "B", "B", "B"], 2),
        (["A", "C", "A", "B", "D", "B"], 1),
        (["A", "A", "A", "B", "B", "B"], 3),
    ]

    for tasks, n in test_cases:
        compare_approaches(tasks, n)

    # Detailed analysis
    print("\n" + "=" * 60)
    print("COMPLEXITY ANALYSIS")
    print("=" * 60)
    print("""
Approach              Time              Space      Notes
------------------------------------------------------------
Naive Simulation      O(time * m)       O(m)       Slow for large n
Heap + Cooldown       O(m log m)        O(m)       Good, intuitive
Mathematical Formula  O(m)              O(m)       Optimal!

Where:
- m = number of unique tasks (at most 26)
- time = result (number of intervals)

Key Insights - Mathematical Approach:
====================================

The Problem Structure:
- Most frequent task must be spread out
- Creates a "skeleton" with required gaps
- Other tasks fill the gaps
- Idle time only if gaps can't be filled

The Formula:
intervals = (max_freq - 1) * (n + 1) + num_max

Explanation:
1. Most frequent task appears max_freq times
2. Creates (max_freq - 1) gaps between occurrences
3. Each gap has n slots after the task (n + 1 total per segment)
4. Last segment has num_max tasks (all tasks with max frequency)

Example: tasks = ["A","A","A","B","B","B"], n = 2

Task frequencies: A=3, B=3
max_freq = 3, num_max = 2

Skeleton:
[A] [_] [_] [A] [_] [_] [A]
 ^   n=2 slots  ^  n=2 slots ^

Formula: (3-1) * (2+1) + 2 = 2 * 3 + 2 = 8

Fill with B:
[A] [B] [_] [A] [B] [_] [A] [B]
 1   2   3   4   5   6   7   8  = 8 intervals

Why max(formula, len(tasks))?
- If we have enough variety of tasks
- We can fill all gaps without idle
- In that case, time = total tasks
- Formula gives lower bound from most frequent task

Heap Approach:
- Simulate the scheduling process
- Use max-heap to always pick most frequent available task
- Execute n+1 tasks per cycle (one of each within cooldown)
- Track cooldown with temporary queue
- Intuitive but more complex than formula

When to use each:
- Heap: When you need actual schedule, not just time
- Formula: When you only need minimum time (optimal)
- Both are good for interviews (formula shows insight)

This problem demonstrates:
1. Greedy scheduling with constraints
2. Mathematical optimization
3. Heap for priority-based simulation
4. Pattern recognition (most frequent creates skeleton)

Interview Strategy:
- Start with heap approach (shows understanding)
- Optimize to formula (shows analytical thinking)
- Explain why formula works (shows deep insight)
    """)
