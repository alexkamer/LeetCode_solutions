"""
Meeting Rooms II (LeetCode #253)

Problem:
Given an array of meeting time intervals where intervals[i] = [start_i, end_i],
return the minimum number of conference rooms required.

Example 1:
Input: intervals = [[0,30],[5,10],[15,20]]
Output: 2
Explanation: 
- Room 1: [0,30]
- Room 2: [5,10] then [15,20]

Example 2:
Input: intervals = [[7,10],[2,4]]
Output: 1

Constraints:
- 1 <= intervals.length <= 10^4
- 0 <= start_i < end_i <= 10^6
"""

import heapq


def min_meeting_rooms_heap(intervals):
    """
    Optimal greedy solution using min heap.
    
    Greedy Strategy:
    1. Sort meetings by start time
    2. Use min heap to track end times of ongoing meetings
    3. For each meeting:
       - If earliest ending meeting finishes before this starts, reuse room
       - Otherwise, need a new room
    4. Heap size = number of rooms needed at any time
    
    Why Greedy Works:
    - We process meetings in chronological order (earliest start first)
    - At any point, we need exactly as many rooms as there are overlapping meetings
    - Reusing the room that frees up earliest is always optimal
    - This is greedy: always reuse earliest available room
    
    Proof:
    - Let k = maximum number of overlapping meetings at any point
    - We need at least k rooms (pigeonhole principle)
    - Our algorithm uses exactly k rooms (never creates unnecessary rooms)
    - Therefore optimal
    
    Time Complexity: O(n log n) for sorting + O(n log n) for heap operations
    Space Complexity: O(n) for heap
    
    Args:
        intervals: List of [start, end] meeting times
        
    Returns:
        Minimum number of conference rooms needed
    """
    if not intervals:
        return 0
    
    # Sort meetings by start time
    intervals.sort(key=lambda x: x[0])
    
    # Min heap of end times for ongoing meetings
    # Heap invariant: heap[0] = earliest ending meeting
    rooms = []
    
    for start, end in intervals:
        # If earliest meeting has ended, reuse that room
        if rooms and rooms[0] <= start:
            heapq.heappop(rooms)
        
        # Add current meeting's end time
        heapq.heappush(rooms, end)
    
    # Number of rooms = number of meetings in heap
    return len(rooms)


def min_meeting_rooms_chronological(intervals):
    """
    Alternative approach - process all events chronologically.
    
    Strategy:
    1. Create events for all starts (+1) and ends (-1)
    2. Sort events chronologically
    3. Track running count of active meetings
    4. Maximum count = rooms needed
    
    Why this works:
    - At any point in time, rooms needed = active meetings
    - By processing events in order, we track active meetings
    - Key insight: if meeting ends at time T and another starts at T,
      we can reuse the room (end happens "before" start in our ordering)
    
    Time Complexity: O(n log n) for sorting
    Space Complexity: O(n) for events list
    """
    if not intervals:
        return 0
    
    events = []
    
    # Create start and end events
    for start, end in intervals:
        events.append((start, 1))    # Meeting starts: +1 room needed
        events.append((end, -1))     # Meeting ends: -1 room needed
    
    # Sort by time, with ends before starts at same time
    events.sort(key=lambda x: (x[0], x[1]))
    
    max_rooms = 0
    current_rooms = 0
    
    for time, delta in events:
        current_rooms += delta
        max_rooms = max(max_rooms, current_rooms)
    
    return max_rooms


