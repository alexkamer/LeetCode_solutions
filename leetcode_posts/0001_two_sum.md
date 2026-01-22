# 3 Methods: Brute Force → Two-Pass → One-Pass Hash Map | Python Solution

# Intuition
First time seeing this? Most people think "just check every pair until I find one that works." That's totally valid - it's the brute force approach. But we can do way better with a hash map.

# Approach

## Method 1: Brute Force - The Obvious Way
Just check every possible pair:
```python
for i in range(len(nums)):
    for j in range(i+1, len(nums)):
        if nums[i] + nums[j] == target:
            return [i, j]
```

**Why this works:** You're literally trying every combination until you hit the right one.

**The problem:** For an array with 10,000 elements, you're doing 10,000 × 10,000 = 100,000,000 comparisons. That's gonna be slow.

**Time:** O(n²) | **Space:** O(1)

---

## Method 2: Two-Pass Hash Map - Getting Smarter
First pass: throw everything into a hash map
```python
hash_map = {}
for i in range(len(nums)):
    hash_map[nums[i]] = i

for i in range(len(nums)):
    complement = target - nums[i]
    if complement in hash_map and hash_map[complement] != i:
        return [i, hash_map[complement]]
```

**Why this works:** You store all numbers first, then for each number you just check "does my complement exist?" Hash map lookups are instant (O(1)), so no more nested loops.

**The catch:** You need to make sure you're not using the same element twice (that's why we check `hash_map[complement] != i`).

**Time:** O(n) | **Space:** O(n)

---

## Method 3: One-Pass Hash Map - The Best Way
This is the slick version. Instead of two passes, do it in one:

```python
hash_map = {}
for i in range(len(nums)):
    complement = target - nums[i]
    if complement in hash_map:
        return [hash_map[complement], i]
    hash_map[nums[i]] = i
```

**Why this works:** As you scan through the array, you're checking "have I already seen the number I need?" If yes, done. If no, remember this number for later.

**The magic:** By the time you reach the second number of the pair, you've already stored the first number. So you find it immediately.

**Example:** `nums = [2, 7, 11, 15], target = 9`
```
i=0, num=2: Need 7. Seen it? Nope. Store {2: 0}
i=1, num=7: Need 2. Seen it? YES at index 0! Return [0, 1]
```

**Time:** O(n) | **Space:** O(n)

---

# Which One Should You Use?

**For interviews:** Method 3 (one-pass hash map)
- It's the fastest
- Shows you understand hash maps
- Interviewers expect you to optimize from brute force to this

**For learning:** Start with Method 1, understand why it's slow, then appreciate why Method 3 is elegant.

# Complexity
- Time complexity: $O(n)$ - you go through the array once
- Space complexity: $O(n)$ - worst case you store every number

# Code
```python3 []
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hash_map = {}

        for i in range(len(nums)):
            complement = target - nums[i]

            if complement in hash_map:
                return [hash_map[complement], i]

            hash_map[nums[i]] = i
```

# Why Hash Maps?
Hash maps trade space for speed. You're using O(n) extra memory to avoid doing O(n²) comparisons. Almost always worth it.

The pattern here (storing complements) shows up in tons of other problems. Master this and you'll recognize it everywhere.
