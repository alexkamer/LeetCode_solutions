"""
First Unique Character in a String (LeetCode #387)

Problem:
Given a string 's', find the first non-repeating character in it and return
its index. If it does not exist, return -1.

Example 1:
Input: s = "leetcode"
Output: 0
Explanation: The character 'l' at index 0 is the first character that does not
occur at any other index.

Example 2:
Input: s = "loveleetcode"
Output: 2
Explanation: 'v' at index 2.

Example 3:
Input: s = "aabb"
Output: -1
Explanation: All characters repeat.

Constraints:
- 1 <= s.length <= 10^5
- s consists of only lowercase English letters
"""


def first_unique_char_brute_force(s):
    """
    Brute force approach - count occurrences for each character.

    Approach:
    1. For each character, count how many times it appears in string
    2. Return the index of first character with count 1

    Time Complexity: O(n²) - for each char, scan entire string
    Space Complexity: O(1) - no extra data structures

    Args:
        s: Input string

    Returns:
        Index of first unique character, or -1 if none exists
    """
    for i in range(len(s)):
        # Count occurrences of current character
        count = 0
        for j in range(len(s)):
            if s[j] == s[i]:
                count += 1

        # If appears only once, it's unique
        if count == 1:
            return i

    return -1


def first_unique_char_two_pass(s):
    """
    Two-pass hash map approach.

    Approach:
    1. First pass: Count frequency of each character
    2. Second pass: Return index of first character with frequency 1

    Time Complexity: O(n) - two passes through string
    Space Complexity: O(1) - at most 26 lowercase letters

    Args:
        s: Input string

    Returns:
        Index of first unique character, or -1 if none exists
    """
    # First pass: Build frequency map
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1

    # Second pass: Find first unique character
    for i, char in enumerate(s):
        if freq[char] == 1:
            return i

    return -1


def first_unique_char(s):
    """
    Optimal approach using Counter - most Pythonic.

    Approach:
    1. Use Counter to count frequencies in one line
    2. Scan string to find first character with frequency 1

    Time Complexity: O(n) - two passes
    Space Complexity: O(1) - limited character set (26 letters)

    Args:
        s: Input string

    Returns:
        Index of first unique character, or -1 if none exists
    """
    from collections import Counter

    # Count character frequencies
    freq = Counter(s)

    # Find first unique character
    for i, char in enumerate(s):
        if freq[char] == 1:
            return i

    return -1


def first_unique_char_array(s):
    """
    Array-based approach for fixed character set.

    Approach:
    - Use array of size 26 for lowercase letters
    - Index by (ord(char) - ord('a'))

    Time Complexity: O(n)
    Space Complexity: O(1) - fixed size array

    Note: Only works for limited character sets.
    """
    # Array for 26 lowercase letters
    freq = [0] * 26

    # Count frequencies
    for char in s:
        index = ord(char) - ord('a')
        freq[index] += 1

    # Find first unique
    for i, char in enumerate(s):
        index = ord(char) - ord('a')
        if freq[index] == 1:
            return i

    return -1


def first_unique_char_with_index(s):
    """
    Extension: Track both frequency and first occurrence index.

    Approach:
    - Store tuple (count, first_index) for each character
    - Find character with count 1 and smallest index

    Time Complexity: O(n)
    Space Complexity: O(1) - at most 26 letters
    """
    char_info = {}  # char -> (count, first_index)

    for i, char in enumerate(s):
        if char in char_info:
            count, _ = char_info[char]
            char_info[char] = (count + 1, -1)  # Mark as duplicate
        else:
            char_info[char] = (1, i)

    # Find unique char with smallest index
    min_index = float('inf')
    for count, index in char_info.values():
        if count == 1 and index < min_index:
            min_index = index

    return min_index if min_index != float('inf') else -1


