"""
Jump Game (LeetCode #55)

Problem:
You are given an integer array nums. You are initially positioned at the array's
first index, and each element in the array represents your maximum jump length
at that position.

Return true if you can reach the last index, or false otherwise.

Example 1:
Input: nums = [2,3,1,1,4]
Output: true
Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.

Example 2:
Input: nums = [3,2,1,0,4]
Output: false
Explanation: You will always arrive at index 3 no matter what. Its maximum jump
length is 0, which makes it impossible to reach the last index.

Constraints:
- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 10^5
"""


def can_jump_greedy(nums):
    """
    Greedy approach - track maximum reachable position.
    
    Greedy Choice: At each position, update the maximum index we can reach.
    If we ever encounter a position beyond our max reach, return False.
    
    Why Greedy Works (Proof):
    - We only care if we CAN reach the end, not the path
    - If position i is reachable and nums[i] = j, then all positions 
      up to i+j are reachable
    - We only need to track the farthest position reachable so far
    - If current position > max reachable, it's impossible
    
    Time Complexity: O(n) - single pass through array
    Space Complexity: O(1) - only tracking one variable
    
    Args:
        nums: List of integers representing jump lengths
        
    Returns:
        Boolean indicating if last index is reachable
    """
    max_reach = 0
    
    for i in range(len(nums)):
        # If current position is beyond what we can reach, impossible
        if i > max_reach:
            return False
        
        # Update maximum reachable position from here
        max_reach = max(max_reach, i + nums[i])
        
        # Early exit: if we can already reach the end
        if max_reach >= len(nums) - 1:
            return True
    
    return True


def can_jump_optimized(nums):
    """
    Slightly optimized version - track furthest reachable.
    
    Same logic but cleaner implementation.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    furthest = 0
    
    for i, jump in enumerate(nums):
        # Can't reach this position
        if i > furthest:
            return False
        
        furthest = max(furthest, i + jump)
    
    return furthest >= len(nums) - 1


def can_jump_backward(nums):
    """
    Alternative greedy - work backwards from end.
    
    Start from end and work backwards, checking if each position
    can reach the target. Move target backwards as we find positions
    that can reach it.
    
    Why this works:
    - If we can move target all the way to index 0, then 0 can reach original end
    - Each step we're making greedy choice: can current position reach target?
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    target = len(nums) - 1
    
    for i in range(len(nums) - 2, -1, -1):
        if i + nums[i] >= target:
            # This position can reach target, move target here
            target = i
    
    return target == 0


# Non-greedy approaches for comparison
def can_jump_dp(nums):
    """
    Dynamic Programming approach (overkill for this problem).
    
    dp[i] = True if index i is reachable
    
    Time Complexity: O(n^2) - worse than greedy
    Space Complexity: O(n)
    
    This shows greedy is superior when it works!
    """
    n = len(nums)
    dp = [False] * n
    dp[0] = True
    
    for i in range(n):
        if not dp[i]:
            continue
            
        # From position i, mark all reachable positions
        for j in range(1, nums[i] + 1):
            if i + j < n:
                dp[i + j] = True
    
    return dp[-1]


def can_jump_bfs(nums):
    """
    BFS approach (also overkill).
    
    Treat as graph where edges connect i to all i+1...i+nums[i].
    
    Time Complexity: O(n^2) worst case
    Space Complexity: O(n) for queue
    """
    if len(nums) <= 1:
        return True
    
    from collections import deque
    queue = deque([0])
    visited = {0}
    target = len(nums) - 1
    
    while queue:
        pos = queue.popleft()
        
        # Try all jumps from current position
        for next_pos in range(pos + 1, min(pos + nums[pos] + 1, len(nums))):
            if next_pos == target:
                return True
            
            if next_pos not in visited:
                visited.add(next_pos)
                queue.append(next_pos)
    
    return False


