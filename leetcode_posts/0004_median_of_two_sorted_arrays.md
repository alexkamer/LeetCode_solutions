# 4 Methods: Merge & Sort → Two Pointers → Binary Search on Merged → Binary Search Partition | Python

# Intuition
You've got two sorted arrays and need to find the median of all elements combined. The naive way? Merge everything, sort it, find the middle. Simple, but the problem says it should run in O(log(m+n)). That "log" is screaming "binary search," but binary search on what exactly? That's the tricky part.

# Approach

## Method 1: Merge and Sort (Your Solution - Simple but Not Optimal)
```python
def findMedianSortedArrays(self, nums1, nums2):
    all_nums = sorted(nums1 + nums2)
    middle = len(all_nums) // 2

    if len(all_nums) % 2 != 0:
        return all_nums[middle]
    else:
        return (all_nums[middle] + all_nums[middle-1]) / 2
```

**Why this works:** Combine both arrays, sort them, pick the middle element(s).

**The problem:** You're sorting an already-sorted input. That's wasteful. Plus, sorting is O((m+n)log(m+n)), which violates the O(log(m+n)) requirement.

**Time:** O((m+n)log(m+n)) | **Space:** O(m+n)

**Use this if:** You're in a time crunch and just need something working. But in interviews, they'll push you to optimize.

---

## Method 2: Merge Without Sorting (Better)
Since both arrays are already sorted, use two pointers to merge them in order:

```python
def findMedianSortedArrays(self, nums1, nums2):
    merged = []
    i, j = 0, 0

    # Merge both arrays
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            merged.append(nums1[i])
            i += 1
        else:
            merged.append(nums2[j])
            j += 1

    # Add remaining elements
    merged.extend(nums1[i:])
    merged.extend(nums2[j:])

    # Find median
    n = len(merged)
    if n % 2 == 0:
        return (merged[n//2 - 1] + merged[n//2]) / 2
    else:
        return merged[n//2]
```

**Why this is better:** No sorting needed. You're leveraging the fact that inputs are already sorted.

**Example:** `nums1 = [1,3]`, `nums2 = [2]`
```
Compare 1 vs 2 → take 1 → merged = [1]
Compare 3 vs 2 → take 2 → merged = [1,2]
Add remaining 3 → merged = [1,2,3]
Middle = 2 ✓
```

**Time:** O(m+n) | **Space:** O(m+n)

**Still not optimal.** We're building the entire merged array when we only need the median.

---

## Method 3: Find Median Without Full Merge (Space Optimized)
You don't need the whole merged array - just the middle element(s):

```python
def findMedianSortedArrays(self, nums1, nums2):
    m, n = len(nums1), len(nums2)
    total = m + n
    target = total // 2

    i, j = 0, 0
    prev, curr = 0, 0

    # Iterate until we reach the median position
    for count in range(target + 1):
        prev = curr

        if i < m and (j >= n or nums1[i] <= nums2[j]):
            curr = nums1[i]
            i += 1
        else:
            curr = nums2[j]
            j += 1

    # Calculate median
    if total % 2 == 0:
        return (prev + curr) / 2
    else:
        return curr
```

**The optimization:** Only track the previous and current elements as you merge. Stop once you reach the median position.

**Why this works:** For median, you only care about the middle element(s), not the entire sorted sequence.

**Example:** `nums1 = [1,3]`, `nums2 = [2,4]` (total=4, need index 1 and 2)
```
count=0: curr=1 (from nums1[0])
count=1: prev=1, curr=2 (from nums2[0])
count=2: prev=2, curr=3 (from nums1[1])
Median = (2+3)/2 = 2.5 ✓
```

**Time:** O(m+n) | **Space:** O(1)

**This is respectable.** You've optimized space but still haven't hit the O(log(m+n)) target.

---

## Method 4: Binary Search Partition (Optimal - What They Want)
This is the hard part. Instead of merging, partition both arrays so that:
- Left half contains smaller elements
- Right half contains larger elements
- The partition point gives you the median

**Key insight:** If you know where to partition the smaller array, you can calculate where to partition the larger array.

