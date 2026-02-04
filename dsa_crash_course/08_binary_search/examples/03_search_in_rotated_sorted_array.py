"""
Search in Rotated Sorted Array

Problem:
There is an integer array 'nums' sorted in ascending order (with distinct values).

Prior to being passed to your function, 'nums' is possibly rotated at an unknown
pivot index k (1 <= k < nums.length) such that the resulting array is
[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed).

For example, [0,1,2,4,5,6,7] might be rotated at pivot index 3 and become [4,5,6,7,0,1,2].

Given the array 'nums' after the possible rotation and an integer 'target', return
the index of 'target' if it is in 'nums', or -1 if it is not in 'nums'.

You must write an algorithm with O(log n) runtime complexity.

Example 1:
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4

Example 2:
Input: nums = [4,5,6,7,0,1,2], target = 3
Output: -1

Example 3:
Input: nums = [1], target = 0
Output: -1

Example 4:
Input: nums = [1,3], target = 1
Output: 0

Constraints:
- 1 <= nums.length <= 5000
- -10^4 <= nums[i] <= 10^4
- All values of nums are unique
- nums is an ascending array that is possibly rotated
- -10^4 <= target <= 10^4
"""


def search_rotated(nums, target):
    """
    Search in rotated sorted array using modified binary search.

    Key insight: After rotation, at least one half of the array is always sorted.
    We can determine which half is sorted by comparing nums[left] with nums[mid].

    Approach:
    1. Calculate mid point
    2. Determine which half is sorted:
       - If nums[left] <= nums[mid]: left half is sorted
       - Otherwise: right half is sorted
    3. Check if target is in the sorted half:
       - If yes, search that half
       - If no, search the other half

    Time Complexity: O(log n) - binary search
    Space Complexity: O(1) - only using a few variables

    Args:
        nums: Rotated sorted array
        target: Value to find

    Returns:
        Index of target if found, -1 otherwise
    """
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        # Found target
        if nums[mid] == target:
            return mid

        # Determine which half is sorted
        if nums[left] <= nums[mid]:
            # Left half is sorted
            # Check if target is in sorted left half
            if nums[left] <= target < nums[mid]:
                right = mid - 1  # Target in left half
            else:
                left = mid + 1   # Target in right half
        else:
            # Right half is sorted
            # Check if target is in sorted right half
            if nums[mid] < target <= nums[right]:
                left = mid + 1   # Target in right half
            else:
                right = mid - 1  # Target in left half

    # Target not found
    return -1


def search_rotated_find_pivot(nums, target):
    """
    Alternative approach: First find pivot, then do normal binary search.

    This is less efficient (two binary searches) but more intuitive.

    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    if not nums:
        return -1

    # Find the pivot (minimum element)
    pivot = find_pivot(nums)

    # If no rotation, do normal binary search
    if pivot == 0:
        return binary_search(nums, 0, len(nums) - 1, target)

    # Determine which half to search
    if nums[0] <= target <= nums[pivot - 1]:
        # Target in left portion
        return binary_search(nums, 0, pivot - 1, target)
    else:
        # Target in right portion
        return binary_search(nums, pivot, len(nums) - 1, target)


def find_pivot(nums):
    """
    Find the index of the minimum element (the pivot point).

    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    left = 0
    right = len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] > nums[right]:
            # Minimum is in right half
            left = mid + 1
        else:
            # Minimum is in left half (including mid)
            right = mid

    return left


