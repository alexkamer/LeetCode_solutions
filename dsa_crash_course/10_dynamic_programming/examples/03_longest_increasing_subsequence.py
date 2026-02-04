"""
Longest Increasing Subsequence (LeetCode #300)

Problem:
Given an integer array nums, return the length of the longest strictly
increasing subsequence.

A subsequence is a sequence that can be derived from an array by deleting
some or no elements without changing the order of the remaining elements.

Example 1:
Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: The longest increasing subsequence is [2,3,7,101], therefore
the length is 4.

Example 2:
Input: nums = [0,1,0,3,2,3]
Output: 4

Example 3:
Input: nums = [7,7,7,7,7,7,7]
Output: 1

Constraints:
- 1 <= nums.length <= 2500
- -10^4 <= nums[i] <= 10^4
"""


def length_of_lis_dp(nums):
    """
    Dynamic Programming approach - O(n²) solution.

    Intuition:
    For each position i, find the length of the longest increasing
    subsequence that ENDS at position i. To do this, look at all
    previous positions j where nums[j] < nums[i], and extend their
    subsequences.

    State Definition:
    dp[i] = length of longest increasing subsequence ending at index i

    Recurrence Relation:
    dp[i] = max(dp[j] + 1) for all j < i where nums[j] < nums[i]

    Base Case:
    dp[i] = 1 (each element is a subsequence of length 1)

    Example: [10,9,2,5,3,7,101,18]
    dp[0] = 1: [10]
    dp[1] = 1: [9]
    dp[2] = 1: [2]
    dp[3] = 2: [2,5]
    dp[4] = 2: [2,3]
    dp[5] = 3: [2,3,7] or [2,5,7]
    dp[6] = 4: [2,3,7,101] or [2,5,7,101]
    dp[7] = 4: [2,3,7,18] or [2,5,7,18]

    Time Complexity: O(n²)
    - Outer loop: n iterations
    - Inner loop: up to n iterations
    - Total: n × n

    Space Complexity: O(n) - dp array

    Args:
        nums: List of integers

    Returns:
        Length of longest increasing subsequence
    """
    if not nums:
        return 0

    n = len(nums)
    # dp[i] = length of LIS ending at index i
    dp = [1] * n  # Each element is a subsequence of length 1

    # For each position i
    for i in range(1, n):
        # Look at all previous positions j
        for j in range(i):
            # If we can extend the subsequence ending at j
            if nums[j] < nums[i]:
                # Update dp[i] if extending j gives longer subsequence
                dp[i] = max(dp[i], dp[j] + 1)

    # Answer is the maximum value in dp array
    return max(dp)


def length_of_lis_binary_search(nums):
    """
    Optimized approach using binary search - O(n log n).

    Intuition:
    Maintain an array 'tails' where tails[i] is the smallest ending
    element of all increasing subsequences of length i+1.

    Key Insight:
    - If a new number is larger than all tails, append it (longer LIS)
    - Otherwise, find the smallest tail that is >= new number and replace it
      (this maintains a smaller ending value for that length)

    Why this works:
    - We want to keep ending values as small as possible
    - This gives us more room to extend subsequences later
    - Binary search finds the right position to update

    Example: [10,9,2,5,3,7,101,18]

    Initially: tails = []
    Process 10: tails = [10]           (LIS length 1)
    Process 9:  tails = [9]            (replace 10, keep ending small)
    Process 2:  tails = [2]            (replace 9)
    Process 5:  tails = [2,5]          (append, now have length 2)
    Process 3:  tails = [2,3]          (replace 5 with smaller 3)
    Process 7:  tails = [2,3,7]        (append, now have length 3)
    Process 101: tails = [2,3,7,101]   (append, now have length 4)
    Process 18: tails = [2,3,7,18]     (replace 101 with smaller 18)

    Time Complexity: O(n log n)
    - n iterations
    - Binary search takes O(log n)

    Space Complexity: O(n) - tails array (worst case)

    Args:
        nums: List of integers

    Returns:
        Length of longest increasing subsequence
    """
    if not nums:
        return 0

    # tails[i] = smallest tail of all increasing subsequences of length i+1
    tails = []

    for num in nums:
        # Binary search to find position to insert/replace
        left, right = 0, len(tails)

        while left < right:
            mid = (left + right) // 2
            if tails[mid] < num:
                left = mid + 1
            else:
                right = mid

        # If left == len(tails), append (found new longer subsequence)
        if left == len(tails):
            tails.append(num)
        else:
            # Replace to keep smaller ending value
            tails[left] = num

    # Length of LIS is length of tails array
    return len(tails)


def length_of_lis_with_sequence(nums):
    """
    DP approach that also returns the actual LIS.

    Approach:
    Same as DP approach, but track parent pointers to reconstruct
    the actual sequence.

    Returns:
        Tuple of (length, sequence)
    """
    if not nums:
        return 0, []

    n = len(nums)
    dp = [1] * n
    parent = [-1] * n  # Track previous element in LIS

    # Build dp array and track parents
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                parent[i] = j  # j is previous element in LIS ending at i

    # Find the index with maximum LIS length
    max_length = max(dp)
    max_idx = dp.index(max_length)

    # Reconstruct the sequence by following parent pointers
    sequence = []
    idx = max_idx
    while idx != -1:
        sequence.append(nums[idx])
        idx = parent[idx]

    sequence.reverse()
    return max_length, sequence


