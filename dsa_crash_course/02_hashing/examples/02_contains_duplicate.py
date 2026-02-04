"""
Contains Duplicate (LeetCode #217)

Problem:
Given an integer array 'nums', return true if any value appears at least twice
in the array, and return false if every element is distinct.

Example 1:
Input: nums = [1,2,3,1]
Output: true
Explanation: 1 appears twice.

Example 2:
Input: nums = [1,2,3,4]
Output: false
Explanation: All elements are distinct.

Example 3:
Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true

Constraints:
- 1 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9
"""


def contains_duplicate_brute_force(nums):
    """
    Brute force approach - compare every pair.

    Approach:
    1. Compare each element with every other element
    2. If we find a match, return True
    3. If no matches found, return False

    Time Complexity: O(n²) - nested loops
    Space Complexity: O(1) - no extra space

    Args:
        nums: List of integers

    Returns:
        True if any duplicate exists, False otherwise
    """
    n = len(nums)

    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] == nums[j]:
                return True

    return False


def contains_duplicate_sorting(nums):
    """
    Sorting approach - sort and check adjacent elements.

    Approach:
    1. Sort the array
    2. Check adjacent elements
    3. If any two adjacent elements are equal, return True

    Why this works:
    - Sorting brings duplicates together
    - Only need to check neighbors, not all pairs

    Time Complexity: O(n log n) - dominated by sorting
    Space Complexity: O(1) or O(n) - depends on sorting algorithm

    Args:
        nums: List of integers

    Returns:
        True if any duplicate exists, False otherwise
    """
    # Sort the array (modifies original, use nums[:] to copy)
    nums = sorted(nums)

    # Check adjacent elements
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            return True

    return False


def contains_duplicate(nums):
    """
    Optimal hash set approach - track seen elements.

    Approach:
    1. Use a set to track seen numbers
    2. For each number, check if it's in the set
    3. If yes, we found a duplicate
    4. If no, add it to the set

    Why this works:
    - Set provides O(1) membership testing
    - We can detect duplicate as soon as we see it
    - Set automatically handles uniqueness

    Time Complexity: O(n) - single pass through array
    Space Complexity: O(n) - set stores up to n unique elements

    Args:
        nums: List of integers

    Returns:
        True if any duplicate exists, False otherwise
    """
    seen = set()

    for num in nums:
        # If number already in set, it's a duplicate
        if num in seen:
            return True

        # Add number to set
        seen.add(num)

    return False


def contains_duplicate_pythonic(nums):
    """
    Pythonic approach - compare lengths.

    Approach:
    - Set removes duplicates automatically
    - If set length < list length, duplicates existed

    Time Complexity: O(n) - converting to set
    Space Complexity: O(n) - set stores unique elements

    Note: This is elegant but less flexible than the loop approach.
    Can't find which element is duplicated or return early.
    """
    return len(set(nums)) < len(nums)


def find_duplicate_element(nums):
    """
    Extension: Return the first duplicate element found.

    Returns the first number that appears twice, or None if no duplicates.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    seen = set()

    for num in nums:
        if num in seen:
            return num
        seen.add(num)

    return None


def find_all_duplicates(nums):
    """
    Extension: Return all duplicate elements.

    Returns a list of all numbers that appear more than once.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    from collections import Counter

    freq = Counter(nums)
    return [num for num, count in freq.items() if count > 1]


def visualize_contains_duplicate(nums):
    """
    Helper function to visualize the duplicate detection process.

    Shows step-by-step how the hash set approach works.
    """
    print(f"\nChecking for duplicates in: {nums}")
    print("=" * 60)

    seen = set()

    for i, num in enumerate(nums):
        print(f"\nStep {i + 1}:")
        print(f"  Current number: {num}")
        print(f"  Seen set before: {seen}")

        if num in seen:
            print(f"  ✓ Found duplicate! {num} was already seen")
            print(f"  Result: True")
            return True

        seen.add(num)
        print(f"  ✗ Not a duplicate, adding {num} to seen set")

    print("\n" + "=" * 60)
    print("No duplicates found")
    print("Result: False")
    return False


