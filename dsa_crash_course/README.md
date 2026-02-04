# Data Structures & Algorithms Crash Course

A comprehensive guide to mastering data structures and algorithms for technical interviews and competitive programming.

## 📚 Course Overview

This crash course covers the fundamental data structures and algorithmic techniques you need to excel in coding interviews. Each section includes:

- **Theoretical foundations** - Core concepts and when to use them
- **Complexity analysis** - Time and space complexity for all operations
- **Common patterns** - Recurring problem-solving techniques
- **Example problems** - Fully solved problems with detailed explanations
- **Edge cases** - Important gotchas and corner cases to watch for

## 🗺️ Learning Path

The sections are ordered from foundational to advanced concepts:

### Foundation (Start Here)
1. **[Arrays and Strings](./01_arrays_and_strings/)** - The building blocks
2. **[Hashing](./02_hashing/)** - Fast lookups and counting
3. **[Linked Lists](./03_linked_lists/)** - Dynamic data structures

### Intermediate Structures
4. **[Stacks and Queues](./04_stacks_and_queues/)** - LIFO and FIFO operations
5. **[Trees and Graphs](./05_trees_and_graphs/)** - Hierarchical and networked data
6. **[Heaps](./06_heaps/)** - Priority-based operations

### Advanced Techniques
7. **[Greedy Algorithms](./07_greedy/)** - Making optimal local choices
8. **[Binary Search](./08_binary_search/)** - Efficient search techniques
9. **[Backtracking](./09_backtracking/)** - Exploring all possibilities
10. **[Dynamic Programming](./10_dynamic_programming/)** - Optimal subproblem solutions

## 📋 Content Structure

Each section contains:

```
XX_topic_name/
├── README.md          # Comprehensive theory and concepts
├── notes.md           # Quick reference (patterns, complexities, templates)
└── examples/          # Solved practice problems
    ├── problem_1.py
    ├── problem_2.py
    └── ...
```

## 🎯 How to Use This Course

### For Beginners
1. Start with section 1 and work through sequentially
2. Read the README first to understand the theory
3. Review the notes.md for quick reference
4. Work through each example problem, trying to solve it yourself first
5. Study the solution and understand the approach

### For Interview Prep
1. Review notes.md for each relevant section as a refresher
2. Focus on the example problems that match your target company's patterns
3. Practice implementing solutions without looking at the code
4. Time yourself to simulate interview conditions

### For Quick Reference
1. Use notes.md as cheat sheets during practice
2. Refer to complexity tables when analyzing your solutions
3. Use the pattern guides to identify which technique to apply

## 📊 Complexity Cheat Sheet

### Data Structure Operations

| Structure | Access | Search | Insert | Delete | Space |
|-----------|--------|--------|--------|--------|-------|
| Array | O(1) | O(n) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1) | O(1) | O(n) |
| Stack | O(n) | O(n) | O(1) | O(1) | O(n) |
| Queue | O(n) | O(n) | O(1) | O(1) | O(n) |
| Hash Table | - | O(1)* | O(1)* | O(1)* | O(n) |
| Binary Search Tree | O(log n)* | O(log n)* | O(log n)* | O(log n)* | O(n) |
| Heap | - | O(n) | O(log n) | O(log n) | O(n) |

*Average case; worst case may differ

### Algorithm Complexities

| Algorithm | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Binary Search | O(1) | O(log n) | O(log n) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) |
| DFS/BFS | O(V) | O(V+E) | O(V+E) | O(V) |

## 🔑 Problem-Solving Framework

When facing a new problem:

1. **Understand** - Read carefully, identify inputs/outputs, clarify edge cases
2. **Examples** - Work through 2-3 examples, including edge cases
3. **Approach** - Identify the pattern, choose appropriate data structure/algorithm
4. **Complexity** - Estimate time/space complexity before coding
5. **Implement** - Write clean, readable code with good variable names
6. **Test** - Verify with your examples and edge cases
7. **Optimize** - Consider if there's a more efficient solution

## 🎓 Pattern Recognition Guide

| Problem Keywords | Likely Pattern | Section |
|------------------|----------------|---------|
| "subarray", "substring" | Sliding Window | Arrays & Strings |
| "count", "frequency", "unique" | Hashing | Hashing |
| "linked list" + two pointer | Fast/Slow Pointers | Linked Lists |
| "valid parentheses", "next greater" | Stack | Stacks & Queues |
| "tree", "graph", "connected" | DFS/BFS | Trees & Graphs |
| "k smallest", "k largest", "median" | Heap | Heaps |
| "maximum/minimum", "interval" | Greedy | Greedy |
| "sorted array", "find target" | Binary Search | Binary Search |
| "all combinations", "permutations" | Backtracking | Backtracking |
| "maximum", "minimum", "count ways" | Dynamic Programming | Dynamic Programming |

## 📈 Progress Tracking

Keep track of your progress through each section:

- [ ] Arrays and Strings
- [ ] Hashing
- [ ] Linked Lists
- [ ] Stacks and Queues
- [ ] Trees and Graphs
- [ ] Heaps
- [ ] Greedy Algorithms
- [ ] Binary Search
- [ ] Backtracking
- [ ] Dynamic Programming

## 🔗 Additional Resources

- **Practice Platforms**: LeetCode, HackerRank, CodeForces
- **Books**: "Cracking the Coding Interview", "Algorithm Design Manual"
- **Visualizations**: VisuAlgo.net, Python Tutor

## 💡 Tips for Success

1. **Practice consistently** - Solve at least one problem daily
2. **Understand, don't memorize** - Focus on patterns, not specific solutions
3. **Time yourself** - Simulate real interview pressure
4. **Explain out loud** - Practice verbalizing your thought process
5. **Review mistakes** - Learn from wrong approaches
6. **Start simple** - Brute force first, then optimize
7. **Draw it out** - Visualize data structures and algorithm flow

---

*This crash course is designed to be language-agnostic, with examples in Python for clarity. The concepts apply to any programming language.*
