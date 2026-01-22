class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        Sliding window approach with hash map.

        Approach:
        - Use two pointers (start and end) to define a window
        - Use a hash map to track the most recent index of each character
        - When we find a duplicate, move start pointer past the old occurrence
        - Track the maximum window size seen

        Time Complexity: O(n) - single pass through string
        Space Complexity: O(min(n, m)) where m is charset size
        """
        char_index = {}  # Maps character to its most recent index
        max_length = 0
        start = 0

        for end in range(len(s)):
            char = s[end]

            # If character is already in our window, move start pointer
            if char in char_index and char_index[char] >= start:
                start = char_index[char] + 1

            # Update the character's most recent position
            char_index[char] = end

            # Calculate current window size and update max
            max_length = max(max_length, end - start + 1)

        return max_length


if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    s = "abcabcbb"
    print(f"Input: s = {s}")
    print(f"Output: {solution.lengthOfLongestSubstring(s)}")
    print(f"Expected: 3\n")

    # Test case 2
    s = "bbbbb"
    print(f"Input: s = {s}")
    print(f"Output: {solution.lengthOfLongestSubstring(s)}")
    print(f"Expected: 1\n")

    # Test case 3
    s = "pwwkew"
    print(f"Input: s = {s}")
    print(f"Output: {solution.lengthOfLongestSubstring(s)}")
    print(f"Expected: 3\n")

    # Test case 4 (the one that was failing)
    s = "ckilbkd"
    print(f"Input: s = {s}")
    print(f"Output: {solution.lengthOfLongestSubstring(s)}")
    print(f"Expected: 5\n")
