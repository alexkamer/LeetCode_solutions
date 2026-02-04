class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if needle not in haystack:
            return -1

        possible_indexes = [i for i, char in enumerate(haystack) if char == needle[0] and i <= (len(haystack)-len(needle))]
        # print(possible_indexes)
        for i in possible_indexes:
            # print(haystack[i:i+len(needle)], needle)
            if haystack[i:i+len(needle)] == needle:
                return i



if __name__ == '__main__':
    solution = Solution()


    haystack = "sadbutsad"
    needle = "sad"
    print(solution.strStr(haystack, needle))
    print("Expected: 0")


    haystack = "leetcode"
    needle = "leeto"
    print(solution.strStr(haystack, needle))
    print("Expected: -1")

    haystack = "mississippi"
    needle = "issip"
    print(solution.strStr(haystack, needle))
    print("Expected: 4")