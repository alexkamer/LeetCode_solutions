"""
Find Minimum in Rotated Sorted Array (LeetCode #153)

Problem:
Suppose an array of length n sorted in ascending order is rotated between 1 and n times.
For example, the array nums = [0,1,2,4,5,6,7] might become:
- [4,5,6,7,0,1,2] if it was rotated 4 times.
- [0,1,2,4,5,6,7] if it was rotated 7 times.

Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results in
the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]].

Given the sorted rotated array nums of unique elements, return the minimum element
of this array.

You must write an algorithm that runs in O(log n) time.

Example 1:
Input: nums = [3,4,5,1,2]
Output: 1
Explanation: The original array was [1,2,3,4,5] rotated 3 times.

Example 2:
Input: nums = [4,5,6,7,0,1,2]
Output: 0
Explanation: The original array was [0,1,2,4,5,6,7] and it was rotated 4 times.

Example 3:
Input: nums = [11,13,15,17]
Output: 11
Explanation: The original array was [11,13,15,17] and it was rotated 4 times.

Example 4:
Input: nums = [2,1]
Output: 1

Constraints:
- n == nums.length
- 1 <= n <= 5000
- -5000 <= nums[i] <= 5000
- All the integers of nums are unique
- nums is sorted and rotated between 1 and n times
"""


def find_min(nums):
    """
    Find minimum using binary search - compare with rightmost element.

    Key Insight:
    In a rotated sorted array, the minimum element is at the rotation point.
    By comparing mid with the rightmost element, we can determine which half
    contains the minimum.

    Strategy:
    - If nums[mid] > nums[right]: minimum is in right half (mid is in larger portion)
    - If nums[mid] < nums[right]: minimum is in left half including mid
    - If nums[mid] == nums[right]: only happens when they're the same element

    Why compare with right instead of left?
    Consider [3,4,5,1,2]:
    - mid=5, left=3, right=2
    - Comparing with right: 5 > 2, so min is on right ✓
    - Comparing with left: 5 > 3, ambiguous (could be either side)

    Time Complexity: O(log n) - binary search
    Space Complexity: O(1) - only a few variables

    Args:
        nums: Rotated sorted array with unique elements

    Returns:
        The minimum element in the array
    """
    left = 0
    right = len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        # If mid element is greater than rightmost element,
        # the minimum must be to the right of mid
        if nums[mid] > nums[right]:
            # Minimum is in right half
            left = mid + 1
        else:
            # Minimum is in left half (including mid)
            # mid could be the minimum, so we keep it
            right = mid

    # When left == right, we've found the minimum
    return nums[left]


def find_min_index(nums):
    """
    Find the index of minimum element (the rotation pivot point).

    This is useful when you need to know where the rotation happened,
    not just the minimum value.

    Time Complexity: O(log n)
    Space Complexity: O(1)

    Returns:
        Index of the minimum element
    """
    left = 0
    right = len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    return left


