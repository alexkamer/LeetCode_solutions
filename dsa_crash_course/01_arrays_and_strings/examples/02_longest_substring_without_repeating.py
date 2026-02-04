"""
Longest Substring Without Repeating Characters

Problem:
Given a string s, find the length of the longest substring without repeating 
characters.

Example 1:
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.

Example 2:
Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.

Example 3:
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

Constraints:
- 0 <= s.length <= 5 * 10^4
- s consists of English letters, digits, symbols and spaces.
"""


def length_of_longest_substring(s):
    """
    Sliding window with hash map approach - optimal solution.
    
    Approach:
    1. Use sliding window with left and right pointers
    2. Use hash map to track last seen index of each character
    3. Expand window by moving right pointer
    4. If character is repeated, shrink window from left
    5. Track maximum window size seen
    
    Key Insight:
    When we find a duplicate, we don't need to move left pointer one by one.
    We can jump directly to position after the previous occurrence.
    
    Time Complexity: O(n) - each character visited at most twice
    Space Complexity: O(min(m, n)) where m is charset size
    
    Args:
        s: Input string
        
    Returns:
        Length of longest substring without repeating characters
    """
    # Map to store last seen index of each character
    char_index = {}
    max_length = 0
    left = 0
    
    for right in range(len(s)):
        char = s[right]
        
        # If character was seen before and is in current window
        if char in char_index and char_index[char] >= left:
            # Move left pointer to position after previous occurrence
            left = char_index[char] + 1
        
        # Update last seen index of current character
        char_index[char] = right
        
        # Update max length
        current_length = right - left + 1
        max_length = max(max_length, current_length)
    
    return max_length


def length_of_longest_substring_set(s):
    """
    Alternative: Sliding window with set.
    
    This is more intuitive but slightly less efficient as we may move
    left pointer multiple times for a single duplicate.
    
    Time Complexity: O(2n) = O(n) - worst case each char visited twice
    Space Complexity: O(min(m, n))
    """
    char_set = set()
    max_length = 0
    left = 0
    
    for right in range(len(s)):
        # Remove characters from left until no duplicate
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        
        # Add current character
        char_set.add(s[right])
        
        # Update max length
        max_length = max(max_length, right - left + 1)
    
    return max_length


def length_of_longest_substring_brute_force(s):
    """
    Brute force approach - check all substrings.
    
    Approach:
    1. Generate all substrings
    2. Check if each substring has all unique characters
    3. Track maximum length
    
    Time Complexity: O(n³) - O(n²) substrings, O(n) to check each
    Space Complexity: O(min(m, n)) for set
    
    This is too slow but helps understand the problem.
    """
    max_length = 0
    
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            substring = s[i:j]
            
            # Check if all characters are unique
            if len(substring) == len(set(substring)):
                max_length = max(max_length, len(substring))
    
    return max_length


def test_longest_substring():
    """Comprehensive test cases."""
    
    # Test case 1: Mixed characters
    assert length_of_longest_substring("abcabcbb") == 3  # "abc"
    
    # Test case 2: All same characters
    assert length_of_longest_substring("bbbbb") == 1  # "b"
    
    # Test case 3: All unique
    assert length_of_longest_substring("pwwkew") == 3  # "wke"
    
    # Test case 4: Empty string
    assert length_of_longest_substring("") == 0
    
    # Test case 5: Single character
    assert length_of_longest_substring("a") == 1
    
    # Test case 6: No repeats
    assert length_of_longest_substring("abcdef") == 6
    
    # Test case 7: Longest at end
    assert length_of_longest_substring("abba") == 2  # "ab" or "ba"
    
    # Test case 8: With spaces and symbols
    assert length_of_longest_substring("a b c a") == 3  # " bc" or "b c"
    
    # Test case 9: Numbers
    assert length_of_longest_substring("12321") == 3  # "123" or "321"
    
    # Test case 10: Long repeat-free sequence at end
    assert length_of_longest_substring("aaabcdefg") == 7  # "abcdefg"
    
    print("All test cases passed!")


def visualize_solution(s):
    """
    Helper function to visualize the sliding window process.
    """
    print(f"\nFinding longest substring without repeating chars in: '{s}'")
    print("-" * 60)
    
    char_index = {}
    max_length = 0
    max_substring = ""
    left = 0
    
    for right in range(len(s)):
        char = s[right]
        
        if char in char_index and char_index[char] >= left:
            print(f"Step {right+1}: Found duplicate '{char}' at index {right}")
            print(f"  Previous occurrence at index {char_index[char]}")
            print(f"  Moving left from {left} to {char_index[char] + 1}")
            left = char_index[char] + 1
        
        char_index[char] = right
        current_length = right - left + 1
        
        if current_length > max_length:
            max_length = current_length
            max_substring = s[left:right+1]
            print(f"Step {right+1}: New max found: '{max_substring}' (length {max_length})")
        
        print(f"  Window: [{left}, {right}] = '{s[left:right+1]}'")
    
    print(f"\nResult: '{max_substring}' with length {max_length}")
    return max_length


if __name__ == "__main__":
    test_longest_substring()
    
    # Visualize solution process
    test_cases = ["abcabcbb", "pwwkew"]
    for test in test_cases:
        visualize_solution(test)
