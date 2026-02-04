"""
Longest Consecutive Sequence (LeetCode #128)

Problem:
Given an unsorted array of integers 'nums', return the length of the longest
consecutive elements sequence.

You must write an algorithm that runs in O(n) time.

Example 1:
Input: nums = [100,4,200,1,3,2]
Output: 4
Explanation: The longest consecutive sequence is [1, 2, 3, 4]. Length is 4.

Example 2:
Input: nums = [0,3,7,2,5,8,4,6,0,1]
Output: 9
Explanation: The longest consecutive sequence is [0,1,2,3,4,5,6,7,8]. Length is 9.

Example 3:
Input: nums = [9,1,4,7,3,-1,0,5,8,-2,6,2]
Output: 7
Explanation: Sequence is [-2,-1,0,1,2,3,4]. Length is 7.

Constraints:
- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
"""


def longest_consecutive_brute_force(nums):
    """
    Brute force approach - check sequence for each number.

    Approach:
    1. For each number, try to build longest sequence starting from it
    2. Check if num+1, num+2, num+3... exist in array
    3. Track maximum length found

    Time Complexity: O(n³) - for each num, search for consecutive nums
    Space Complexity: O(1)

    Args:
        nums: List of integers

    Returns:
        Length of longest consecutive sequence
    """
    if not nums:
        return 0

    max_length = 1

    for num in nums:
        current = num
        current_length = 1

        # Build sequence starting from num
        while current + 1 in nums:
            current += 1
            current_length += 1

        max_length = max(max_length, current_length)

    return max_length


def longest_consecutive_sorting(nums):
    """
    Sorting approach - sort and find longest consecutive run.

    Approach:
    1. Sort the array
    2. Scan through sorted array
    3. Count consecutive increasing sequences
    4. Handle duplicates

    Time Complexity: O(n log n) - dominated by sorting
    Space Complexity: O(1) or O(n) - depends on sorting algorithm

    Args:
        nums: List of integers

    Returns:
        Length of longest consecutive sequence
    """
    if not nums:
        return 0

    nums = sorted(nums)
    max_length = 1
    current_length = 1

    for i in range(1, len(nums)):
        # Skip duplicates
        if nums[i] == nums[i - 1]:
            continue

        # Check if consecutive
        if nums[i] == nums[i - 1] + 1:
            current_length += 1
        else:
            # Sequence broken, reset
            max_length = max(max_length, current_length)
            current_length = 1

    # Don't forget to check last sequence
    max_length = max(max_length, current_length)

    return max_length


def longest_consecutive(nums):
    """
    Optimal hash set approach - O(n) time.

    Approach:
    1. Convert array to set for O(1) lookup
    2. For each number, check if it's the START of a sequence
       - A number is a start if (num - 1) doesn't exist
    3. If it's a start, count consecutive numbers
    4. Track maximum length

    Why this works:
    - Only start counting from sequence beginnings
    - Avoids recounting same sequence multiple times
    - Each number checked at most twice (once as start, once as next)

    Key insight:
    - Don't start counting from every number
    - Only count from sequence starts: when (num - 1) not in set
    - This ensures O(n) time

    Time Complexity: O(n) - each element accessed at most twice
    Space Complexity: O(n) - hash set stores all elements

    Args:
        nums: List of integers

    Returns:
        Length of longest consecutive sequence
    """
    if not nums:
        return 0

    num_set = set(nums)
    max_length = 0

    for num in num_set:
        # Only start counting if this is the beginning of a sequence
        if num - 1 not in num_set:
            current_num = num
            current_length = 1

            # Count consecutive numbers
            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1

            max_length = max(max_length, current_length)

    return max_length


def find_longest_consecutive_sequence(nums):
    """
    Extension: Return the actual sequence, not just length.

    Returns the longest consecutive sequence as a list.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not nums:
        return []

    num_set = set(nums)
    max_length = 0
    best_start = None

    for num in num_set:
        if num - 1 not in num_set:
            current_num = num
            current_length = 1

            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1

            if current_length > max_length:
                max_length = current_length
                best_start = num

    # Build the sequence
    if best_start is not None:
        return list(range(best_start, best_start + max_length))

    return []


def find_all_consecutive_sequences(nums):
    """
    Extension: Find all maximal consecutive sequences.

    Returns list of all consecutive sequences of length >= 2.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not nums:
        return []

    num_set = set(nums)
    sequences = []

    for num in num_set:
        # Start of a sequence
        if num - 1 not in num_set:
            sequence = [num]
            current = num

            while current + 1 in num_set:
                current += 1
                sequence.append(current)

            # Only include sequences of length >= 2
            if len(sequence) >= 2:
                sequences.append(sequence)

    return sequences


