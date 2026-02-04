"""
Subarray Sum Equals K (LeetCode #560)

Problem:
Given an array of integers 'nums' and an integer 'k', return the total number
of subarrays whose sum equals to k.

A subarray is a contiguous non-empty sequence of elements within an array.

Example 1:
Input: nums = [1,1,1], k = 2
Output: 2
Explanation: There are 2 subarrays with sum 2: [1,1] and [1,1]

Example 2:
Input: nums = [1,2,3], k = 3
Output: 2
Explanation: Subarrays are [1,2] and [3]

Example 3:
Input: nums = [1,-1,1,-1], k = 0
Output: 4
Explanation: [1,-1], [-1,1], [1,-1,1,-1], and [-1,1,-1] (overlapping)

Constraints:
- 1 <= nums.length <= 2 * 10^4
- -1000 <= nums[i] <= 1000
- -10^7 <= k <= 10^7
"""


def subarray_sum_brute_force(nums, k):
    """
    Brute force approach - try all subarrays.

    Approach:
    1. For each starting index i
    2. Try all ending indices j >= i
    3. Calculate sum of subarray [i:j+1]
    4. Count how many equal k

    Time Complexity: O(n³) - nested loops + sum calculation
    Space Complexity: O(1)

    Args:
        nums: List of integers
        k: Target sum

    Returns:
        Count of subarrays with sum k
    """
    count = 0
    n = len(nums)

    for i in range(n):
        for j in range(i, n):
            # Calculate sum of subarray [i:j+1]
            subarray_sum = sum(nums[i:j+1])

            if subarray_sum == k:
                count += 1

    return count


def subarray_sum_optimized_brute(nums, k):
    """
    Optimized brute force - accumulate sum instead of recalculating.

    Approach:
    1. For each starting index i
    2. Maintain running sum as we extend to j
    3. No need to recalculate sum each time

    Time Complexity: O(n²) - nested loops, no sum recalculation
    Space Complexity: O(1)

    Args:
        nums: List of integers
        k: Target sum

    Returns:
        Count of subarrays with sum k
    """
    count = 0
    n = len(nums)

    for i in range(n):
        current_sum = 0

        for j in range(i, n):
            # Add current element to running sum
            current_sum += nums[j]

            if current_sum == k:
                count += 1

    return count


def subarray_sum(nums, k):
    """
    Optimal approach using prefix sum + hash map.

    Approach:
    1. Use prefix sum: sum from start to current index
    2. Store frequency of each prefix sum in hash map
    3. For current prefix_sum, check if (prefix_sum - k) exists
    4. If yes, those are valid subarrays ending at current position

    Why this works:
    - If sum[0:i] - sum[0:j] = k, then sum[j+1:i] = k
    - sum[0:i] - k = sum[0:j]
    - So we look for (current_prefix_sum - k) in our map

    Key insight:
    - prefix_sum[j] = sum of nums[0:j+1]
    - prefix_sum[i] - prefix_sum[j] = sum of nums[j+1:i+1]
    - If prefix_sum[i] - prefix_sum[j] = k
    - Then prefix_sum[j] = prefix_sum[i] - k

    Time Complexity: O(n) - single pass
    Space Complexity: O(n) - hash map stores prefix sums

    Args:
        nums: List of integers
        k: Target sum

    Returns:
        Count of subarrays with sum k
    """
    count = 0
    prefix_sum = 0
    sum_freq = {0: 1}  # Initialize with 0:1 for subarrays starting at index 0

    for num in nums:
        # Update prefix sum
        prefix_sum += num

        # Check if (prefix_sum - k) exists
        # If yes, we found subarrays ending at current position
        if prefix_sum - k in sum_freq:
            count += sum_freq[prefix_sum - k]

        # Store current prefix sum frequency
        sum_freq[prefix_sum] = sum_freq.get(prefix_sum, 0) + 1

    return count