def min_meeting_rooms_two_arrays(intervals):
    """
    Two arrays approach - separate starts and ends.
    
    Strategy:
    1. Create sorted array of start times
    2. Create sorted array of end times
    3. Use two pointers to track overlaps
    
    Intuition:
    - If next event is a start, need another room
    - If next event is an end, free a room
    - Process events in chronological order using two pointers
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    if not intervals:
        return 0
    
    starts = sorted([i[0] for i in intervals])
    ends = sorted([i[1] for i in intervals])
    
    start_ptr = 0
    end_ptr = 0
    rooms_needed = 0
    max_rooms = 0
    
    while start_ptr < len(starts):
        # If next event is a start
        if starts[start_ptr] < ends[end_ptr]:
            rooms_needed += 1
            max_rooms = max(max_rooms, rooms_needed)
            start_ptr += 1
        else:
            # Next event is an end, free a room
            rooms_needed -= 1
            end_ptr += 1
    
    return max_rooms


def min_meeting_rooms_sweep_line(intervals):
    """
    Sweep line algorithm - another view of chronological processing.
    
    This is conceptually the same as chronological approach but
    makes the "sweep line" concept explicit.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    if not intervals:
        return 0
    
    # Create timeline of changes
    timeline = []
    for start, end in intervals:
        timeline.append((start, 'start'))
        timeline.append((end, 'end'))
    
    # Sort: ends before starts at same time (can reuse room)
    timeline.sort(key=lambda x: (x[0], 0 if x[1] == 'end' else 1))
    
    current = 0
    max_rooms = 0
    
    for time, event_type in timeline:
        if event_type == 'start':
            current += 1
            max_rooms = max(max_rooms, current)
        else:
            current -= 1
    
    return max_rooms


# Helper functions for testing
def create_overlapping_intervals(n, max_time=100):
    """Generate test cases with varying overlap."""
    import random
    intervals = []
    for _ in range(n):
        start = random.randint(0, max_time)
        end = random.randint(start + 1, max_time + 10)
        intervals.append([start, end])
    return intervals


def visualize_meetings(intervals, rooms_needed):
    """
    Visualize meeting schedule.
    """
    print(f"\nMeeting Schedule (Need {rooms_needed} rooms):")
    print("-" * 60)
    
    # Sort by start time
    sorted_intervals = sorted(intervals)
    
    # Assign to rooms
    room_assignments = [[] for _ in range(rooms_needed)]
    
    for start, end in sorted_intervals:
        # Find first available room
        for i, room in enumerate(room_assignments):
            if not room or room[-1][1] <= start:
                room.append([start, end])
                break
    
    # Print room schedules
    for i, room in enumerate(room_assignments):
        print(f"Room {i+1}: {room}")


def test_meeting_rooms():
    """Comprehensive test cases."""
    
    # Test case 1: Basic overlapping
    intervals = [[0, 30], [5, 10], [15, 20]]
    assert min_meeting_rooms_heap(intervals) == 2
    assert min_meeting_rooms_chronological(intervals) == 2
    assert min_meeting_rooms_two_arrays(intervals) == 2
    
    # Test case 2: No overlap
    intervals = [[7, 10], [2, 4]]
    assert min_meeting_rooms_heap(intervals) == 1
    assert min_meeting_rooms_chronological(intervals) == 1
    
    # Test case 3: All overlap
    intervals = [[0, 10], [0, 10], [0, 10]]
    assert min_meeting_rooms_heap(intervals) == 3
    assert min_meeting_rooms_chronological(intervals) == 3
    
    # Test case 4: Sequential meetings (back-to-back)
    intervals = [[0, 5], [5, 10], [10, 15]]
    assert min_meeting_rooms_heap(intervals) == 1
    
    # Test case 5: One long meeting covering several short ones
    intervals = [[0, 30], [5, 10], [10, 15], [15, 20], [20, 25]]
    assert min_meeting_rooms_heap(intervals) == 2
    
    # Test case 6: Complex overlap pattern
    intervals = [[1, 5], [2, 6], [3, 7], [4, 8]]
    assert min_meeting_rooms_heap(intervals) == 4
    
    # Test case 7: Many sequential
    intervals = [[i, i+1] for i in range(10)]
    assert min_meeting_rooms_heap(intervals) == 1
    
    # Test case 8: All at same time
    intervals = [[1, 10] for _ in range(5)]
    assert min_meeting_rooms_heap(intervals) == 5
    
    # Test case 9: Single meeting
    intervals = [[1, 10]]
    assert min_meeting_rooms_heap(intervals) == 1
    
    # Test case 10: Edge case - meeting ends when another starts
    intervals = [[1, 5], [5, 9]]
    assert min_meeting_rooms_heap(intervals) == 1
    
    print("All test cases passed!")


