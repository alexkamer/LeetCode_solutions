"""
Product of Array Except Self

Problem:
Given an integer array nums, return an array answer such that answer[i] is 
equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operator.

Example 1:
Input: nums = [1,2,3,4]
Output: [24,12,8,6]
Explanation: 
- answer[0] = 2*3*4 = 24
- answer[1] = 1*3*4 = 12
- answer[2] = 1*2*4 = 8
- answer[3] = 1*2*3 = 6

Example 2:
Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]

Constraints:
- 2 <= nums.length <= 10^5
- -30 <= nums[i] <= 30
- The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

Follow up: Can you solve the problem in O(1) extra space complexity? 
(The output array does not count as extra space for space complexity analysis.)
"""


def product_except_self(nums):
    """
    Two-pass with prefix and suffix products - optimal solution.
    
    Approach:
    The product except self[i] = (product of all elements before i) * 
                                 (product of all elements after i)
    
    1. First pass (left to right): Calculate prefix products
       - answer[i] = product of all elements to the left of i
    2. Second pass (right to left): Multiply by suffix products
       - answer[i] *= product of all elements to the right of i
    
    Key Insight:
    We can build the result array by combining prefix and suffix products
    without needing division or extra arrays.
    
    Time Complexity: O(n) - two passes through array
    Space Complexity: O(1) - only using output array (doesn't count)
    
    Args:
        nums: Input array of integers
        
    Returns:
        Array where each element is product of all other elements
    """
    n = len(nums)
    answer = [1] * n
    
    # First pass: left to right (prefix products)
    # answer[i] will contain product of all elements to the left
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]
    
    # Second pass: right to left (suffix products)
    # Multiply answer[i] by product of all elements to the right
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]
    
    return answer


def product_except_self_with_arrays(nums):
    """
    Alternative: Using explicit prefix and suffix arrays.
    
    This is more intuitive but uses O(n) extra space.
    Good for understanding the concept.
    
    Time Complexity: O(n)
    Space Complexity: O(n) - prefix and suffix arrays
    """
    n = len(nums)
    
    # Build prefix products array
    prefix = [1] * n
    for i in range(1, n):
        prefix[i] = prefix[i-1] * nums[i-1]
    
    # Build suffix products array
    suffix = [1] * n
    for i in range(n - 2, -1, -1):
        suffix[i] = suffix[i+1] * nums[i+1]
    
    # Combine prefix and suffix
    answer = [prefix[i] * suffix[i] for i in range(n)]
    
    return answer


def product_except_self_division(nums):
    """
    Using division (not allowed by problem, but good to know).
    
    Approach:
    1. Calculate total product of all elements
    2. For each element: total_product / nums[i]
    
    Edge case: Handle zeros specially
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Note: This fails if there are zeros in the array and doesn't meet
    the problem constraints (no division allowed).
    """
    # Count zeros and calculate product of non-zero elements
    zero_count = nums.count(0)
    
    if zero_count > 1:
        # More than one zero: all products are 0
        return [0] * len(nums)
    
    if zero_count == 1:
        # One zero: only that position gets product of others
        total_product = 1
        for num in nums:
            if num != 0:
                total_product *= num
        
        return [0 if num != 0 else total_product for num in nums]
    
    # No zeros: normal division approach
    total_product = 1
    for num in nums:
        total_product *= num
    
    return [total_product // num for num in nums]


def product_except_self_brute_force(nums):
    """
    Brute force - calculate product for each position.
    
    Time Complexity: O(n²) - for each element, multiply all others
    Space Complexity: O(1)
    
    Too slow for large inputs.
    """
    n = len(nums)
    answer = []
    
    for i in range(n):
        product = 1
        for j in range(n):
            if i != j:
                product *= nums[j]
        answer.append(product)
    
    return answer


def test_product_except_self():
    """Comprehensive test cases."""
    
    # Test case 1: Basic example
    assert product_except_self([1,2,3,4]) == [24,12,8,6]
    
    # Test case 2: With zero
    assert product_except_self([-1,1,0,-3,3]) == [0,0,9,0,0]
    
    # Test case 3: All ones
    assert product_except_self([1,1,1,1]) == [1,1,1,1]
    
    # Test case 4: Two elements
    assert product_except_self([2,3]) == [3,2]
    
    # Test case 5: With negative numbers
    assert product_except_self([-1,2,-3,4]) == [-24,-12,-8,6]
    
    # Test case 6: Large numbers
    assert product_except_self([10,20,30]) == [600,300,200]
    
    # Test case 7: Single zero at start
    assert product_except_self([0,1,2,3]) == [6,0,0,0]
    
    # Test case 8: Single zero at end
    assert product_except_self([1,2,3,0]) == [0,0,0,6]
    
    # Test case 9: Multiple zeros
    assert product_except_self([0,0,1]) == [0,0,0]
    
    print("All test cases passed!")


def visualize_solution(nums):
    """
    Helper to visualize the prefix/suffix calculation process.
    """
    print(f"\nCalculating products for: {nums}")
    print("=" * 60)
    
    n = len(nums)
    answer = [1] * n
    
    # Visualize prefix pass
    print("\nPrefix pass (left to right):")
    print("Building product of all elements to the left")
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        print(f"  i={i}: answer[{i}] = {prefix} (product of nums[0..{i-1}])")
        prefix *= nums[i]
    
    print(f"\nAfter prefix pass: {answer}")
    
    # Visualize suffix pass
    print("\nSuffix pass (right to left):")
    print("Multiplying by product of all elements to the right")
    suffix = 1
    for i in range(n - 1, -1, -1):
        print(f"  i={i}: answer[{i}] = {answer[i]} * {suffix} = {answer[i] * suffix}")
        answer[i] *= suffix
        suffix *= nums[i]
    
    print(f"\nFinal result: {answer}")
    
    # Verify
    print("\nVerification:")
    for i in range(n):
        expected = 1
        for j in range(n):
            if i != j:
                expected *= nums[j]
        print(f"  answer[{i}] = {answer[i]}, expected = {expected}, " + 
              ("✓" if answer[i] == expected else "✗"))
    
    return answer


def compare_approaches():
    """
    Compare different approaches.
    """
    import time
    
    # Generate large test case
    nums = list(range(1, 1001))
    
    approaches = [
        ("Optimal (O(1) space)", product_except_self),
        ("With arrays (O(n) space)", product_except_self_with_arrays),
    ]
    
    results = []
    for name, func in approaches:
        start = time.time()
        result = func(nums)
        elapsed = time.time() - start
        results.append((name, elapsed, result))
        print(f"{name:30s}: {elapsed:.6f}s")
    
    # Verify all approaches give same result
    all_same = all(r[2] == results[0][2] for r in results)
    print(f"\nAll approaches agree: {all_same}")


if __name__ == "__main__":
    test_product_except_self()
    
    # Visualize examples
    test_cases = [
        [1,2,3,4],
        [2,3,4,5]
    ]
    
    for test in test_cases:
        visualize_solution(test)
    
    # Performance comparison
    print("\n" + "=" * 60)
    print("Performance Comparison")
    print("=" * 60)
    compare_approaches()
