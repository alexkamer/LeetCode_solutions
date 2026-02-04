"""
Container With Most Water

Problem:
You are given an integer array height of length n. There are n vertical lines 
drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the 
container contains the most water.

Return the maximum amount of water a container can store.

Note: You may not slant the container.

Example 1:
Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: Lines at index 1 and index 8 form container with area = 7 * (8-1) = 49

Example 2:
Input: height = [1,1]
Output: 1

Constraints:
- n == height.length
- 2 <= n <= 10^5
- 0 <= height[i] <= 10^4
"""


def max_area(height):
    """
    Two pointer approach - optimal solution.
    
    Approach:
    1. Start with widest container (leftmost and rightmost lines)
    2. Calculate area: min(height[left], height[right]) * (right - left)
    3. Move the pointer pointing to shorter line inward
    4. Keep track of maximum area seen
    
    Key Insight:
    - Area is limited by shorter line
    - Moving shorter line inward might find a taller line
    - Moving taller line inward will only decrease width and can't increase area
      (because area is still limited by the shorter line on the other side)
    
    Why this works:
    We start with maximum width. As we move pointers inward, width decreases.
    To potentially increase area, we need to find taller lines.
    Moving the pointer at shorter line gives us the best chance.
    
    Time Complexity: O(n) - single pass with two pointers
    Space Complexity: O(1) - only using pointer variables
    
    Args:
        height: List of line heights
        
    Returns:
        Maximum water area that can be contained
    """
    left = 0
    right = len(height) - 1
    max_water = 0
    
    while left < right:
        # Calculate current area
        # Width: distance between lines
        # Height: limited by shorter line
        width = right - left
        current_height = min(height[left], height[right])
        current_area = width * current_height
        
        # Update maximum
        max_water = max(max_water, current_area)
        
        # Move pointer at shorter line
        # This gives us chance to find taller line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water


def max_area_brute_force(height):
    """
    Brute force approach - check all pairs.
    
    Approach:
    Try all possible pairs of lines and calculate area for each.
    
    Time Complexity: O(n²) - nested loops
    Space Complexity: O(1)
    
    This works but is too slow for large inputs.
    """
    max_water = 0
    n = len(height)
    
    for i in range(n):
        for j in range(i + 1, n):
            width = j - i
            current_height = min(height[i], height[j])
            area = width * current_height
            max_water = max(max_water, area)
    
    return max_water


def test_max_area():
    """Comprehensive test cases."""
    
    # Test case 1: Example from problem
    assert max_area([1,8,6,2,5,4,8,3,7]) == 49
    
    # Test case 2: Minimum array
    assert max_area([1,1]) == 1
    
    # Test case 3: Ascending heights
    assert max_area([1,2,3,4,5]) == 6  # lines at index 0 and 4: min(1,5) * 4
    
    # Test case 4: Descending heights
    assert max_area([5,4,3,2,1]) == 6  # lines at index 0 and 4: min(5,1) * 4
    
    # Test case 5: All same height
    assert max_area([4,4,4,4]) == 12  # lines at index 0 and 3: 4 * 3
    
    # Test case 6: Peak in middle
    assert max_area([1,3,2,5,25,24,5]) == 24  # lines at index 4 and 5: min(25,24) * 1
    
    # Test case 7: Tall lines at ends
    assert max_area([10,1,1,1,1,10]) == 50  # lines at index 0 and 5: min(10,10) * 5
    
    # Test case 8: One tall line
    assert max_area([1,100,1]) == 2  # lines at index 0 and 2: min(1,1) * 2
    
    print("All test cases passed!")


def visualize_solution(height):
    """
    Helper to visualize the two-pointer process.
    """
    print(f"\nFinding max water area for heights: {height}")
    print("-" * 60)
    
    left = 0
    right = len(height) - 1
    max_water = 0
    best_config = None
    
    step = 0
    while left < right:
        width = right - left
        current_height = min(height[left], height[right])
        current_area = width * current_height
        
        step += 1
        print(f"Step {step}:")
        print(f"  Lines at indices {left} (h={height[left]}) and {right} (h={height[right]})")
        print(f"  Width: {width}, Height: {current_height}, Area: {current_area}")
        
        if current_area > max_water:
            max_water = current_area
            best_config = (left, right, width, current_height)
            print(f"  ** New maximum! **")
        
        # Move pointer at shorter line
        if height[left] < height[right]:
            print(f"  Moving left pointer (shorter line)")
            left += 1
        else:
            print(f"  Moving right pointer")
            right -= 1
    
    print(f"\nBest configuration:")
    left, right, width, h = best_config
    print(f"  Indices: {left} and {right}")
    print(f"  Heights: {height[left]} and {height[right]}")
    print(f"  Width: {width}, Height: {h}")
    print(f"  Maximum Area: {max_water}")
    
    return max_water


if __name__ == "__main__":
    test_max_area()
    
    # Visualize example
    test_cases = [
        [1,8,6,2,5,4,8,3,7],
        [1,2,1]
    ]
    
    for heights in test_cases:
        visualize_solution(heights)
