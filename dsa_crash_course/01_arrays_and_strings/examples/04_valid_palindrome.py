"""
Valid Palindrome

Problem:
A phrase is a palindrome if, after converting all uppercase letters into 
lowercase letters and removing all non-alphanumeric characters, it reads 
the same forward and backward. Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.

Example 1:
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.

Example 2:
Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.

Example 3:
Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.

Constraints:
- 1 <= s.length <= 2 * 10^5
- s consists only of printable ASCII characters.
"""


def is_palindrome(s):
    """
    Two pointer approach with in-place checking - optimal solution.
    
    Approach:
    1. Use two pointers: left at start, right at end
    2. Skip non-alphanumeric characters from both ends
    3. Compare characters (case-insensitive)
    4. If mismatch found, return False
    5. If pointers meet, return True
    
    Key Insight:
    We don't need to create a cleaned string - we can check while skipping
    invalid characters, saving space.
    
    Time Complexity: O(n) - single pass through string
    Space Complexity: O(1) - only using pointer variables
    
    Args:
        s: Input string to check
        
    Returns:
        True if string is palindrome, False otherwise
    """
    left = 0
    right = len(s) - 1
    
    while left < right:
        # Skip non-alphanumeric from left
        while left < right and not s[left].isalnum():
            left += 1
        
        # Skip non-alphanumeric from right
        while left < right and not s[right].isalnum():
            right -= 1
        
        # Compare characters (case-insensitive)
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True


def is_palindrome_cleaned_string(s):
    """
    Alternative: Clean string first, then check.
    
    This is more straightforward but uses extra space.
    
    Time Complexity: O(n)
    Space Complexity: O(n) - creates cleaned string
    """
    # Clean string: only keep alphanumeric, convert to lowercase
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    
    # Check if cleaned string equals its reverse
    return cleaned == cleaned[::-1]


def is_palindrome_recursive(s):
    """
    Recursive approach - educational but not optimal.
    
    Time Complexity: O(n)
    Space Complexity: O(n) - recursion stack
    """
    # Clean string first
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    
    def helper(left, right):
        # Base case: pointers met or crossed
        if left >= right:
            return True
        
        # Check if characters match
        if cleaned[left] != cleaned[right]:
            return False
        
        # Recursively check inner substring
        return helper(left + 1, right - 1)
    
    return helper(0, len(cleaned) - 1)


def test_is_palindrome():
    """Comprehensive test cases."""
    
    # Test case 1: Classic palindrome with spaces and punctuation
    assert is_palindrome("A man, a plan, a canal: Panama") == True
    
    # Test case 2: Not a palindrome
    assert is_palindrome("race a car") == False
    
    # Test case 3: Empty after cleaning
    assert is_palindrome(" ") == True
    
    # Test case 4: Single character
    assert is_palindrome("a") == True
    
    # Test case 5: Simple palindrome
    assert is_palindrome("racecar") == True
    
    # Test case 6: Palindrome with numbers
    assert is_palindrome("A1b2B1a") == True
    
    # Test case 7: Mixed case
    assert is_palindrome("Was it a car or a cat I saw?") == False
    
    # Test case 8: Numbers only
    assert is_palindrome("12321") == True
    
    # Test case 9: Special characters only
    assert is_palindrome(".,!") == True
    
    # Test case 10: Long palindrome
    assert is_palindrome("Able was I ere I saw Elba") == True
    
    # Test case 11: Not palindrome, close
    assert is_palindrome("abc") == False
    
    # Test case 12: Two characters, same
    assert is_palindrome("aa") == True
    
    # Test case 13: Two characters, different
    assert is_palindrome("ab") == False
    
    print("All test cases passed!")


def visualize_solution(s):
    """
    Helper to visualize the palindrome checking process.
    """
    print(f"\nChecking if palindrome: '{s}'")
    print("-" * 60)
    
    # Show cleaned version
    cleaned = ''.join(char.lower() for char in s if char.isalnum())
    print(f"After cleaning: '{cleaned}'")
    print()
    
    left = 0
    right = len(s) - 1
    step = 0
    
    while left < right:
        # Skip non-alphanumeric from left
        while left < right and not s[left].isalnum():
            left += 1
        
        # Skip non-alphanumeric from right
        while left < right and not s[right].isalnum():
            right -= 1
        
        step += 1
        print(f"Step {step}:")
        print(f"  Comparing s[{left}]='{s[left]}' with s[{right}]='{s[right]}'")
        print(f"  Lowercase: '{s[left].lower()}' vs '{s[right].lower()}'")
        
        if s[left].lower() != s[right].lower():
            print(f"  Mismatch! Not a palindrome.")
            return False
        
        print(f"  Match!")
        left += 1
        right -= 1
    
    print(f"\nResult: IS a palindrome!")
    return True


def compare_approaches():
    """
    Compare different implementation approaches.
    """
    import time
    
    test_string = "A man, a plan, a canal: Panama" * 100  # Long test
    
    # Test approach 1: Two pointers (optimal)
    start = time.time()
    result1 = is_palindrome(test_string)
    time1 = time.time() - start
    
    # Test approach 2: Cleaned string
    start = time.time()
    result2 = is_palindrome_cleaned_string(test_string)
    time2 = time.time() - start
    
    # Test approach 3: Recursive
    start = time.time()
    result3 = is_palindrome_recursive(test_string)
    time3 = time.time() - start
    
    print(f"\nPerformance comparison:")
    print(f"Two pointers (optimal):  {time1:.6f}s")
    print(f"Cleaned string:          {time2:.6f}s ({time2/time1:.2f}x slower)")
    print(f"Recursive:               {time3:.6f}s ({time3/time1:.2f}x slower)")
    print(f"\nAll approaches agree: {result1 == result2 == result3}")


if __name__ == "__main__":
    test_is_palindrome()
    
    # Visualize examples
    test_cases = [
        "A man, a plan, a canal: Panama",
        "race a car",
        "Was it a car or a cat I saw?"
    ]
    
    for test in test_cases:
        visualize_solution(test)
    
    # Compare performance
    print("\n" + "=" * 60)
    compare_approaches()
