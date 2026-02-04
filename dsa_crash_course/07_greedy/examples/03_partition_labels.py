"""
Partition Labels (LeetCode #763)

Problem:
You are given a string s. We want to partition the string into as many parts
as possible so that each letter appears in at most one part.

Return a list of integers representing the size of these parts.

Example 1:
Input: s = "ababcbacadefegdehijhklij"
Output: [9,7,8]
Explanation:
- Partition "ababcbaca" (9) - contains a,b,c
- Partition "defegde" (7) - contains d,e,f,g
- Partition "hijhklij" (8) - contains h,i,j,k,l

Example 2:
Input: s = "eccbbbbdec"
Output: [10]

Constraints:
- 1 <= s.length <= 500
- s consists of lowercase English letters
"""


def partition_labels(s):
    """
    Greedy solution using last occurrence tracking.
    
    Greedy Strategy:
    1. First pass: record last occurrence of each character
    2. Second pass: expand current partition to include all occurrences
       of characters seen so far
    3. When we reach the end of current partition, create a new one
    
    Why Greedy Works:
    - Each character must be completely contained in one partition
    - If we see character 'x' at position i, partition must extend 
      at least to last occurrence of 'x'
    - Greedy choice: make partition as small as possible while satisfying
      this constraint (ends at rightmost last-occurrence seen so far)
    - This maximizes number of partitions (optimal)
    
    Proof:
    - Consider optimal partition P
    - For first partition in P:
      * Must include all occurrences of its characters
      * Our greedy partition is minimal partition satisfying this
      * If our partition is smaller, P's first partition can be split further
      * If our partition is same size, continue by induction
      * If our partition is larger, P is invalid (would split some character)
    - Therefore greedy is optimal
    
    Time Complexity: O(n) - two passes through string
    Space Complexity: O(1) - hash map with at most 26 entries (constant)
    
    Args:
        s: String to partition
        
    Returns:
        List of partition sizes
    """
    # Record last occurrence of each character
    last_occurrence = {char: i for i, char in enumerate(s)}
    
    partitions = []
    start = 0
    end = 0
    
    for i, char in enumerate(s):
        # Extend current partition to include last occurrence of this char
        end = max(end, last_occurrence[char])
        
        # If we've reached the end of current partition
        if i == end:
            partitions.append(end - start + 1)
            start = i + 1
    
    return partitions