def binary_search(nums, left, right, target):
    """
    Standard binary search in a range.

    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


def search_rotated_with_duplicates(nums, target):
    """
    Modified version that handles duplicates (Follow-up problem).

    With duplicates, worst case becomes O(n) because we can't determine
    which half is sorted when nums[left] == nums[mid] == nums[right].

    Time Complexity: O(log n) average, O(n) worst case
    Space Complexity: O(1)
    """
    left = 0
    right = len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid

        # Handle duplicates
        if nums[left] == nums[mid] == nums[right]:
            # Can't determine which half is sorted, shrink both ends
            left += 1
            right -= 1
        elif nums[left] <= nums[mid]:
            # Left half is sorted
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            # Right half is sorted
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1


def visualize_search(nums, target):
    """
    Visualize the search process in rotated array.
    """
    print(f"\nSearching for {target} in rotated array: {nums}")
    print(f"Array indices: {list(range(len(nums)))}")

    # First, identify the rotation point
    pivot = find_pivot(nums)
    print(f"\nRotation pivot (minimum element) is at index {pivot}")
    print(f"Original sorted array was rotated at this point")

    left = 0
    right = len(nums) - 1
    iteration = 0

    print("\n--- Binary Search Process ---")

    while left <= right:
        iteration += 1
        mid = left + (right - left) // 2

        visual = [' '] * len(nums)
        visual[left] = 'L'
        visual[right] = 'R'
        visual[mid] = 'M'

        print(f"\nIteration {iteration}:")
        print(f"  Array:   {nums}")
        print(f"  Markers: {visual}")
        print(f"  Left={left}, Mid={mid}, Right={right}")
        print(f"  nums[left]={nums[left]}, nums[mid]={nums[mid]}, nums[right]={nums[right]}")

        if nums[mid] == target:
            print(f"  ✓ Found {target} at index {mid}!")
            return mid

        # Determine which half is sorted
        if nums[left] <= nums[mid]:
            print(f"  Left half [{left}:{mid}] is sorted")
            if nums[left] <= target < nums[mid]:
                print(f"  {target} is in sorted left half")
                right = mid - 1
            else:
                print(f"  {target} is not in left half, search right")
                left = mid + 1
        else:
            print(f"  Right half [{mid}:{right}] is sorted")
            if nums[mid] < target <= nums[right]:
                print(f"  {target} is in sorted right half")
                left = mid + 1
            else:
                print(f"  {target} is not in right half, search left")
                right = mid - 1

    print(f"\n  ✗ {target} not found in array")
    return -1


def test_search_rotated():
    """Comprehensive test cases."""

    # Test case 1: Target after rotation point
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4

    # Test case 2: Target not found
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1

    # Test case 3: Single element - not found
    assert search_rotated([1], 0) == -1

    # Test case 4: Two elements - target is first
    assert search_rotated([1, 3], 1) == 0

    # Test case 5: No rotation
    assert search_rotated([1, 2, 3, 4, 5], 3) == 2

    # Test case 6: Fully rotated (1 position)
    assert search_rotated([2, 3, 4, 5, 1], 1) == 4

    # Test case 7: Target at pivot
    assert search_rotated([5, 1, 3], 1) == 1

    # Test case 8: Target before rotation
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 5) == 1

    # Test case 9: Target after rotation
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 1) == 5

    # Test case 10: Two elements - rotated
    assert search_rotated([3, 1], 1) == 1

    # Test case 11: Large rotation
    assert search_rotated([6, 7, 8, 9, 10, 1, 2, 3, 4, 5], 3) == 7

    # Test alternative approach
    assert search_rotated_find_pivot([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert search_rotated_find_pivot([4, 5, 6, 7, 0, 1, 2], 3) == -1

    # Test with duplicates (Follow-up)
    assert search_rotated_with_duplicates([2, 5, 6, 0, 0, 1, 2], 0) == 3
    assert search_rotated_with_duplicates([1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1], 2) == 8

    print("All test cases passed!")


def demonstrate_rotation():
    """
    Demonstrate how rotation works and various rotation scenarios.
    """
    print("\n" + "="*60)
    print("UNDERSTANDING ROTATION")
    print("="*60)

    original = [0, 1, 2, 3, 4, 5, 6, 7]
    print(f"\nOriginal sorted array: {original}")

    for pivot in range(len(original)):
        rotated = original[pivot:] + original[:pivot]
        print(f"  Rotate at index {pivot}: {rotated}")


if __name__ == "__main__":
    # Run tests
    test_search_rotated()

    # Demonstrate rotation
    demonstrate_rotation()

    # Visualize examples
    print("\n" + "="*60)
    print("VISUALIZATION EXAMPLES")
    print("="*60)

    print("\nExample 1: Target in rotated portion")
    print("-" * 60)
    visualize_search([4, 5, 6, 7, 0, 1, 2], 0)

    print("\n" + "-" * 60)
    print("Example 2: Target in non-rotated portion")
    print("-" * 60)
    visualize_search([4, 5, 6, 7, 0, 1, 2], 5)

    print("\n" + "-" * 60)
    print("Example 3: Target not found")
    print("-" * 60)
    visualize_search([4, 5, 6, 7, 0, 1, 2], 3)

    print("\n" + "-" * 60)
    print("Example 4: No rotation")
    print("-" * 60)
    visualize_search([1, 2, 3, 4, 5, 6, 7], 4)