def find_subarray_indices(nums, k):
    """
    Extension: Return indices of all subarrays that sum to k.

    Returns list of tuples (start, end) for each valid subarray.

    Time Complexity: O(n²) worst case
    Space Complexity: O(n)
    """
    result = []
    prefix_sum = 0
    sum_indices = {0: [-1]}  # Map sum to list of indices

    for i, num in enumerate(nums):
        prefix_sum += num

        # Check if we can form subarray with sum k
        target = prefix_sum - k
        if target in sum_indices:
            for start_idx in sum_indices[target]:
                result.append((start_idx + 1, i))

        # Store current prefix sum and index
        if prefix_sum not in sum_indices:
            sum_indices[prefix_sum] = []
        sum_indices[prefix_sum].append(i)

    return result


def visualize_subarray_sum(nums, k):
    """
    Helper function to visualize the prefix sum approach.

    Shows step-by-step how the algorithm works.
    """
    print(f"\nFinding subarrays in {nums} that sum to {k}")
    print("=" * 70)

    count = 0
    prefix_sum = 0
    sum_freq = {0: 1}

    print("\nInitial state:")
    print(f"  sum_freq = {sum_freq}")
    print(f"  Explanation: {0: 1} handles subarrays starting at index 0\n")

    for i, num in enumerate(nums):
        prefix_sum += num
        target = prefix_sum - k

        print(f"Step {i + 1}: Processing nums[{i}] = {num}")
        print(f"  Current prefix_sum = {prefix_sum}")
        print(f"  Looking for: prefix_sum - k = {prefix_sum} - {k} = {target}")

        if target in sum_freq:
            occurrences = sum_freq[target]
            count += occurrences
            print(f"  ✓ Found {target} in map with frequency {occurrences}")
            print(f"  → This means {occurrences} subarray(s) ending here sum to {k}")
            print(f"  → Total count: {count}")
        else:
            print(f"  ✗ {target} not in map")

        sum_freq[prefix_sum] = sum_freq.get(prefix_sum, 0) + 1
        print(f"  Updated sum_freq[{prefix_sum}] = {sum_freq[prefix_sum]}")
        print(f"  Current map: {sum_freq}\n")

    print("=" * 70)
    print(f"Final result: {count} subarray(s) with sum {k}")
    return count


def test_subarray_sum():
    """Test cases covering various scenarios."""

    # Test case 1: Multiple overlapping subarrays
    assert subarray_sum([1, 1, 1], 2) == 2
    assert subarray_sum_brute_force([1, 1, 1], 2) == 2

    # Test case 2: Different numbers
    assert subarray_sum([1, 2, 3], 3) == 2
    assert subarray_sum_optimized_brute([1, 2, 3], 3) == 2

    # Test case 3: With negative numbers
    assert subarray_sum([1, -1, 1, -1], 0) == 4

    # Test case 4: Single element equals k
    assert subarray_sum([1], 1) == 1

    # Test case 5: No subarray sums to k
    assert subarray_sum([1, 2, 3], 7) == 0

    # Test case 6: Entire array sums to k
    assert subarray_sum([1, 2, 3], 6) == 1

    # Test case 7: Multiple same elements
    assert subarray_sum([3, 3, 3], 6) == 2

    # Test case 8: k = 0 with positive and negative
    assert subarray_sum([1, -1, 0], 0) == 3

    # Test case 9: Large numbers
    assert subarray_sum([100, 200, 300], 500) == 1

    # Test case 10: All negative
    assert subarray_sum([-1, -2, -3], -3) == 2

    print("All test cases passed!")