def explain_greedy_correctness():
    """
    Detailed proof of correctness.
    
    CLAIM: The heap-based greedy algorithm finds the minimum number of rooms.
    
    PROOF:
    
    1. LOWER BOUND:
       - Let k = maximum number of meetings that overlap at any single point
       - We need AT LEAST k rooms (pigeonhole principle)
       - If k meetings overlap, they all need different rooms
    
    2. UPPER BOUND (Algorithm uses at most k rooms):
       - Process meetings by start time (greedy order)
       - Maintain heap of end times for active meetings
       - When meeting starts:
         a) If a room is free (earliest end <= current start), reuse it
         b) Otherwise, all rooms busy, need new room
       - Maximum heap size = maximum overlap = k
    
    3. OPTIMALITY:
       - Algorithm uses exactly k rooms
       - We proved we need at least k rooms
       - Therefore, algorithm is optimal
    
    4. GREEDY CHOICE:
       - "Always reuse the room that frees up earliest"
       - Why is this safe?
       - If room A ends at time t1 and room B ends at t2, where t1 < t2
       - If we can use room B for meeting starting at t3, we can use room A
       - Using A leaves B available for a potentially earlier meeting
       - So choosing earliest ending room never hurts
    
    EXCHANGE ARGUMENT:
    - Suppose optimal solution O differs from greedy solution G
    - Let meeting M be first where they differ
    - G assigns M to room with earliest end time
    - O assigns M to some other room
    - We can swap these assignments without increasing total rooms
    - By induction, G is optimal
    
    TIME COMPLEXITY ANALYSIS:
    - Sorting: O(n log n)
    - For each meeting: O(log n) heap operation
    - Total: O(n log n)
    
    SPACE COMPLEXITY:
    - Heap size = number of concurrent meetings = O(n) worst case
    """
    print(__doc__)


def compare_approaches():
    """Compare different solution approaches."""
    import time
    
    test_sizes = [10, 100, 1000]
    
    for size in test_sizes:
        intervals = create_overlapping_intervals(size)
        
        print(f"\nTest size: {size} meetings")
        
        approaches = [
            ("Heap (optimal)", min_meeting_rooms_heap),
            ("Chronological", min_meeting_rooms_chronological),
            ("Two arrays", min_meeting_rooms_two_arrays),
            ("Sweep line", min_meeting_rooms_sweep_line),
        ]
        
        for name, func in approaches:
            start = time.time()
            result = func(intervals[:])  # Copy to be safe
            elapsed = time.time() - start
            print(f"  {name:20s}: {result:3d} rooms in {elapsed*1000:6.3f}ms")


if __name__ == "__main__":
    test_meeting_rooms()
    
    print("\n" + "="*60)
    print("Example Usage:")
    print("="*60)
    
    # Example 1
    intervals = [[0, 30], [5, 10], [15, 20]]
    result = min_meeting_rooms_heap(intervals)
    print(f"Input: intervals = {intervals}")
    print(f"Output: {result}")
    visualize_meetings(intervals, result)
    
    # Example 2
    intervals = [[7, 10], [2, 4]]
    result = min_meeting_rooms_heap(intervals)
    print(f"\nInput: intervals = {intervals}")
    print(f"Output: {result}")
    
    print("\n" + "="*60)
    print("Greedy Correctness Proof:")
    print("="*60)
    explain_greedy_correctness()
    
    print("\n" + "="*60)
    print("Performance Comparison:")
    print("="*60)
    compare_approaches()
