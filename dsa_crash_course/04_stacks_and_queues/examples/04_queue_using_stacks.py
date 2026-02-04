"""
Implement Queue using Stacks (LeetCode #232)

Problem:
Implement a first in first out (FIFO) queue using only two stacks. The implemented
queue should support all the functions of a normal queue (push, peek, pop, and empty).

Implement the MyQueue class:
- void push(int x) Pushes element x to the back of the queue.
- int pop() Removes the element from the front of the queue and returns it.
- int peek() Returns the element at the front of the queue.
- boolean empty() Returns true if the queue is empty, false otherwise.

Notes:
- You must use only standard operations of a stack, which means only push to top,
  peek/pop from top, size, and is empty operations are valid.
- Depending on your language, the stack may not be supported natively. You may
  simulate a stack using a list or deque (double-ended queue) as long as you use
  only a stack's standard operations.

Example 1:
Input:
["MyQueue", "push", "push", "peek", "pop", "empty"]
[[], [1], [2], [], [], []]

Output:
[null, null, null, 1, 1, false]

Explanation:
MyQueue myQueue = new MyQueue();
myQueue.push(1); // queue is: [1]
myQueue.push(2); // queue is: [1, 2] (leftmost is front)
myQueue.peek();  // return 1
myQueue.pop();   // return 1, queue is [2]
myQueue.empty(); // return false

Constraints:
- 1 <= x <= 9
- At most 100 calls will be made to push, pop, peek, and empty.
- All the calls to pop and peek are valid.

Follow-up: Can you implement the queue such that each operation is amortized O(1)
time complexity? In other words, performing n operations will take overall O(n)
time even if one of those operations may take longer.
"""


class MyQueue:
    """
    Two-stack queue with amortized O(1) operations.

    Approach:
    1. Use two stacks: in_stack (for push) and out_stack (for pop/peek)
    2. Push always goes to in_stack: O(1)
    3. Pop/peek use out_stack:
       - If out_stack is not empty, pop from it: O(1)
       - If out_stack is empty, move all from in_stack to out_stack: O(n)
    4. Moving reverses order, converting LIFO to FIFO

    Why this works:
    - Stacks are LIFO (last in, first out)
    - Queue is FIFO (first in, first out)
    - Moving between stacks reverses order
    - in_stack: newest on top, out_stack: oldest on top

    Time Complexity:
    - push: O(1) - just append to in_stack
    - pop: O(1) amortized - each element moved once
    - peek: O(1) amortized - same as pop
    - empty: O(1) - check both stacks

    Space Complexity: O(n) - store n elements across two stacks

    Amortized Analysis:
    - An element is pushed once to in_stack: 1 operation
    - An element is moved to out_stack: 1 operation
    - An element is popped from out_stack: 1 operation
    - Total: 3 operations per element = O(1) amortized
    """

    def __init__(self):
        """Initialize two empty stacks."""
        self.in_stack = []    # For push operations
        self.out_stack = []   # For pop/peek operations

    def push(self, x):
        """
        Push element to the back of queue.

        Args:
            x: Element to push

        Time: O(1)
        """
        self.in_stack.append(x)

    def pop(self):
        """
        Remove and return element from front of queue.

        Returns:
            Element at front of queue

        Time: O(1) amortized
        """
        self._move_if_needed()
        return self.out_stack.pop()

    def peek(self):
        """
        Return element at front without removing.

        Returns:
            Element at front of queue

        Time: O(1) amortized
        """
        self._move_if_needed()
        return self.out_stack[-1]

    def empty(self):
        """
        Check if queue is empty.

        Returns:
            True if queue is empty, False otherwise

        Time: O(1)
        """
        return not self.in_stack and not self.out_stack

    def _move_if_needed(self):
        """
        Move elements from in_stack to out_stack if out_stack is empty.

        This is the key operation that converts LIFO to FIFO.
        Only called when we need to access front element.

        Time: O(n) worst case, but amortized O(1)
        """
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())


class MyQueueAlwaysMove:
    """
    Alternative: Move elements on every operation.

    This approach moves elements between stacks on every push or pop.
    NOT recommended - worse time complexity.

    Time Complexity:
    - push: O(n) - move all elements
    - pop: O(1) - just pop from stack
    - peek: O(1) - just peek at stack
    - empty: O(1)

    Space Complexity: O(n)

    This is simpler to understand but inefficient.
    """

    def __init__(self):
        self.stack = []

    def push(self, x):
        """Time: O(n) - move all elements"""
        temp = []
        while self.stack:
            temp.append(self.stack.pop())
        self.stack.append(x)
        while temp:
            self.stack.append(temp.pop())

    def pop(self):
        """Time: O(1)"""
        return self.stack.pop()

    def peek(self):
        """Time: O(1)"""
        return self.stack[-1]

    def empty(self):
        """Time: O(1)"""
        return not self.stack


def test_queue():
    """Test cases for MyQueue implementation."""

    print("Testing MyQueue implementation...\n")

    # Test case 1: Basic operations
    queue = MyQueue()
    queue.push(1)
    queue.push(2)
    assert queue.peek() == 1
    assert queue.pop() == 1
    assert queue.empty() == False
    print("Test 1 passed: Basic operations")

    # Test case 2: Multiple operations
    queue = MyQueue()
    queue.push(1)
    queue.push(2)
    queue.push(3)
    assert queue.pop() == 1
    queue.push(4)
    assert queue.pop() == 2
    assert queue.pop() == 3
    assert queue.pop() == 4
    assert queue.empty() == True
    print("Test 2 passed: Multiple operations")

    # Test case 3: Interleaved push/pop
    queue = MyQueue()
    queue.push(1)
    assert queue.pop() == 1
    queue.push(2)
    queue.push(3)
    assert queue.pop() == 2
    queue.push(4)
    assert queue.pop() == 3
    assert queue.pop() == 4
    print("Test 3 passed: Interleaved operations")

    # Test case 4: Single element
    queue = MyQueue()
    queue.push(1)
    assert queue.peek() == 1
    assert queue.pop() == 1
    assert queue.empty() == True
    print("Test 4 passed: Single element")

    # Test case 5: Many elements
    queue = MyQueue()
    for i in range(1, 11):
        queue.push(i)
    for i in range(1, 11):
        assert queue.pop() == i
    assert queue.empty() == True
    print("Test 5 passed: Many elements")

    print("\nAll tests passed!")