def find_all_unique_chars(s):
    """
    Extension: Return all unique character indices.

    Returns list of indices of all non-repeating characters.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    from collections import Counter

    freq = Counter(s)
    return [i for i, char in enumerate(s) if freq[char] == 1]


def visualize_first_unique_char(s):
    """
    Helper function to visualize the process.

    Shows step-by-step how the two-pass approach works.
    """
    print(f"\nFinding first unique character in: '{s}'")
    print("=" * 60)

    # First pass: Count frequencies
    print("\nFirst Pass - Counting Frequencies:")
    print("-" * 60)
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
        print(f"  '{char}': {freq[char]} occurrence(s)")

    print("\nFrequency Map:")
    for char, count in sorted(freq.items()):
        status = "unique" if count == 1 else "repeated"
        print(f"  '{char}': {count} ({status})")

    # Second pass: Find first unique
    print("\nSecond Pass - Finding First Unique:")
    print("-" * 60)
    for i, char in enumerate(s):
        is_unique = freq[char] == 1
        symbol = "✓" if is_unique else "✗"
        print(f"  Index {i}: '{char}' - frequency {freq[char]} {symbol}")

        if is_unique:
            print(f"\nFirst unique character: '{char}' at index {i}")
            return i

    print("\nNo unique character found")
    return -1


def test_first_unique_char():
    """Test cases covering various scenarios."""

    # Test case 1: Unique at beginning
    assert first_unique_char("leetcode") == 0
    assert first_unique_char_brute_force("leetcode") == 0

    # Test case 2: Unique in middle
    assert first_unique_char("loveleetcode") == 2
    assert first_unique_char_two_pass("loveleetcode") == 2

    # Test case 3: No unique character
    assert first_unique_char("aabb") == -1
    assert first_unique_char_array("aabb") == -1

    # Test case 4: All unique
    assert first_unique_char("abcdef") == 0

    # Test case 5: Single character
    assert first_unique_char("a") == 0

    # Test case 6: All same character
    assert first_unique_char("aaaa") == -1

    # Test case 7: Unique at end
    assert first_unique_char("aabbcd") == 4

    # Test case 8: Long string with unique at end
    assert first_unique_char("aabbccddeef") == 10

    # Test case 9: Complex pattern
    assert first_unique_char("dddccdbba") == 8

    # Test extensions
    assert find_all_unique_chars("loveleetcode") == [2, 3]
    assert find_all_unique_chars("aabb") == []

    print("All test cases passed!")


if __name__ == "__main__":
    # Run tests
    test_first_unique_char()

    # Example with visualization
    print("\n" + "=" * 60)
    print("EXAMPLE 1: UNIQUE AT BEGINNING")
    print("=" * 60)
    visualize_first_unique_char("leetcode")

    print("\n" + "=" * 60)
    print("EXAMPLE 2: UNIQUE IN MIDDLE")
    print("=" * 60)
    visualize_first_unique_char("loveleetcode")

    print("\n" + "=" * 60)
    print("EXAMPLE 3: NO UNIQUE CHARACTER")
    print("=" * 60)
    visualize_first_unique_char("aabb")

    # Compare approaches
    print("\n" + "=" * 60)
    print("COMPARING APPROACHES")
    print("=" * 60)

    test_cases = ["leetcode", "loveleetcode", "aabb", "abcdef"]

    for s in test_cases:
        print(f"\nInput: s = '{s}'")

        # Brute force
        result1 = first_unique_char_brute_force(s)
        print(f"Brute Force (O(n²)):    {result1}")

        # Two pass
        result2 = first_unique_char_two_pass(s)
        print(f"Two Pass (O(n)):        {result2}")

        # Counter
        result3 = first_unique_char(s)
        print(f"Counter (O(n)):         {result3}")

        # Array
        result4 = first_unique_char_array(s)
        print(f"Array-based (O(n)):     {result4}")

        if result3 != -1:
            print(f"Character: '{s[result3]}'")

        # Extension: all unique
        all_unique = find_all_unique_chars(s)
        if all_unique:
            unique_chars = [s[i] for i in all_unique]
            print(f"All unique chars: {unique_chars} at indices {all_unique}")

    # Performance comparison
    print("\n" + "=" * 60)
    print("COMPLEXITY ANALYSIS")
    print("=" * 60)
    print("""
Approach          Time         Space      Notes
--------------------------------------------------------
Brute Force       O(n²)        O(1)       Count for each char
Two-Pass Dict     O(n)         O(1)*      Best balance
Counter           O(n)         O(1)*      Most Pythonic
Array-based       O(n)         O(1)       Fastest for limited charset

*O(1) because at most 26 lowercase letters (constant space)

Key Insights:
1. Two passes better than nested loops: O(n) vs O(n²)
2. Hash map provides O(1) frequency lookup
3. For limited character set, array can be faster than dict
4. Counter simplifies frequency counting
5. Order matters: must find FIRST unique, so scan left to right

Pattern Recognition:
- "First unique/non-repeating" → Frequency count + scan
- "Count occurrences" → Hash map or Counter
- "Limited character set" → Can use array instead of hash map

Common Variations:
1. Find last unique character → Scan right to left
2. Find all unique characters → Return all with freq 1
3. Find kth unique character → Keep counter
4. Stream of characters → Use queue + hash map (LRU pattern)
    """)

    # Related problems
    print("\n" + "=" * 60)
    print("RELATED PROBLEMS")
    print("=" * 60)
    print("""
Similar Pattern:
1. First Non-Repeating Character in Stream
   - Use queue to maintain order
   - Hash map for frequencies
   - Remove from queue when count > 1

2. Sort Characters by Frequency (451)
   - Count frequencies
   - Sort by count descending
   - Build result string

3. Valid Anagram (242)
   - Count frequencies of both strings
   - Compare frequency maps

4. Group Anagrams (49)
   - Use sorted string or char count as key
   - Group strings with same key

5. Find All Anagrams in String (438)
   - Sliding window with frequency map
   - Compare window map with pattern map

Key Pattern: Frequency Counting
- Count occurrences of each element
- Process based on frequency
- Hash map is ideal data structure
    """)