if __name__ == "__main__":
    # Run tests
    test_subarray_sum()

    # Example with visualization
    print("\n" + "=" * 70)
    print("EXAMPLE 1: BASIC CASE")
    print("=" * 70)
    visualize_subarray_sum([1, 1, 1], 2)

    print("\n" + "=" * 70)
    print("EXAMPLE 2: WITH NEGATIVE NUMBERS")
    print("=" * 70)
    visualize_subarray_sum([1, -1, 1, -1], 0)

    print("\n" + "=" * 70)
    print("EXAMPLE 3: DIFFERENT NUMBERS")
    print("=" * 70)
    visualize_subarray_sum([1, 2, 3], 3)

    # Compare approaches
    print("\n" + "=" * 70)
    print("COMPARING APPROACHES")
    print("=" * 70)

    test_cases = [
        ([1, 1, 1], 2),
        ([1, 2, 3], 3),
        ([1, -1, 1, -1], 0),
    ]

    for nums, k in test_cases:
        print(f"\nInput: nums = {nums}, k = {k}")

        # Brute force
        result1 = subarray_sum_brute_force(nums, k)
        print(f"Brute Force (O(n³)):        {result1}")

        # Optimized brute force
        result2 = subarray_sum_optimized_brute(nums, k)
        print(f"Optimized Brute (O(n²)):    {result2}")

        # Hash map
        result3 = subarray_sum(nums, k)
        print(f"Prefix Sum + Map (O(n)):    {result3}")

        # Show subarray indices
        indices = find_subarray_indices(nums, k)
        print(f"Subarray ranges: {indices}")
        for start, end in indices:
            subarray = nums[start:end+1]
            print(f"  nums[{start}:{end+1}] = {subarray} (sum = {sum(subarray)})")

    # Detailed explanation
    print("\n" + "=" * 70)
    print("ALGORITHM EXPLANATION")
    print("=" * 70)
    print("""
The key insight is using PREFIX SUMS with a HASH MAP:

1. Prefix Sum Concept:
   - prefix_sum[i] = sum of nums[0] to nums[i]
   - Sum of subarray [j+1, i] = prefix_sum[i] - prefix_sum[j]

2. Finding Subarrays:
   - We want: prefix_sum[i] - prefix_sum[j] = k
   - Rearrange: prefix_sum[j] = prefix_sum[i] - k
   - So at index i, look for (prefix_sum[i] - k) in our map

3. Hash Map Stores:
   - Key: prefix sum value
   - Value: how many times we've seen this sum
   - Why frequency? Multiple subarrays can end at current position

4. Why {0: 1} initialization?
   - Handles subarrays starting at index 0
   - If prefix_sum = k, then prefix_sum - k = 0
   - We need 0 in map to count these subarrays

Example: nums = [1, 2, 3], k = 3

Step 0: sum_freq = {0: 1}

Step 1: num = 1, prefix_sum = 1
  Looking for 1 - 3 = -2 (not in map)
  sum_freq = {0: 1, 1: 1}

Step 2: num = 2, prefix_sum = 3
  Looking for 3 - 3 = 0 (in map with count 1!)
  Found 1 subarray: [1, 2]
  sum_freq = {0: 1, 1: 1, 3: 1}

Step 3: num = 3, prefix_sum = 6
  Looking for 6 - 3 = 3 (in map with count 1!)
  Found 1 subarray: [3]
  sum_freq = {0: 1, 1: 1, 3: 1, 6: 1}

Total: 2 subarrays
    """)

    # Performance comparison
    print("\n" + "=" * 70)
    print("COMPLEXITY ANALYSIS")
    print("=" * 70)
    print("""
Approach              Time         Space      Notes
----------------------------------------------------------
Brute Force           O(n³)        O(1)       Try all + sum
Optimized Brute       O(n²)        O(1)       Running sum
Prefix Sum + Map      O(n)         O(n)       Optimal solution

Key Insights:
1. Hash map enables O(1) lookup of previous prefix sums
2. Store frequencies, not just existence (multiple subarrays)
3. {0: 1} initialization is crucial for edge cases
4. Works with negative numbers (unlike sliding window)
5. Pattern: prefix_sum - k lookup

Common Pitfalls:
- Forgetting {0: 1} initialization
- Using set instead of map (need frequencies)
- Trying sliding window (doesn't work with negatives)
- Not considering multiple subarrays ending at same position

Related Problems Using Same Pattern:
1. Subarray Sum Divisible by K (974)
2. Continuous Subarray Sum (523)
3. Contiguous Array (525) - equal 0s and 1s
4. Binary Subarrays With Sum (930)
5. Longest Well-Performing Interval (1124)
    """)
