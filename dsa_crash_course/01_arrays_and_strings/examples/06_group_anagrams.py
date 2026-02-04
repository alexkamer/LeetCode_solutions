"""
Group Anagrams

Problem:
Given an array of strings strs, group the anagrams together. You can return 
the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different 
word or phrase, typically using all the original letters exactly once.

Example 1:
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

Example 2:
Input: strs = [""]
Output: [[""]]

Example 3:
Input: strs = ["a"]
Output: [["a"]]

Constraints:
- 1 <= strs.length <= 10^4
- 0 <= strs[i].length <= 100
- strs[i] consists of lowercase English letters.
"""

from collections import defaultdict


def group_anagrams(strs):
    """
    Hash map with sorted string as key - optimal and elegant solution.
    
    Approach:
    1. Anagrams have the same characters, just rearranged
    2. If we sort the characters, anagrams become identical
    3. Use sorted string as key in hash map
    4. Group strings with same key together
    
    Example: "eat", "tea", "ate" all become "aet" when sorted
    
    Time Complexity: O(n * k log k) where n = number of strings, k = max length
                     - n strings, each sorted in O(k log k)
    Space Complexity: O(n * k) - storing all strings in hash map
    
    Args:
        strs: List of strings to group
        
    Returns:
        List of lists, each containing anagrams grouped together
    """
    # Use defaultdict to automatically create empty lists
    anagram_map = defaultdict(list)
    
    for s in strs:
        # Sort string to create key
        # "eat" -> ['a','e','t'] -> "aet"
        key = ''.join(sorted(s))
        anagram_map[key].append(s)
    
    # Return all groups as list
    return list(anagram_map.values())


def group_anagrams_count(strs):
    """
    Hash map with character count as key - optimal without sorting.
    
    Approach:
    Instead of sorting, count character frequencies.
    Use count tuple as key (e.g., (1,0,0,1,1,0,...) for "eat")
    
    This avoids sorting but uses more space for keys.
    
    Time Complexity: O(n * k) where n = number of strings, k = max length
                     - Better than sorting approach!
    Space Complexity: O(n * k)
    
    Args:
        strs: List of strings to group
        
    Returns:
        List of lists, each containing anagrams grouped together
    """
    anagram_map = defaultdict(list)
    
    for s in strs:
        # Count character frequencies
        count = [0] * 26  # For 'a' to 'z'
        for char in s:
            count[ord(char) - ord('a')] += 1
        
        # Use tuple of counts as key (lists aren't hashable)
        key = tuple(count)
        anagram_map[key].append(s)
    
    return list(anagram_map.values())


def group_anagrams_brute_force(strs):
    """
    Brute force - compare each pair.
    
    Approach:
    For each string, check if it's an anagram of any existing group.
    If not, create a new group.
    
    Time Complexity: O(n² * k) - for each string, check against all groups
    Space Complexity: O(n * k)
    
    Too slow for large inputs.
    """
    def are_anagrams(s1, s2):
        """Check if two strings are anagrams."""
        if len(s1) != len(s2):
            return False
        return sorted(s1) == sorted(s2)
    
    groups = []
    
    for s in strs:
        # Try to find existing group
        found = False
        for group in groups:
            if are_anagrams(s, group[0]):
                group.append(s)
                found = True
                break
        
        # Create new group if needed
        if not found:
            groups.append([s])
    
    return groups


def test_group_anagrams():
    """Comprehensive test cases."""
    
    def normalize_result(result):
        """Sort for consistent comparison."""
        return sorted([sorted(group) for group in result])
    
    # Test case 1: Basic example
    result = group_anagrams(["eat","tea","tan","ate","nat","bat"])
    expected = [["bat"],["nat","tan"],["ate","eat","tea"]]
    assert normalize_result(result) == normalize_result(expected)
    
    # Test case 2: Empty string
    result = group_anagrams([""])
    expected = [[""]]
    assert normalize_result(result) == normalize_result(expected)
    
    # Test case 3: Single string
    result = group_anagrams(["a"])
    expected = [["a"]]
    assert normalize_result(result) == normalize_result(expected)
    
    # Test case 4: No anagrams
    result = group_anagrams(["abc","def","ghi"])
    expected = [["abc"],["def"],["ghi"]]
    assert normalize_result(result) == normalize_result(expected)
    
    # Test case 5: All anagrams
    result = group_anagrams(["abc","bca","cab"])
    expected = [["abc","bca","cab"]]
    assert normalize_result(result) == normalize_result(expected)
    
    # Test case 6: Different lengths
    result = group_anagrams(["a","ab","abc"])
    expected = [["a"],["ab"],["abc"]]
    assert normalize_result(result) == normalize_result(expected)
    
    # Test case 7: Repeated strings
    result = group_anagrams(["ab","ab","cd","cd"])
    expected = [["ab","ab"],["cd","cd"]]
    assert normalize_result(result) == normalize_result(expected)
    
    print("All test cases passed!")


def visualize_solution(strs):
    """
    Helper to visualize the grouping process.
    """
    print(f"\nGrouping anagrams for: {strs}")
    print("=" * 60)
    
    anagram_map = defaultdict(list)
    
    print("\nProcessing each string:")
    for i, s in enumerate(strs):
        key = ''.join(sorted(s))
        anagram_map[key].append(s)
        
        print(f"{i+1}. '{s}'")
        print(f"   Sorted: '{key}'")
        print(f"   Current group: {anagram_map[key]}")
    
    result = list(anagram_map.values())
    
    print(f"\nFinal groups: {result}")
    print(f"Number of groups: {len(result)}")
    
    return result


def compare_approaches():
    """
    Compare sorting vs counting approaches.
    """
    import time
    
    # Generate test case with many long strings
    test_strs = ["abcdefghij"] * 100 + ["jihgfedcba"] * 100 + ["aaabbbcccd"] * 100
    
    approaches = [
        ("Sorting", group_anagrams),
        ("Counting", group_anagrams_count),
    ]
    
    print("\nPerformance Comparison:")
    print("-" * 40)
    
    results = []
    for name, func in approaches:
        start = time.time()
        result = func(test_strs)
        elapsed = time.time() - start
        results.append((name, elapsed, result))
        print(f"{name:20s}: {elapsed:.6f}s")
    
    # Verify both give same result (after normalization)
    def normalize(r):
        return sorted([sorted(group) for group in r])
    
    same = normalize(results[0][2]) == normalize(results[1][2])
    print(f"\nBoth approaches agree: {same}")
    print(f"Counting is {results[0][1]/results[1][1]:.2f}x faster")


def analyze_complexity():
    """
    Analyze why counting approach is faster.
    """
    print("\nComplexity Analysis:")
    print("=" * 60)
    
    print("\nSorting approach: O(n * k log k)")
    print("  - n strings")
    print("  - Each sorted in O(k log k) where k is string length")
    print("  - For k=100: log k ≈ 7, so ~700 operations per string")
    
    print("\nCounting approach: O(n * k)")
    print("  - n strings")
    print("  - Each counted in O(k) where k is string length")
    print("  - For k=100: exactly 100 operations per string")
    
    print("\nFor long strings, counting is significantly faster!")
    print("For short strings, the difference is negligible.")


if __name__ == "__main__":
    test_group_anagrams()
    
    # Visualize examples
    test_cases = [
        ["eat","tea","tan","ate","nat","bat"],
        ["abc","bca","xyz","zyx","cab"]
    ]
    
    for test in test_cases:
        visualize_solution(test)
    
    # Performance comparison
    print("\n" + "=" * 60)
    compare_approaches()
    analyze_complexity()
