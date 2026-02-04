"""
Min Stack (LeetCode #155)

Problem:
Design a stack that supports push, pop, top, and retrieving the minimum element
in constant time.

Implement the MinStack class:
- MinStack() initializes the stack object.
- void push(int val) pushes the element val onto the stack.
- void pop() removes the element on the top of the stack.
- int top() gets the top element of the stack.
- int getMin() retrieves the minimum element in the stack.

You must implement a solution with O(1) time complexity for each function.

Example 1:
Input:
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]

Output:
[null,null,null,null,-3,null,0,-2]

Explanation:
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin(); // return -3
minStack.pop();
minStack.top();    // return 0
minStack.getMin(); // return -2

Constraints:
- -2^31 <= val <= 2^31 - 1
- pop, top and getMin operations will always be called on non-empty stacks.
- At most 3 * 10^4 calls will be made to push, pop, top, and getMin.
"""


class MinStack:
    """
    Two-stack approach - maintains parallel stack of minimums.

    Approach:
    1. Use one stack for actual values
    2. Use another stack to track minimum at each level
    3. When pushing, calculate new min and push to both stacks
    4. When popping, pop from both stacks
    5. getMin just returns top of min_stack

    Why this works:
    - Each position in min_stack stores the minimum of all elements
      at or below that position in the main stack
    - When we pop, the previous minimum is revealed
    - All operations are O(1) stack operations

    Time Complexity:
    - push: O(1)
    - pop: O(1)
    - top: O(1)
    - getMin: O(1)

    Space Complexity: O(n) - need space for both stacks
    """

    def __init__(self):
        """Initialize empty stacks."""
        self.stack = []
        self.min_stack = []

    def push(self, val):
        """
        Push element to stack and update minimum.

        Args:
            val: Value to push
        """
        self.stack.append(val)

        # Calculate new minimum
        if self.min_stack:
            current_min = min(val, self.min_stack[-1])
        else:
            current_min = val

        self.min_stack.append(current_min)

    def pop(self):
        """Remove top element from stack."""
        self.stack.pop()
        self.min_stack.pop()

    def top(self):
        """
        Get top element without removing it.

        Returns:
            Top element of stack
        """
        return self.stack[-1]

    def get_min(self):
        """
        Get minimum element in O(1) time.

        Returns:
            Minimum element in stack
        """
        return self.min_stack[-1]


class MinStackOptimized:
    """
    Space-optimized approach - only store min when it changes.

    Approach:
    - Only push to min_stack when new value is <= current min
    - When popping, only pop from min_stack if value equals current min
    - This reduces space usage when there are many elements larger than min

    Time Complexity: O(1) for all operations
    Space Complexity: O(n) worst case, but typically better in practice
    """

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)

        # Only push to min_stack if it's a new minimum
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self):
        val = self.stack.pop()

        # Only pop from min_stack if we're removing the minimum
        if val == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def get_min(self):
        return self.min_stack[-1]


class MinStackSingleStack:
    """
    Single-stack approach - store (value, min) pairs.

    Approach:
    - Each element in stack is a tuple (value, min_at_this_level)
    - More intuitive but uses more space per element

    Time Complexity: O(1) for all operations
    Space Complexity: O(n) - storing tuples
    """

    def __init__(self):
        self.stack = []  # Store (value, min) pairs

    def push(self, val):
        if not self.stack:
            self.stack.append((val, val))
        else:
            current_min = min(val, self.stack[-1][1])
            self.stack.append((val, current_min))

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1][0]

    def get_min(self):
        return self.stack[-1][1]


class MinStackDifference:
    """
    Space-efficient approach using differences (advanced).

    Approach:
    - Store differences from minimum instead of actual values
    - Only store one minimum value
    - More complex but uses less space

    Time Complexity: O(1) for all operations
    Space Complexity: O(n) but more memory efficient

    Note: This approach is more complex and has overflow concerns.
    Not recommended for interviews unless specifically asked for
    space optimization.
    """

    def __init__(self):
        self.stack = []
        self.min_val = None

    def push(self, val):
        if not self.stack:
            self.stack.append(0)
            self.min_val = val
        else:
            # Store difference from current min
            diff = val - self.min_val
            self.stack.append(diff)

            # Update min if necessary
            if val < self.min_val:
                self.min_val = val

    def pop(self):
        diff = self.stack.pop()

        # If diff is negative, we're popping the min
        if diff < 0:
            # Restore previous min
            self.min_val = self.min_val - diff

    def top(self):
        diff = self.stack[-1]

        if diff < 0:
            return self.min_val
        else:
            return self.min_val + diff

    def get_min(self):
        return self.min_val