def find_min_compare_neighbors(nums):
    """
    Alternative: Compare mid with its neighbors to find the inflection point.

    The minimum is at a position where:
    - nums[i] < nums[i-1] (smaller than left neighbor)
    - nums[i] < nums[i+1] (smaller than right neighbor)

    This is more intuitive but requires extra boundary checks.

    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    n = len(nums)

    # Edge cases
    if n == 1:
        return nums[0]

    # Array not rotated
    if nums[0] < nums[-1]:
        return nums[0]

    left = 0
    right = n - 1

    while left <= right:
        mid = left + (right - left) // 2

        # Check if mid is the minimum
        # Compare with neighbors (with boundary checks)
        if mid > 0 and nums[mid] < nums[mid - 1]:
            return nums[mid]

        if mid < n - 1 and nums[mid] > nums[mid + 1]:
            return nums[mid + 1]

        # Determine which half to search
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid - 1

    return nums[0]


def find_min_with_duplicates(nums):
    """
    Extension: Handle arrays with duplicate elements (LeetCode #154).

    With duplicates, when nums[mid] == nums[right], we cannot determine
    which half contains the minimum. We must reduce the search space linearly.

    Example: [2,2,2,0,1]
    - If mid=2 and right=1, we know minimum is on the right
    - If mid=2 and right=2, we cannot tell (both sides could have minimum)

    Time Complexity: O(log n) average case, O(n) worst case
    - Worst case: [1,1,1,1,1] - must check all elements

    Space Complexity: O(1)
    """
    left = 0
    right = len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] > nums[right]:
            # Minimum is definitely in right half
            left = mid + 1
        elif nums[mid] < nums[right]:
            # Minimum is in left half (including mid)
            right = mid
        else:
            # nums[mid] == nums[right]
            # Cannot determine which side has minimum
            # Reduce search space by moving right pointer
            right -= 1

    return nums[left]


def find_min_iterative_explanation(nums):
    """
    Same algorithm with detailed step-by-step explanation.
    Useful for understanding the process.
    """
    left = 0
    right = len(nums) - 1

    print(f"Finding minimum in: {nums}")
    print(f"Array indices: {list(range(len(nums)))}\n")

    iteration = 0

    while left < right:
        iteration += 1
        mid = left + (right - left) // 2

        print(f"Iteration {iteration}:")
        print(f"  left={left}, mid={mid}, right={right}")
        print(f"  nums[left]={nums[left]}, nums[mid]={nums[mid]}, nums[right]={nums[right]}")

        if nums[mid] > nums[right]:
            print(f"  {nums[mid]} > {nums[right]}: Minimum is in right half")
            left = mid + 1
        else:
            print(f"  {nums[mid]} <= {nums[right]}: Minimum is in left half (including mid)")
            right = mid

        print(f"  New range: [{left}, {right}]\n")

    print(f"Found minimum: nums[{left}] = {nums[left]}")
    return nums[left]


def visualize_rotated_array(nums):
    """
    Visualize the structure of a rotated array.
    """
    print(f"\nArray: {nums}")
    print("=" * 60)

    min_idx = nums.index(min(nums))

    print(f"\nMinimum element: {nums[min_idx]} at index {min_idx}")
    print(f"Rotation point: The array was rotated {min_idx} times")

    # Show the two sorted portions
    if min_idx > 0:
        left_portion = nums[:min_idx]
        right_portion = nums[min_idx:]
        print(f"\nLeft portion (larger values):  {left_portion}")
        print(f"Right portion (smaller values): {right_portion}")
        print(f"\nOriginal sorted array would be: {right_portion + left_portion}")
    else:
        print("\nNo rotation detected - array is already sorted")

    # Visual representation
    visual = []
    for i, num in enumerate(nums):
        if i == min_idx:
            visual.append(f"[{num}*]")  # Mark minimum
        else:
            visual.append(f" {num} ")

    print(f"\nVisual: {' '.join(visual)}")
    print("        (Element marked with * is the minimum)")


def visualize_search_process(nums):
    """
    Visualize the binary search process step by step.
    """
    print(f"\nSearching for minimum in: {nums}")
    print("=" * 60)

    left = 0
    right = len(nums) - 1
    iteration = 0

    while left < right:
        iteration += 1
        mid = left + (right - left) // 2

        # Create visual representation
        visual = [' '] * len(nums)
        visual[left] = 'L'
        visual[mid] = 'M'
        visual[right] = 'R'

        print(f"\nIteration {iteration}:")
        print(f"Array:   {nums}")
        print(f"Markers: {visual}")
        print(f"Range:   [{left}:{right}]")

        # Show comparison
        print(f"\nCompare: nums[mid]={nums[mid]} vs nums[right]={nums[right]}")

        if nums[mid] > nums[right]:
            print(f"→ {nums[mid]} > {nums[right]}")
            print(f"→ Mid is in the larger rotated portion")
            print(f"→ Minimum must be in right half")
            print(f"→ Search in [{mid+1}:{right}]")
            left = mid + 1
        else:
            print(f"→ {nums[mid]} <= {nums[right]}")
            print(f"→ Mid is in the smaller portion or at minimum")
            print(f"→ Minimum is at mid or to its left")
            print(f"→ Search in [{left}:{mid}]")
            right = mid

    print(f"\n{'='*60}")
    print(f"Found minimum: nums[{left}] = {nums[left]}")
    return nums[left]


def test_find_min():
    """Comprehensive test cases."""

    # Test case 1: Standard rotation
    assert find_min([3, 4, 5, 1, 2]) == 1

    # Test case 2: Larger rotation
    assert find_min([4, 5, 6, 7, 0, 1, 2]) == 0

    # Test case 3: No rotation (or full rotation)
    assert find_min([11, 13, 15, 17]) == 11

    # Test case 4: Two elements
    assert find_min([2, 1]) == 1

    # Test case 5: Two elements, not rotated
    assert find_min([1, 2]) == 1

    # Test case 6: Single element
    assert find_min([1]) == 1

    # Test case 7: Minimum at beginning
    assert find_min([1, 2, 3, 4, 5]) == 1

    # Test case 8: Minimum at end
    assert find_min([2, 3, 4, 5, 1]) == 1

    # Test case 9: Three elements, various rotations
    assert find_min([2, 3, 1]) == 1
    assert find_min([3, 1, 2]) == 1
    assert find_min([1, 2, 3]) == 1

    # Test case 10: Large array
    assert find_min([6, 7, 8, 9, 10, 1, 2, 3, 4, 5]) == 1

    # Test with index finding
    assert find_min_index([3, 4, 5, 1, 2]) == 3
    assert find_min_index([4, 5, 6, 7, 0, 1, 2]) == 4

    # Test alternative approach
    assert find_min_compare_neighbors([3, 4, 5, 1, 2]) == 1
    assert find_min_compare_neighbors([4, 5, 6, 7, 0, 1, 2]) == 0

    # Test with duplicates (extension)
    assert find_min_with_duplicates([2, 2, 2, 0, 1]) == 0
    assert find_min_with_duplicates([1, 3, 5, 5, 5, 5]) == 1
    assert find_min_with_duplicates([3, 3, 1, 3]) == 1

    print("All test cases passed!")


def demonstrate_rotations():
    """
    Demonstrate various rotation scenarios.
    """
    print("\n" + "="*60)
    print("UNDERSTANDING ARRAY ROTATIONS")
    print("="*60)

    original = [1, 2, 3, 4, 5]
    print(f"\nOriginal sorted array: {original}")
    print("\nPossible rotations:")

    for k in range(len(original) + 1):
        rotated = original[k:] + original[:k]
        min_val = min(rotated)
        min_idx = rotated.index(min_val)
        print(f"  Rotate {k} times: {rotated} → min={min_val} at index {min_idx}")


def compare_approaches():
    """
    Compare different approaches and their characteristics.
    """
    print("\n" + "="*60)
    print("COMPARING APPROACHES")
    print("="*60)

    test_array = [4, 5, 6, 7, 0, 1, 2]

    print(f"\nTest array: {test_array}\n")

    approaches = [
        ("Standard (compare right)", find_min),
        ("Compare neighbors", find_min_compare_neighbors),
    ]

    for name, func in approaches:
        result = func(test_array)
        print(f"{name:30s}: {result}")

    print("\nAll approaches give the same result!")
    print("\nKey differences:")
    print("1. Standard approach: Cleaner, fewer edge cases")
    print("2. Neighbor comparison: More intuitive for some people")
    print("3. With duplicates: Requires special handling")


if __name__ == "__main__":
    # Run tests
    test_find_min()

    # Demonstrate rotations
    demonstrate_rotations()

    # Compare approaches
    compare_approaches()

    # Visualization examples
    print("\n" + "="*60)
    print("VISUALIZATION EXAMPLES")
    print("="*60)

    print("\nExample 1: Standard rotated array")
    print("-" * 60)
    visualize_rotated_array([3, 4, 5, 1, 2])

    print("\n" + "-" * 60)
    print("Example 2: Larger rotation")
    print("-" * 60)
    visualize_rotated_array([4, 5, 6, 7, 0, 1, 2])

    print("\n" + "-" * 60)
    print("Example 3: No rotation")
    print("-" * 60)
    visualize_rotated_array([1, 2, 3, 4, 5])

    # Show search process
    print("\n" + "="*60)
    print("DETAILED SEARCH PROCESS")
    print("="*60)

    print("\nExample 1: Finding minimum in [3,4,5,1,2]")
    print("-" * 60)
    visualize_search_process([3, 4, 5, 1, 2])

    print("\n" + "-" * 60)
    print("\nExample 2: Finding minimum in [4,5,6,7,0,1,2]")
    print("-" * 60)
    visualize_search_process([4, 5, 6, 7, 0, 1, 2])

    print("\n" + "-" * 60)
    print("\nExample 3: No rotation [1,2,3,4,5]")
    print("-" * 60)
    visualize_search_process([1, 2, 3, 4, 5])
