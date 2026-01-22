# 3 Solutions: Brute Force → Set Window → Hash Map Window (Optimal) | Python

# Intuition
You need the longest stretch of characters where nothing repeats. First instinct? Check every possible substring. But that's crazy slow. The better way is realizing you can "slide" a window across the string - expand when it's valid, shrink when you hit a duplicate.

# Approach

## Method 1: Brute Force - Check Everything
Try every possible substring and check if it has duplicates:

```python
def lengthOfLongestSubstring(self, s):
    max_len = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            substring = s[i:j+1]
            if len(substring) == len(set(substring)):  # No duplicates
                max_len = max(max_len, len(substring))
    return max_len
```

**Why this works:** You're checking literally every substring. If the set size equals the string length, no duplicates exist.

**The problem:** For "abcabcbb" (8 chars), you're checking 8+7+6+5+4+3+2+1 = 36 substrings. For a 1000-char string? Half a million substrings. Each one requires building the set.

**Time:** O(n³) | **Space:** O(min(n, m)) for the set

**Never use this in interviews.** It'll time out on big inputs.

---

## Method 2: Sliding Window (Set-Based)
Keep a set of current characters and two pointers:

```python
def lengthOfLongestSubstring(self, s):
    char_set = set()
    left = 0
    max_len = 0

    for right in range(len(s)):
        # Shrink window until no duplicates
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1

        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)

    return max_len
```

**How it works:**
- `right` pointer expands the window
- When you hit a duplicate, shrink from `left` until it's gone
- Track max window size

**Example:** `s = "abcabcbb"`
```
right=0: 'a' → set={'a'}, window="a", max=1
right=1: 'b' → set={'a','b'}, window="ab", max=2
right=2: 'c' → set={'a','b','c'}, window="abc", max=3
right=3: 'a' duplicate! Remove from left until 'a' is gone
         Remove 'a' → set={'b','c'}, left=1
         Add 'a' → set={'b','c','a'}, window="bca", max=3
...
```

**Why it's better:** Each character is visited at most twice (once by `right`, once by `left`). No nested loops checking substrings.

**Time:** O(n) | **Space:** O(min(n, m))

**This is solid for interviews.** Easy to understand and explain.

---

## Method 3: Sliding Window with Hash Map (Optimal)
Instead of shrinking one character at a time, jump directly:

```python
def lengthOfLongestSubstring(self, s):
    char_index = {}
    max_len = 0
    start = 0

    for end in range(len(s)):
        char = s[end]

        # If we've seen this char in current window, jump past it
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1

        char_index[char] = end
        max_len = max(max_len, end - start + 1)

    return max_len
```

**The upgrade:** When you find a duplicate, you know exactly where it was last seen. Jump `start` to one position after that. No need to shrink one by one.

**Example:** `s = "abba"`
```
end=0: 'a' at 0, char_index={'a':0}, start=0, window="a", len=1
end=1: 'b' at 1, char_index={'a':0,'b':1}, start=0, window="ab", len=2
end=2: 'b' at 2, duplicate at index 1!
       start jumps to 2, char_index={'a':0,'b':2}, window="b", len=1
end=3: 'a' at 3, char_index={'a':3,'b':2}, start=2, window="ba", len=2
```

**The trick:** Check `char_index[char] >= start` to make sure the duplicate is actually in your current window. If you saw it way back before `start`, it doesn't matter.

**Why check >= start?** Consider "abba" when you hit the second 'a'. The first 'a' is at index 0, but your window starts at 2 (after the duplicate 'b'). That old 'a' isn't in your window anymore, so don't jump back to it.

**Time:** O(n) | **Space:** O(min(n, m))

**This is the gold standard.** One pass, no wasted movements, and you can explain the logic clearly.

---

# Which Approach?

**For interviews:** Method 3 (hash map sliding window)
- Cleanest logic
- Optimal time and space
- Shows you understand both sliding window and hash maps

**If you're learning:** Start with Method 2 (set-based), get comfortable with the window concept, then upgrade to Method 3.

**Avoid:** Method 1 - it'll time out and shows you don't know optimization patterns.

# Complexity
- Time complexity: $O(n)$ - single pass, each character visited once
- Space complexity: $O(min(n, m))$ where m = charset size (26 for lowercase, 128 for ASCII, etc.)

# Code
```python3 []
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_index = {}
        max_length = 0
        start = 0

        for end in range(len(s)):
            char = s[end]

            if char in char_index and char_index[char] >= start:
                start = char_index[char] + 1

            char_index[char] = end
            max_length = max(max_length, end - start + 1)

        return max_length
```

# Gotchas to Watch For

1. **Empty string:** Returns 0 automatically (the loop doesn't run)
2. **All same characters:** "bbbbb" correctly returns 1
3. **All unique:** "abcdef" correctly returns 6
4. **The >= start check:** Critical for not jumping backwards

# Why This Pattern Matters

Sliding window shows up EVERYWHERE:
- Longest substring problems
- Minimum window problems
- Subarray sum problems

The hash map optimization (jumping instead of shrinking) is a key trick. Once you see it here, you'll recognize it in dozens of other problems.

Get comfortable with this. Draw it out. Walk through examples. It's one of those patterns that clicks and then becomes second nature.