```python
def findMedianSortedArrays(self, nums1, nums2):
    # Make sure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    left, right = 0, m

    while left <= right:
        partition1 = (left + right) // 2
        partition2 = (m + n + 1) // 2 - partition1

        # Handle edge cases
        maxLeft1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
        minRight1 = float('inf') if partition1 == m else nums1[partition1]

        maxLeft2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
        minRight2 = float('inf') if partition2 == n else nums2[partition2]

        # Check if we found the correct partition
        if maxLeft1 <= minRight2 and maxLeft2 <= minRight1:
            # Found it!
            if (m + n) % 2 == 0:
                return (max(maxLeft1, maxLeft2) + min(minRight1, minRight2)) / 2
            else:
                return max(maxLeft1, maxLeft2)
        elif maxLeft1 > minRight2:
            # partition1 is too far right, move left
            right = partition1 - 1
        else:
            # partition1 is too far left, move right
            left = partition1 + 1
```

**How this works:**

Imagine you partition both arrays:
```
nums1: [1, 3, | 8, 9]  partition1 = 2
nums2: [2, 5, 6, | 7, 10, 11, 12]  partition2 = 3

Left side:  [1, 3] and [2, 5, 6]
Right side: [8, 9] and [7, 10, 11, 12]
```

For a valid partition:
- `max(left side) <= min(right side)`
- Specifically: `nums1[partition1-1] <= nums2[partition2]` AND `nums2[partition2-1] <= nums1[partition1]`

If this holds, the median is based on the max of left and min of right.

**Why binary search?** You're searching for the correct partition point in the smaller array. Each comparison tells you if you need to move left or right.

**Example:** `nums1 = [1,3]`, `nums2 = [2]`
```
Binary search on nums1:
- Try partition1=1: [1 | 3] and [2 |]
- maxLeft1=1, minRight1=3
- maxLeft2=2, minRight2=inf
- Check: 1 <= inf ✓ and 2 <= 3 ✓
- Total is odd (3 elements)
- Median = max(1, 2) = 2 ✓
```

**Time:** O(log(min(m,n))) | **Space:** O(1)

**This is what LeetCode expects for "Hard".** It's tricky to implement but blazingly fast.

---

# Which Approach?

**For interviews on a "Hard" problem:** Method 4 (binary search partition)
- Shows you understand binary search beyond simple arrays
- Meets the O(log) requirement
- Demonstrates advanced problem-solving

**If you're honest about not knowing the trick:** Start with Method 1 or 2, explain the complexity, then say "I know there's a binary search solution but I'd need to work through the partition logic."

**For real-world code where time isn't critical:** Method 3 is clean and efficient enough.

**What you submitted (Method 1):** Works, but LeetCode marked this as "Hard" specifically because they want the binary search solution. Your approach would be perfect for an "Easy" or "Medium" problem.

# Complexity
**Your solution:**
- Time: O((m+n)log(m+n))
- Space: O(m+n)

**Optimal solution:**
- Time: O(log(min(m,n)))
- Space: O(1)

# Code (Optimal Solution)
```python3 []
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        # Ensure nums1 is the smaller array
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1

        m, n = len(nums1), len(nums2)
        left, right = 0, m

        while left <= right:
            partition1 = (left + right) // 2
            partition2 = (m + n + 1) // 2 - partition1

            maxLeft1 = float('-inf') if partition1 == 0 else nums1[partition1 - 1]
            minRight1 = float('inf') if partition1 == m else nums1[partition1]

            maxLeft2 = float('-inf') if partition2 == 0 else nums2[partition2 - 1]
            minRight2 = float('inf') if partition2 == n else nums2[partition2]

            if maxLeft1 <= minRight2 and maxLeft2 <= minRight1:
                if (m + n) % 2 == 0:
                    return (max(maxLeft1, maxLeft2) + min(minRight1, minRight2)) / 2
                else:
                    return max(maxLeft1, maxLeft2)
            elif maxLeft1 > minRight2:
                right = partition1 - 1
            else:
                left = partition1 + 1
```

# Why This Problem is Hard

The binary search partition approach is not intuitive. Most people don't naturally think "I should partition these arrays and binary search for the right partition." It requires:
1. Understanding that median = partition point between small and large elements
2. Realizing you can binary search on one array to find the partition
3. Handling all the edge cases (empty partitions, odd/even lengths)

Don't feel bad if you didn't get this immediately. It's one of those "once you see it, it makes sense" problems.

# Common Mistakes
1. **Sorting already-sorted arrays** (Method 1) - wastes the given structure
2. **Off-by-one errors in partition calculations** - super easy to mess up
3. **Not handling empty arrays** - edge case that breaks naive solutions
4. **Forgetting to use the smaller array** - binary search on the larger array is slower
5. **Mixing up maxLeft and minRight** - the partition logic is confusing

Practice this one. It's a classic "hard" problem that tests whether you can think beyond basic binary search.
