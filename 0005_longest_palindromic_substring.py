class Solution:
    def longestPalindrome(self, s: str) -> str:
        """
        Expand around center approach.

        For each possible center, expand outward while characters match.
        Handle both odd-length (single center) and even-length (two centers) palindromes.

        Time Complexity: O(n²) - n possible centers, each expansion is O(n)
        Space Complexity: O(1) - only storing indices
        """
        if not s:
            return ""

        def expand_around_center(left, right):
            """Expand outward from center while characters match."""
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            # Return the valid palindrome (left+1 to right-1)
            return left + 1, right - 1

        start, end = 0, 0

        for i in range(len(s)):
            # Check for odd-length palindrome (single character center)
            left1, right1 = expand_around_center(i, i)

            # Check for even-length palindrome (two character center)
            left2, right2 = expand_around_center(i, i + 1)

            # Find the longer of the two palindromes
            if right1 - left1 > end - start:
                start, end = left1, right1
            if right2 - left2 > end - start:
                start, end = left2, right2

        return s[start:end + 1]


if __name__ == '__main__':
    solution = Solution()

    # Test 1
    s = "babad"
    print(f"Input: {s}")
    print(f"Output: {solution.longestPalindrome(s)}")
    print(f"Expected: 'bab' or 'aba'\n")

    # Test 2
    s = "cbbd"
    print(f"Input: {s}")
    print(f"Output: {solution.longestPalindrome(s)}")
    print(f"Expected: 'bb'\n")

    # Test 3 - single character
    s = "a"
    print(f"Input: {s}")
    print(f"Output: {solution.longestPalindrome(s)}")
    print(f"Expected: 'a'\n")

    # Test 4 - all same characters
    s = "aaaa"
    print(f"Input: {s}")
    print(f"Output: {solution.longestPalindrome(s)}")
    print(f"Expected: 'aaaa'\n")