def test_min_stack():
    """Test cases for MinStack implementations."""

    # Test all implementations
    implementations = [
        ("Two Stack", MinStack),
        ("Optimized", MinStackOptimized),
        ("Single Stack", MinStackSingleStack),
        ("Difference", MinStackDifference)
    ]

    for name, StackClass in implementations:
        print(f"\nTesting {name} implementation...")

        # Test case 1: Basic operations
        stack = StackClass()
        stack.push(-2)
        stack.push(0)
        stack.push(-3)
        assert stack.get_min() == -3
        stack.pop()
        assert stack.top() == 0
        assert stack.get_min() == -2

        # Test case 2: Duplicates
        stack = StackClass()
        stack.push(2)
        stack.push(2)
        stack.push(1)
        stack.push(1)
        assert stack.get_min() == 1
        stack.pop()
        assert stack.get_min() == 1
        stack.pop()
        assert stack.get_min() == 2

        # Test case 3: Decreasing sequence
        stack = StackClass()
        stack.push(5)
        stack.push(4)
        stack.push(3)
        stack.push(2)
        stack.push(1)
        assert stack.get_min() == 1
        stack.pop()
        assert stack.get_min() == 2

        # Test case 4: Increasing sequence
        stack = StackClass()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        stack.push(4)
        stack.push(5)
        assert stack.get_min() == 1
        stack.pop()
        assert stack.get_min() == 1

        # Test case 5: Negative numbers
        stack = StackClass()
        stack.push(-5)
        stack.push(-3)
        stack.push(-7)
        assert stack.get_min() == -7
        stack.pop()
        assert stack.get_min() == -5

        print(f"  {name} passed all tests!")

    print("\nAll implementations passed!")


def demonstrate_min_tracking():
    """Demonstrate how minimum is tracked through operations."""

    print("\n=== Min Tracking Demonstration ===\n")

    stack = MinStack()

    operations = [
        ("push", -2),
        ("push", 0),
        ("push", -3),
        ("getMin", None),
        ("pop", None),
        ("top", None),
        ("getMin", None)
    ]

    for op, val in operations:
        if op == "push":
            stack.push(val)
            print(f"push({val})")
            print(f"  Stack: {stack.stack}")
            print(f"  Min Stack: {stack.min_stack}")
            print(f"  Current min: {stack.get_min()}")
        elif op == "pop":
            print(f"pop()")
            stack.pop()
            print(f"  Stack: {stack.stack}")
            print(f"  Min Stack: {stack.min_stack}")
            if stack.stack:
                print(f"  Current min: {stack.get_min()}")
        elif op == "top":
            result = stack.top()
            print(f"top() = {result}")
        elif op == "getMin":
            result = stack.get_min()
            print(f"getMin() = {result}")

        print()


def compare_space_usage():
    """Compare space usage of different implementations."""

    print("\n=== Space Usage Comparison ===\n")

    import sys

    # Create identical sequences in each implementation
    values = [5, 3, 7, 2, 8, 1, 9, 4]

    implementations = [
        ("Two Stack", MinStack),
        ("Optimized", MinStackOptimized),
        ("Single Stack", MinStackSingleStack)
    ]

    for name, StackClass in implementations:
        stack = StackClass()
        for val in values:
            stack.push(val)

        # Rough space calculation
        if name == "Two Stack":
            space = len(stack.stack) + len(stack.min_stack)
            print(f"{name}:")
            print(f"  Main stack: {stack.stack}")
            print(f"  Min stack: {stack.min_stack}")
            print(f"  Total elements stored: {space}")

        elif name == "Optimized":
            space = len(stack.stack) + len(stack.min_stack)
            print(f"{name}:")
            print(f"  Main stack: {stack.stack}")
            print(f"  Min stack: {stack.min_stack}")
            print(f"  Total elements stored: {space}")
            print(f"  Savings: Only stores {len(stack.min_stack)} mins instead of {len(stack.stack)}")

        elif name == "Single Stack":
            space = len(stack.stack)
            print(f"{name}:")
            print(f"  Stack (val, min): {stack.stack}")
            print(f"  Total tuples stored: {space}")

        print()


if __name__ == "__main__":
    # Run tests
    test_min_stack()

    # Demonstrate min tracking
    demonstrate_min_tracking()

    # Compare space usage
    compare_space_usage()

    # Interactive demonstration
    print("\n=== Interactive Demonstration ===\n")
    print("Creating MinStack and performing operations...\n")

    min_stack = MinStack()

    print("push(5)")
    min_stack.push(5)
    print(f"  Min: {min_stack.get_min()}")

    print("\npush(3)")
    min_stack.push(3)
    print(f"  Min: {min_stack.get_min()}")

    print("\npush(7)")
    min_stack.push(7)
    print(f"  Min: {min_stack.get_min()}")

    print("\npush(1)")
    min_stack.push(1)
    print(f"  Min: {min_stack.get_min()}")

    print("\npop()")
    min_stack.pop()
    print(f"  Min: {min_stack.get_min()}")

    print("\npop()")
    min_stack.pop()
    print(f"  Min: {min_stack.get_min()}")