def visualize_lis_building(nums):
    """
    Visualize how the DP array is built for LIS.
    Shows the subsequence ending at each position.
    """
    if not nums:
        return

    print(f"Finding LIS in: {nums}")
    print("=" * 60)

    n = len(nums)
    dp = [1] * n
    parent = [-1] * n

    print(f"Position 0: nums[0]={nums[0]}")
    print(f"  dp[0] = 1, LIS = [{nums[0]}]\n")

    for i in range(1, n):
        print(f"Position {i}: nums[{i}]={nums[i]}")

        candidates = []
        for j in range(i):
            if nums[j] < nums[i]:
                candidates.append((j, dp[j] + 1))
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    parent[i] = j

        if candidates:
            print(f"  Can extend from positions: ", end="")
            for j, length in candidates:
                marker = "✓" if parent[i] == j else " "
                print(f"{marker}j={j}(len={length}) ", end="")
            print()
        else:
            print(f"  Cannot extend any previous subsequence")

        # Show the LIS ending at position i
        seq = []
        idx = i
        while idx != -1:
            seq.append(nums[idx])
            idx = parent[idx]
        seq.reverse()
        print(f"  dp[{i}] = {dp[i]}, LIS ending here = {seq}\n")

    max_length = max(dp)
    max_idx = dp.index(max_length)

    # Reconstruct full LIS
    sequence = []
    idx = max_idx
    while idx != -1:
        sequence.append(nums[idx])
        idx = parent[idx]
    sequence.reverse()

    print(f"Final answer: length = {max_length}")
    print(f"One possible LIS: {sequence}")


def compare_approaches():
    """Compare the two main approaches."""
    import time

    test_arrays = [
        [10,9,2,5,3,7,101,18],
        list(range(100, 0, -1)),  # Decreasing
        list(range(100)),  # Increasing
    ]

    print("Performance Comparison:")
    print("=" * 60)

    for nums in test_arrays:
        print(f"\nArray size: {len(nums)}")

        # DP O(n²)
        start = time.time()
        result_dp = length_of_lis_dp(nums)
        time_dp = time.time() - start

        # Binary Search O(n log n)
        start = time.time()
        result_bs = length_of_lis_binary_search(nums)
        time_bs = time.time() - start

        print(f"LIS length: {result_dp}")
        print(f"DP O(n²):         {time_dp*1000:.4f} ms")
        print(f"Binary Search:    {time_bs*1000:.4f} ms")
        print(f"Speedup:          {time_dp/time_bs:.2f}x")


def test_lis():
    """Test cases covering various scenarios."""

    # Test case 1: Standard case
    assert length_of_lis_dp([10,9,2,5,3,7,101,18]) == 4
    assert length_of_lis_binary_search([10,9,2,5,3,7,101,18]) == 4

    # Test case 2: Multiple valid LIS
    assert length_of_lis_dp([0,1,0,3,2,3]) == 4

    # Test case 3: All same
    assert length_of_lis_dp([7,7,7,7,7,7,7]) == 1

    # Test case 4: Already increasing
    assert length_of_lis_dp([1,2,3,4,5]) == 5

    # Test case 5: Decreasing
    assert length_of_lis_dp([5,4,3,2,1]) == 1

    # Test case 6: Single element
    assert length_of_lis_dp([1]) == 1

    # Test case 7: Two elements increasing
    assert length_of_lis_dp([1,2]) == 2

    # Test case 8: Two elements decreasing
    assert length_of_lis_dp([2,1]) == 1

    # Verify with sequence reconstruction
    length, seq = length_of_lis_with_sequence([10,9,2,5,3,7,101,18])
    assert length == 4
    assert len(seq) == 4
    # Verify it's increasing
    for i in range(len(seq) - 1):
        assert seq[i] < seq[i+1]

    # Both approaches should give same answer
    test_cases = [
        [10,9,2,5,3,7,101,18],
        [0,1,0,3,2,3],
        [7,7,7,7,7,7,7],
        [1,2,3,4,5],
        [5,4,3,2,1],
    ]

    for nums in test_cases:
        dp_result = length_of_lis_dp(nums)
        bs_result = length_of_lis_binary_search(nums)
        assert dp_result == bs_result, \
            f"Mismatch for {nums}: dp={dp_result}, bs={bs_result}"

    print("All test cases passed!")


if __name__ == "__main__":
    # Run tests
    test_lis()
    print()

    # Visualize DP building
    visualize_lis_building([10,9,2,5,3,7,101,18])
    print()

    # Compare performance
    compare_approaches()
    print()

    # Example with actual sequence
    nums = [10,9,2,5,3,7,101,18]
    length, sequence = length_of_lis_with_sequence(nums)
    print(f"Example: nums = {nums}")
    print(f"LIS length: {length}")
    print(f"One possible LIS: {sequence}")
    print("\nNote: There may be multiple valid LIS of the same length.")
    print("For example, [2,5,7,101] and [2,3,7,101] are both valid.")
