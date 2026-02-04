"""
Two Sum II - Input Array Is Sorted

Problem:
Given a 1-indexed array of integers 'numbers' that is already sorted in 
non-decreasing order, find two numbers such that they add up to a specific 
target number. Return the indices of the two numbers (1-indexed).

You may assume that each input has exactly one solution and you may not use 
the same element twice.

Example 1:
Input: numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2.

Example 2:
Input: numbers = [2,3,4], target = 6
Output: [1,3]

Example 3:
Input: numbers = [-1,0], target = -1
Output: [1,2]

Constraints:
- 2 <= numbers.length <= 3 * 10^4
- -1000 <= numbers[i] <= 1000
- numbers is sorted in non-decreasing order
- -1000 <= target <= 1000
- The tests are generated such that there is exactly one solution
"""


def two_sum(numbers, target):
    """
    Two pointer approach - optimal solution for sorted array.
    
    Approach:
    1. Start with two pointers: left at beginning, right at end
    2. Calculate sum of numbers at both pointers
    3. If sum equals target, return indices (1-indexed)
    4. If sum < target, move left pointer right (increase sum)
    5. If sum > target, move right pointer left (decrease sum)
    
    Why this works:
    - Array is sorted, so moving left pointer increases sum
    - Moving right pointer decreases sum
    - We can eliminate possibilities in O(n) time
    
    Time Complexity: O(n) - single pass with two pointers
    Space Complexity: O(1) - only using two pointer variables
    
    Args:
        numbers: List of integers sorted in non-decreasing order
        target: Target sum to find
        
    Returns:
        List of two 1-indexed positions that sum to target
    """
    left = 0
    right = len(numbers) - 1
    
    while left < right:
        current_sum = numbers[left] + numbers[right]
        
        if current_sum == target:
            # Found the pair! Return 1-indexed positions
            return [left + 1, right + 1]
        elif current_sum < target:
            # Sum too small, need larger numbers
            left += 1
        else:
            # Sum too large, need smaller numbers
            right -= 1
    
    # Should never reach here given problem constraints
    return []


# Alternative approach using binary search (less optimal but worth knowing)
def two_sum_binary_search(numbers, target):
    """
    Binary search approach - good to know but less efficient here.
    
    Approach:
    For each number, use binary search to find complement.
    
    Time Complexity: O(n log n) - n iterations, each with O(log n) search
    Space Complexity: O(1)
    
    Note: Two pointers is better for this problem!
    """
    for i in range(len(numbers)):
        complement = target - numbers[i]
        
        # Binary search for complement in remaining array
        left, right = i + 1, len(numbers) - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            if numbers[mid] == complement:
                return [i + 1, mid + 1]  # 1-indexed
            elif numbers[mid] < complement:
                left = mid + 1
            else:
                right = mid - 1
    
    return []


def test_two_sum():
    """Test cases covering various scenarios."""
    
    # Test case 1: Basic example
    assert two_sum([2, 7, 11, 15], 9) == [1, 2]
    
    # Test case 2: Consecutive elements
    assert two_sum([2, 3, 4], 6) == [1, 3]
    
    # Test case 3: Negative numbers
    assert two_sum([-1, 0], -1) == [1, 2]
    
    # Test case 4: Large array
    assert two_sum([1, 2, 3, 4, 5, 6, 7, 8, 9], 17) == [8, 9]
    
    # Test case 5: Minimum array size
    assert two_sum([1, 2], 3) == [1, 2]
    
    # Test case 6: Duplicates
    assert two_sum([1, 2, 2, 3], 4) == [2, 3]
    
    # Test case 7: Negative target
    assert two_sum([-5, -3, -1, 0, 2], -8) == [1, 2]
    
    print("All test cases passed!")


if __name__ == "__main__":
    test_two_sum()
    
    # Example usage
    numbers = [2, 7, 11, 15]
    target = 9
    result = two_sum(numbers, target)
    print(f"Input: numbers = {numbers}, target = {target}")
    print(f"Output: {result}")
    print(f"Explanation: {numbers[result[0]-1]} + {numbers[result[1]-1]} = {target}")