def partition_labels_optimized(s):
    """
    Slightly cleaner version with same logic.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    last = {c: i for i, c in enumerate(s)}
    
    result = []
    partition_start = 0
    partition_end = 0
    
    for i in range(len(s)):
        partition_end = max(partition_end, last[s[i]])
        
        if i == partition_end:
            result.append(partition_end - partition_start + 1)
            partition_start = i + 1
    
    return result


def partition_labels_with_intervals(s):
    """
    Alternative view: merge overlapping intervals.
    
    Strategy:
    1. For each character, create interval [first_occurrence, last_occurrence]
    2. Merge overlapping intervals (characters that must be in same partition)
    3. Return sizes of merged intervals
    
    This is essentially interval merging problem!
    
    Time Complexity: O(n) for building intervals + O(1) for merging (at most 26 chars)
    Space Complexity: O(1) - at most 26 intervals
    """
    # Build intervals for each character
    first_occurrence = {}
    last_occurrence = {}
    
    for i, char in enumerate(s):
        if char not in first_occurrence:
            first_occurrence[char] = i
        last_occurrence[char] = i
    
    # Create intervals
    intervals = []
    for char in first_occurrence:
        intervals.append([first_occurrence[char], last_occurrence[char]])
    
    # Sort by start position
    intervals.sort()
    
    # Merge overlapping intervals
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            # Overlapping, merge
            merged[-1][1] = max(merged[-1][1], end)
        else:
            # Non-overlapping, new partition
            merged.append([start, end])
    
    # Return sizes
    return [end - start + 1 for start, end in merged]


def partition_labels_verbose(s):
    """
    Version with detailed tracking for educational purposes.
    
    Shows step-by-step what the algorithm does.
    """
    last = {c: i for i, c in enumerate(s)}
    
    result = []
    start = 0
    end = 0
    
    print(f"String: {s}")
    print(f"Last occurrence map: {last}")
    print("\nProcessing:")
    
    for i, char in enumerate(s):
        old_end = end
        end = max(end, last[char])
        
        if end != old_end:
            print(f"  Position {i} ('{char}'): extended partition end to {end}")
        
        if i == end:
            partition_size = end - start + 1
            partition_str = s[start:end+1]
            result.append(partition_size)
            print(f"  Position {i}: partition complete! '{partition_str}' (size {partition_size})")
            start = i + 1
    
    return result


def find_all_partition_chars(s, partition_start, partition_end):
    """
    Helper to find all unique characters in a partition.
    
    Used for testing and visualization.
    """
    return set(s[partition_start:partition_end+1])


def validate_partition(s, partition_sizes):
    """
    Verify that partition is valid (each char appears in only one partition).
    
    Returns True if valid, False otherwise.
    """
    partitions = []
    start = 0
    
    for size in partition_sizes:
        end = start + size - 1
        partitions.append(s[start:end+1])
        start = end + 1
    
    # Check that each character appears in only one partition
    all_chars = set()
    for partition in partitions:
        partition_chars = set(partition)
        if all_chars & partition_chars:
            # Overlap found!
            return False
        all_chars.update(partition_chars)
    
    return True


def test_partition_labels():
    """Comprehensive test cases."""
    
    # Test case 1: Example from problem
    s = "ababcbacadefegdehijhklij"
    result = partition_labels(s)
    assert result == [9, 7, 8]
    assert validate_partition(s, result)
    
    # Test case 2: All same partition
    s = "eccbbbbdec"
    result = partition_labels(s)
    assert result == [10]
    assert validate_partition(s, result)
    
    # Test case 3: Each character once (maximum partitions)
    s = "abcdef"
    result = partition_labels(s)
    assert result == [1, 1, 1, 1, 1, 1]
    assert validate_partition(s, result)
    
    # Test case 4: Single character repeated
    s = "aaaaa"
    result = partition_labels(s)
    assert result == [5]
    assert validate_partition(s, result)
    
    # Test case 5: Two distinct partitions
    s = "abcabc"
    result = partition_labels(s)
    assert result == [6]  # All chars interleaved
    assert validate_partition(s, result)
    
    # Test case 6: Clear separation
    s = "aaabbcc"
    result = partition_labels(s)
    assert result == [3, 2, 2]
    assert validate_partition(s, result)
    
    # Test case 7: Complex interleaving
    s = "abcdefg"
    result = partition_labels(s)
    assert result == [1] * 7
    assert validate_partition(s, result)
    
    # Test case 8: Last char extends partition
    s = "aba"
    result = partition_labels(s)
    assert result == [3]
    assert validate_partition(s, result)
    
    # Test case 9: Multiple extensions
    s = "abccaddbeffe"
    result = partition_labels(s)
    assert validate_partition(s, result)
    
    # Test all approaches give same result
    for test_str in ["ababcbacadefegdehijhklij", "eccbbbbdec", "abcdef"]:
        r1 = partition_labels(test_str)
        r2 = partition_labels_optimized(test_str)
        r3 = partition_labels_with_intervals(test_str)
        assert r1 == r2 == r3, f"Mismatch for {test_str}"
    
    print("All test cases passed!")


def explain_greedy_correctness():
    """
    Detailed explanation of why greedy approach is optimal.
    
    CLAIM: Greedy algorithm produces maximum number of partitions.
    
    PROOF BY EXCHANGE ARGUMENT:
    
    1. GREEDY STRATEGY:
       - Make each partition as small as possible
       - Partition ends when we've seen all occurrences of all characters seen so far
       - This is greedy: take earliest possible partition boundary
    
    2. ASSUME optimal solution O differs from greedy solution G:
       - Let first partition in G be P_g ending at position e_g
       - Let first partition in O be P_o ending at position e_o
       - If e_g < e_o: P_o can be split at e_g (still valid) → contradiction
       - If e_g > e_o: P_o splits some character (invalid) → contradiction
       - Therefore e_g = e_o
    
    3. BY INDUCTION:
       - If first k partitions of G and O are same
       - Then (k+1)th partition must also be same (by above argument)
       - Therefore G = O, greedy is optimal
    
    4. ALTERNATIVE PROOF (Greedy stays ahead):
       - At each step, greedy creates partition as early as possible
       - This leaves maximum string remaining for future partitions
       - Can't do better than making partition as small as possible
    
    KEY INSIGHT:
    - This is essentially an interval merging problem
    - Each character defines interval [first_occurrence, last_occurrence]
    - Overlapping intervals must be in same partition
    - Greedy merges intervals optimally
    
    COMPLEXITY:
    - Time: O(n) - two passes through string
    - Space: O(1) - at most 26 characters in map
    
    This problem demonstrates "local optimality → global optimality"
    which is the hallmark of greedy algorithms.
    """
    print(__doc__)


def visualize_partition(s):
    """
    Visualize the partitioning process.
    """
    last = {c: i for i, c in enumerate(s)}
    
    print(f"\nString: {s}")
    print("Index:  " + "".join(str(i % 10) for i in range(len(s))))
    print()
    
    partitions = []
    start = 0
    end = 0
    
    for i, char in enumerate(s):
        end = max(end, last[char])
        
        if i == end:
            partitions.append((start, end))
            start = i + 1
    
    # Print partitions
    for idx, (start, end) in enumerate(partitions):
        partition_str = s[start:end+1]
        chars = sorted(set(partition_str))
        print(f"Partition {idx+1}: [{start:2d}:{end:2d}] = '{partition_str}'")
        print(f"             Characters: {chars}")
        print(f"             Size: {end - start + 1}")
        print()


if __name__ == "__main__":
    test_partition_labels()
    
    print("\n" + "="*60)
    print("Example Usage:")
    print("="*60)
    
    # Example 1 - with visualization
    s = "ababcbacadefegdehijhklij"
    result = partition_labels(s)
    print(f"\nInput: s = {s}")
    print(f"Output: {result}")
    visualize_partition(s)
    
    # Example 2 - verbose processing
    print("="*60)
    print("Verbose Processing:")
    print("="*60)
    s = "eccbbbbdec"
    result = partition_labels_verbose(s)
    print(f"\nFinal result: {result}")
    
    print("\n" + "="*60)
    print("Greedy Correctness Proof:")
    print("="*60)
    explain_greedy_correctness()