def visualize_longest_consecutive(nums):
    """
    Helper function to visualize the hash set approach.

    Shows step-by-step how the algorithm works.
    """
    print(f"\nFinding longest consecutive sequence in: {nums}")
    print("=" * 70)

    if not nums:
        print("Empty array, length = 0")
        return 0

    num_set = set(nums)
    print(f"\nHash Set: {sorted(num_set)}")
    print("\nProcessing each number:")
    print("-" * 70)

    max_length = 0
    best_sequence_start = None

    for num in sorted(num_set):
        is_start = num - 1 not in num_set

        print(f"\nNumber: {num}")
        print(f"  Is start of sequence? {is_start}")

        if not is_start:
            print(f"  Skipping (not a sequence start)")
            continue

        # Count sequence
        current_num = num
        current_length = 1
        sequence = [num]

        while current_num + 1 in num_set:
            current_num += 1
            current_length += 1
            sequence.append(current_num)

        print(f"  Sequence: {sequence}")
        print(f"  Length: {current_length}")

        if current_length > max_length:
            max_length = current_length
            best_sequence_start = num
            print(f"  ✓ New maximum!")

    print("\n" + "=" * 70)
    if best_sequence_start is not None:
        best_sequence = list(range(best_sequence_start, best_sequence_start + max_length))
        print(f"Longest consecutive sequence: {best_sequence}")
        print(f"Length: {max_length}")
    else:
        print(f"Length: {max_length}")

    return max_length


def test_longest_consecutive():
    """Test cases covering various scenarios."""

    # Test case 1: Basic example
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive_sorting([100, 4, 200, 1, 3, 2]) == 4

    # Test case 2: Long sequence
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9

    # Test case 3: With negatives
    assert longest_consecutive([9, 1, 4, 7, 3, -1, 0, 5, 8, -2, 6, 2]) == 7

    # Test case 4: Empty array
    assert longest_consecutive([]) == 0

    # Test case 5: Single element
    assert longest_consecutive([1]) == 1

    # Test case 6: No consecutive
    assert longest_consecutive([1, 3, 5, 7, 9]) == 1

    # Test case 7: All consecutive
    assert longest_consecutive([1, 2, 3, 4, 5]) == 5

    # Test case 8: Duplicates
    assert longest_consecutive([1, 2, 0, 1]) == 3

    # Test case 9: Multiple sequences, same length
    assert longest_consecutive([1, 2, 3, 10, 11, 12]) == 3

    # Test case 10: Unsorted with gaps
    assert longest_consecutive([4, 2, 6, 1, 5]) == 3

    # Test extensions
    assert find_longest_consecutive_sequence([100, 4, 200, 1, 3, 2]) == [1, 2, 3, 4]
    sequences = find_all_consecutive_sequences([1, 2, 3, 10, 11, 12])
    assert len(sequences) == 2

    print("All test cases passed!")