def visualize_operations():
    """Visualize how the two stacks work together."""

    print("\n=== Two-Stack Queue Visualization ===\n")

    queue = MyQueue()

    operations = [
        ("push", 1),
        ("push", 2),
        ("push", 3),
        ("peek", None),
        ("pop", None),
        ("push", 4),
        ("pop", None),
        ("pop", None),
    ]

    for i, (op, val) in enumerate(operations):
        print(f"Step {i+1}: {op}({val if val else ''})")

        if op == "push":
            queue.push(val)
            print(f"  Pushed {val} to in_stack")
        elif op == "pop":
            result = queue.pop()
            print(f"  Popped {result} from queue")
        elif op == "peek":
            result = queue.peek()
            print(f"  Peeked {result} (front of queue)")

        print(f"  in_stack (push here):  {queue.in_stack} (top is right)")
        print(f"  out_stack (pop here):  {queue.out_stack} (top is right)")

        # Show logical queue order
        logical = list(reversed(queue.out_stack)) + queue.in_stack
        print(f"  Logical queue order:   {logical} (front is left)")
        print()


def explain_amortization():
    """Explain amortized O(1) complexity."""

    print("\n=== Understanding Amortized O(1) ===\n")

    print("What is Amortized Analysis?")
    print("  Look at average cost over many operations")
    print("  Some operations may be expensive, but rare")
    print("  Total cost for n operations is O(n)")
    print("  Therefore, average per operation is O(1)")
    print()

    print("For Queue Using Stacks:")
    print("  Push: Always O(1) - just append to in_stack")
    print("  Pop: Usually O(1), occasionally O(n)")
    print()

    print("When is Pop expensive?")
    print("  Only when out_stack is empty")
    print("  Must move all elements from in_stack")
    print("  This costs O(k) where k = elements in in_stack")
    print()

    print("Why is it still O(1) amortized?")
    print("  Each element is:")
    print("    1. Pushed to in_stack: 1 operation")
    print("    2. Moved to out_stack: 1 operation (once in lifetime)")
    print("    3. Popped from out_stack: 1 operation")
    print("  Total: 3 operations per element")
    print("  For n elements: 3n operations = O(n)")
    print("  Average per element: O(n)/n = O(1)")
    print()

    print("Key Insight:")
    print("  Each element moves between stacks AT MOST ONCE")
    print("  So we're not repeatedly doing expensive operations")
    print()


def demonstrate_amortization():
    """Demonstrate amortized cost with timing."""

    import time

    print("\n=== Demonstrating Amortized Cost ===\n")

    queue = MyQueue()
    n = 1000

    # Push n elements
    print(f"Pushing {n} elements...")
    for i in range(n):
        queue.push(i)
    print(f"  in_stack has {len(queue.in_stack)} elements")
    print(f"  out_stack has {len(queue.out_stack)} elements")
    print()

    # Pop n elements and time them
    print(f"Popping {n} elements and timing each batch of 100...")
    times = []

    for batch in range(n // 100):
        start = time.perf_counter()

        for _ in range(100):
            queue.pop()

        elapsed = time.perf_counter() - start
        times.append(elapsed)

        if batch < 3 or batch == n // 100 - 1:
            print(f"  Batch {batch+1}: {elapsed*1000:.4f}ms")
            if batch == 0:
                print(f"    (First batch includes moving {n} elements)")

    print()
    print(f"Total time: {sum(times)*1000:.4f}ms")
    print(f"Average per batch: {sum(times)/len(times)*1000:.4f}ms")
    print(f"Average per element: {sum(times)/n*1000000:.4f}µs")
    print()
    print("Notice: First batch is expensive (moving elements)")
    print("        But subsequent batches are fast (direct pop)")
    print("        Overall average is O(1)")


def compare_implementations():
    """Compare different implementations."""

    import time

    print("\n=== Comparing Implementations ===\n")

    implementations = [
        ("Amortized O(1)", MyQueue),
        ("Always Move O(n)", MyQueueAlwaysMove)
    ]

    operations = 1000

    for name, QueueClass in implementations:
        queue = QueueClass()

        start = time.perf_counter()

        # Interleaved push and pop
        for i in range(operations):
            queue.push(i)
            if i % 2 == 1:
                queue.pop()

        elapsed = time.perf_counter() - start

        print(f"{name}:")
        print(f"  Time for {operations} operations: {elapsed*1000:.4f}ms")
        print(f"  Average per operation: {elapsed/operations*1000000:.4f}µs")
        print()


if __name__ == "__main__":
    # Run tests
    test_queue()

    # Visualize operations
    visualize_operations()

    # Explain amortization
    explain_amortization()

    # Demonstrate amortization
    demonstrate_amortization()

    # Compare implementations
    compare_implementations()

    print("\n=== Key Takeaways ===\n")
    print("1. Two stacks can implement a queue")
    print("2. Use one stack for push, one for pop")
    print("3. Moving between stacks reverses order (LIFO → FIFO)")
    print("4. Each element moved at most once = O(1) amortized")
    print("5. This is a classic interview question!")