def test_contains_duplicate():
    """Test cases covering various scenarios."""

    # Test case 1: Has duplicate
    assert contains_duplicate([1, 2, 3, 1]) == True
    assert contains_duplicate_brute_force([1, 2, 3, 1]) == True
    assert contains_duplicate_sorting([1, 2, 3, 1]) == True

    # Test case 2: No duplicate
    assert contains_duplicate([1, 2, 3, 4]) == False
    assert contains_duplicate_pythonic([1, 2, 3, 4]) == False

    # Test case 3: Multiple duplicates
    assert contains_duplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) == True

    # Test case 4: Single element (no duplicate)
    assert contains_duplicate([1]) == False

    # Test case 5: Two elements, same
    assert contains_duplicate([1, 1]) == True

    # Test case 6: Two elements, different
    assert contains_duplicate([1, 2]) == False

    # Test case 7: All same elements
    assert contains_duplicate([5, 5, 5, 5, 5]) == True

    # Test case 8: Large array with duplicate at end
    assert contains_duplicate(list(range(1000)) + [500]) == True

    # Test case 9: Negative numbers
    assert contains_duplicate([-1, -2, -3, -1]) == True

    # Test case 10: Mix of positive and negative
    assert contains_duplicate([1, -1, 2, -2, 3]) == False

    # Test extensions
    assert find_duplicate_element([1, 2, 3, 1]) == 1
    assert find_duplicate_element([1, 2, 3, 4]) == None
    assert set(find_all_duplicates([1, 2, 2, 3, 3, 3])) == {2, 3}

    print("All test cases passed!")


if __name__ == "__main__":
    # Run tests
    test_contains_duplicate()

    # Example with visualization
    print("\n" + "=" * 60)
    print("EXAMPLE 1: WITH DUPLICATES")
    print("=" * 60)
    visualize_contains_duplicate([1, 2, 3, 1])

    print("\n" + "=" * 60)
    print("EXAMPLE 2: WITHOUT DUPLICATES")
    print("=" * 60)
    visualize_contains_duplicate([1, 2, 3, 4])

    # Compare approaches
    print("\n" + "=" * 60)
    print("COMPARING APPROACHES")
    print("=" * 60)

    test_cases = [
        [1, 2, 3, 1],
        [1, 2, 3, 4],
        [1, 1, 1, 3, 3, 4, 3, 2, 4, 2],
    ]

    for nums in test_cases:
        print(f"\nInput: {nums}")

        # Brute force
        result1 = contains_duplicate_brute_force(nums)
        print(f"Brute Force (O(n²)):    {result1}")

        # Sorting
        result2 = contains_duplicate_sorting(nums)
        print(f"Sorting (O(n log n)):   {result2}")

        # Hash set
        result3 = contains_duplicate(nums)
        print(f"Hash Set (O(n)):        {result3}")

        # Pythonic
        result4 = contains_duplicate_pythonic(nums)
        print(f"Pythonic (O(n)):        {result4}")

        # Extensions
        dup = find_duplicate_element(nums)
        if dup:
            print(f"First duplicate found:  {dup}")
            all_dups = find_all_duplicates(nums)
            print(f"All duplicates:         {all_dups}")

    # Performance comparison
    print("\n" + "=" * 60)
    print("COMPLEXITY ANALYSIS")
    print("=" * 60)
    print("""
Approach          Time         Space      Best For
-------------------------------------------------
Brute Force       O(n²)        O(1)       Small arrays, space critical
Sorting           O(n log n)   O(1)*      Balance time/space
Hash Set          O(n)         O(n)       Optimal for large arrays
Pythonic (set)    O(n)         O(n)       Quick one-liner

*Sorting space depends on algorithm (O(1) for in-place sorts)

Key Insights:
1. Hash set trades space for optimal time
2. Set membership test is O(1) vs O(n) for list
3. Early termination: hash set returns as soon as duplicate found
4. Sorting is middle ground: better than O(n²), worse than O(n)
5. Pythonic approach is elegant but can't return early

Common Follow-ups:
- Find the duplicate element → Return num instead of True
- Find all duplicates → Use Counter or track frequencies
- Count duplicates → Track how many times each appears
- Duplicates within distance k → Sliding window with hash set
    """)

    # Real-world applications
    print("\n" + "=" * 60)
    print("REAL-WORLD APPLICATIONS")
    print("=" * 60)
    print("""
This pattern appears in:

1. Data Validation
   - Check for duplicate IDs in database
   - Validate unique usernames/emails
   - Detect duplicate entries in forms

2. Fraud Detection
   - Multiple transactions from same source
   - Duplicate credit card numbers
   - Repeated login attempts

3. Data Deduplication
   - Remove duplicate files
   - Merge duplicate records
   - Clean datasets

4. Graph Algorithms
   - Detect cycles (revisiting nodes)
   - Track visited nodes in DFS/BFS
   - Find duplicate edges

5. Stream Processing
   - Detect repeated events
   - Filter duplicate messages
   - Track unique visitors
    """)