def test_jump_game():
    """Comprehensive test cases."""
    
    # Test case 1: Can reach end
    assert can_jump_greedy([2, 3, 1, 1, 4]) == True
    assert can_jump_optimized([2, 3, 1, 1, 4]) == True
    assert can_jump_backward([2, 3, 1, 1, 4]) == True
    
    # Test case 2: Cannot reach end (zero blocks path)
    assert can_jump_greedy([3, 2, 1, 0, 4]) == False
    assert can_jump_optimized([3, 2, 1, 0, 4]) == False
    assert can_jump_backward([3, 2, 1, 0, 4]) == False
    
    # Test case 3: Single element
    assert can_jump_greedy([0]) == True
    assert can_jump_optimized([0]) == True
    
    # Test case 4: Two elements, can reach
    assert can_jump_greedy([1, 0]) == True
    assert can_jump_backward([1, 0]) == True
    
    # Test case 5: Two elements, cannot reach
    assert can_jump_greedy([0, 1]) == False
    assert can_jump_backward([0, 1]) == False
    
    # Test case 6: Large jumps
    assert can_jump_greedy([5, 4, 3, 2, 1, 0]) == True
    
    # Test case 7: All zeros except first
    assert can_jump_greedy([2, 0, 0]) == True
    assert can_jump_greedy([1, 0, 0]) == False
    
    # Test case 8: Can barely make it
    assert can_jump_greedy([1, 1, 1, 1]) == True
    
    # Test case 9: Multiple zeros
    assert can_jump_greedy([2, 5, 0, 0]) == True
    
    # Test case 10: Large array
    assert can_jump_greedy([1] * 10000) == True
    
    print("All test cases passed!")


def compare_approaches():
    """Compare different approaches."""
    import time
    
    # Test on larger input
    test_cases = [
        [2, 3, 1, 1, 4],
        [3, 2, 1, 0, 4],
        [1] * 1000,
        [1000] + [0] * 999,
    ]
    
    approaches = [
        ("Greedy (forward)", can_jump_greedy),
        ("Greedy (optimized)", can_jump_optimized),
        ("Greedy (backward)", can_jump_backward),
        ("DP", can_jump_dp),
    ]
    
    for test in test_cases:
        print(f"\nInput size: {len(test)}, First few: {test[:5]}")
        for name, func in approaches:
            start = time.time()
            result = func(test)
            elapsed = time.time() - start
            print(f"  {name:25s}: {str(result):5s} in {elapsed*1000:.3f}ms")


def explain_greedy_proof():
    """
    Detailed explanation of why greedy works.
    
    PROOF BY EXCHANGE ARGUMENT:
    
    Claim: Greedy algorithm (tracking max reach) correctly determines reachability.
    
    Proof:
    1. Define reachable set R = all indices we can reach from index 0
    
    2. Greedy maintains: max_reach = maximum index in R
    
    3. At each step i:
       - If i > max_reach, then i not in R (not reachable)
       - If i <= max_reach, then i in R (reachable)
       - From i, we can reach i+1, i+2, ..., i+nums[i]
       - So max_reach = max(max_reach, i + nums[i])
    
    4. By induction:
       Base: Initially max_reach = 0 (can reach index 0)
       Step: If we can reach i, we extend R by nums[i] positions
       
    5. After processing all reachable positions:
       - If last index <= max_reach, it's reachable (return True)
       - If we encounter i > max_reach, last index not reachable (return False)
    
    6. Greedy choice is correct: we don't need to track paths or decisions,
       only the maximum extent of our reach.
    
    COMPLEXITY ANALYSIS:
    - Time: O(n) - visit each index at most once
    - Space: O(1) - only one variable
    
    VS DYNAMIC PROGRAMMING:
    - DP tracks reachability of each index separately: O(n) space
    - DP explores all edges: O(n^2) time worst case
    - Greedy aggregates information: O(n) time, O(1) space
    - Greedy works because we only need existence, not paths
    """
    print(__doc__)


if __name__ == "__main__":
    test_jump_game()
    
    print("\n" + "="*60)
    print("Example Usage:")
    print("="*60)
    
    # Example 1
    nums = [2, 3, 1, 1, 4]
    result = can_jump_greedy(nums)
    print(f"Input: nums = {nums}")
    print(f"Output: {result}")
    print(f"Explanation: Jump from 0→1→4 (or other paths)")
    
    print()
    
    # Example 2
    nums = [3, 2, 1, 0, 4]
    result = can_jump_greedy(nums)
    print(f"Input: nums = {nums}")
    print(f"Output: {result}")
    print(f"Explanation: All paths lead to index 3 (value 0), can't proceed")
    
    print("\n" + "="*60)
    print("Greedy Correctness Proof:")
    print("="*60)
    explain_greedy_proof()
    
    print("\n" + "="*60)
    print("Performance Comparison:")
    print("="*60)
    compare_approaches()