if __name__ == "__main__":
    # Run tests
    test_longest_consecutive()

    # Example with visualization
    print("\n" + "=" * 70)
    print("EXAMPLE 1: BASIC CASE")
    print("=" * 70)
    visualize_longest_consecutive([100, 4, 200, 1, 3, 2])

    print("\n" + "=" * 70)
    print("EXAMPLE 2: WITH NEGATIVE NUMBERS")
    print("=" * 70)
    visualize_longest_consecutive([9, 1, 4, 7, 3, -1, 0, 5, 8, -2, 6, 2])

    # Compare approaches
    print("\n" + "=" * 70)
    print("COMPARING APPROACHES")
    print("=" * 70)

    test_cases = [
        [100, 4, 200, 1, 3, 2],
        [0, 3, 7, 2, 5, 8, 4, 6, 0, 1],
        [1, 3, 5, 7, 9],
    ]

    for nums in test_cases:
        print(f"\nInput: {nums}")

        # Brute force
        result1 = longest_consecutive_brute_force(nums)
        print(f"Brute Force (O(n³)):    {result1}")

        # Sorting
        result2 = longest_consecutive_sorting(nums)
        print(f"Sorting (O(n log n)):   {result2}")

        # Hash set
        result3 = longest_consecutive(nums)
        print(f"Hash Set (O(n)):        {result3}")

        # Show actual sequence
        sequence = find_longest_consecutive_sequence(nums)
        print(f"Actual sequence:        {sequence}")

        # Show all sequences
        all_seqs = find_all_consecutive_sequences(nums)
        if all_seqs:
            print(f"All sequences (≥2):     {all_seqs}")

    # Detailed explanation
    print("\n" + "=" * 70)
    print("ALGORITHM EXPLANATION")
    print("=" * 70)
    print("""
The key insight is ONLY starting from sequence beginnings:

1. Why Hash Set?
   - O(1) lookup to check if number exists
   - Eliminates duplicates automatically

2. Identifying Sequence Starts:
   - A number is a sequence start if (num - 1) doesn't exist
   - Example: In [1, 2, 3], only 1 is a start

3. Counting from Starts Only:
   - From each start, count consecutive numbers
   - Since we only start from beginnings, no duplicated work

4. Time Complexity Analysis:
   - Building set: O(n)
   - Checking each number: O(n)
   - Counting sequences: appears O(n²) but actually O(n)
     * Each number visited at most twice:
       1. Once when checking if it's a start
       2. Once when building sequence from some start
   - Total: O(n)

Example: nums = [100, 4, 200, 1, 3, 2]
Set: {1, 2, 3, 4, 100, 200}

Process each number:
- 1: Is start (0 not in set)
     Count: 1, 2, 3, 4 → length 4 ✓
- 2: Not start (1 in set), skip
- 3: Not start (2 in set), skip
- 4: Not start (3 in set), skip
- 100: Is start (99 not in set)
       Count: 100 → length 1
- 200: Is start (199 not in set)
       Count: 200 → length 1

Result: 4 (from sequence [1, 2, 3, 4])

Key: Only 1, 100, and 200 trigger counting!
    """)

    # Performance comparison
    print("\n" + "=" * 70)
    print("COMPLEXITY ANALYSIS")
    print("=" * 70)
    print("""
Approach          Time         Space      Notes
-------------------------------------------------------
Brute Force       O(n³)        O(1)       Check each sequence
Sorting           O(n log n)   O(1)*      Sort then scan
Hash Set          O(n)         O(n)       Optimal solution

*Sorting space depends on algorithm

Key Insights:
1. Hash set enables O(1) membership testing
2. Only count from sequence starts → avoid duplicated work
3. Each element accessed at most twice → O(n) total
4. Converting to set eliminates duplicates automatically

Common Mistakes:
- Counting from every number → O(n²) time
- Not handling duplicates properly
- Forgetting to check (num - 1) to identify starts
- Using list instead of set → O(n) per lookup

Why Not Other Approaches?
- Brute force: Too slow for large n
- Sorting: Changes O(n) → O(n log n), violates requirement
- Hash map (num -> length): More complex, same complexity

Pattern Recognition:
"Consecutive sequence" + "O(n) time" → Use hash set
- Set for O(1) lookup
- Only process sequence starts
- Count consecutive elements

Related Problems:
1. Longest Consecutive Sequence II (with range ops)
2. Consecutive Numbers Sum (829)
3. Find Longest Awesome Substring (1542)
4. Longest Substring Without Repeating Characters (3)
5. Longest Harmonious Subsequence (594)
    """)

    # Visual representation
    print("\n" + "=" * 70)
    print("VISUAL EXAMPLE")
    print("=" * 70)
    print("""
Input: [100, 4, 200, 1, 3, 2]

Step 1: Convert to set (removes duplicates, enables O(1) lookup)
Set: {1, 2, 3, 4, 100, 200}

Step 2: Process each number
┌─────┬──────────┬───────────┬──────────────────┐
│ Num │ Is Start │ Action    │ Sequence Found   │
├─────┼──────────┼───────────┼──────────────────┤
│ 1   │ Yes      │ Count     │ [1,2,3,4] len=4  │
│ 2   │ No       │ Skip      │ -                │
│ 3   │ No       │ Skip      │ -                │
│ 4   │ No       │ Skip      │ -                │
│ 100 │ Yes      │ Count     │ [100] len=1      │
│ 200 │ Yes      │ Count     │ [200] len=1      │
└─────┴──────────┴───────────┴──────────────────┘

Result: Maximum length = 4

Why this is O(n):
- We visit each number once to check if it's a start
- We visit consecutive numbers once when building from start
- Each number accessed at most 2 times
- Total operations: O(n)
    """)
