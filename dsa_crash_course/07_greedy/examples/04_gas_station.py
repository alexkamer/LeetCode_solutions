"""
Gas Station (LeetCode #134)

Problem:
There are n gas stations along a circular route, where the amount of gas at 
station i is gas[i].

You have a car with an unlimited gas tank and it costs cost[i] of gas to travel
from station i to its next station (i + 1). You begin the journey with an empty
tank at one of the gas stations.

Given two integer arrays gas and cost, return the starting gas station's index
if you can travel around the circuit once in the clockwise direction, otherwise
return -1. If there exists a solution, it is guaranteed to be unique.

Example 1:
Input: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
Output: 3
Explanation:
Start at station 3: 4 gas, move to 4: 4-1+5=8, move to 0: 8-2+1=7,
move to 1: 7-3+2=6, move to 2: 6-4+3=5, move to 3: done

Example 2:
Input: gas = [2,3,4], cost = [3,4,3]
Output: -1
Explanation: Cannot complete circuit from any starting point.

Constraints:
- n == gas.length == cost.length
- 1 <= n <= 10^5
- 0 <= gas[i], cost[i] <= 10^4
"""


def can_complete_circuit(gas, cost):
    """
    Optimal one-pass greedy solution.
    
    Greedy Strategy:
    1. Track total balance (sum of all gas - cost)
       - If total < 0, impossible from any start
    2. Track current balance from current starting point
       - If current < 0, can't start from any station up to here
       - Reset start to next station
    3. The last reset point that allows completion is the answer
    
    Why Greedy Works (Proof):
    
    Key Observations:
    1. If total gas >= total cost, solution exists
    2. If we can't reach station j from station i, then we also can't
       reach j from any station between i and j
    
    Proof of Observation 2:
    - Suppose we start at i, and fail to reach j (run out of gas before j)
    - Let k be any station between i and j (i < k < j)
    - When we reached k from i, we had some gas >= 0
    - If we start at k instead, we start with 0 gas
    - So starting at k is strictly worse than reaching k from i
    - Therefore, if i can't reach j, neither can k
    
    This means: if we fail at position j starting from i, we should
    try starting from j+1 (all positions i..j are invalid starts)
    
    Time Complexity: O(n) - single pass
    Space Complexity: O(1) - only tracking a few variables
    
    Args:
        gas: List of gas amounts at each station
        cost: List of costs to travel to next station
        
    Returns:
        Starting station index, or -1 if impossible
    """
    n = len(gas)
    total_tank = 0
    current_tank = 0
    start_station = 0
    
    for i in range(n):
        # Net gain/loss at this station
        diff = gas[i] - cost[i]
        
        # Track total (determines if solution exists)
        total_tank += diff
        
        # Track current journey
        current_tank += diff
        
        # If we can't proceed, reset start to next station
        if current_tank < 0:
            start_station = i + 1
            current_tank = 0
    
    # If total tank negative, impossible
    return start_station if total_tank >= 0 else -1


def can_complete_circuit_verbose(gas, cost):
    """
    Same algorithm with detailed tracking for educational purposes.
    """
    n = len(gas)
    
    print(f"Gas:   {gas}")
    print(f"Cost:  {cost}")
    print(f"Diff:  {[gas[i] - cost[i] for i in range(n)]}")
    print(f"Total: {sum(gas) - sum(cost)}")
    print()
    
    total_tank = 0
    current_tank = 0
    start_station = 0
    
    for i in range(n):
        diff = gas[i] - cost[i]
        total_tank += diff
        current_tank += diff
        
        print(f"Station {i}: diff={diff:+3d}, current_tank={current_tank:+3d}, ", end="")
        
        if current_tank < 0:
            print(f"FAILED! Reset start to {i+1}")
            start_station = i + 1
            current_tank = 0
        else:
            print(f"OK (start={start_station})")
    
    print(f"\nTotal tank: {total_tank}")
    if total_tank >= 0:
        print(f"Solution: Start at station {start_station}")
        return start_station
    else:
        print("No solution possible")
        return -1


def can_complete_circuit_simulation(gas, cost, start):
    """
    Simulate journey starting from given station.
    
    Used for testing and verification.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    n = len(gas)
    tank = 0
    
    for i in range(n):
        station = (start + i) % n
        tank += gas[station] - cost[station]
        
        if tank < 0:
            return False
    
    return True


def can_complete_circuit_brute_force(gas, cost):
    """
    Brute force: try every starting position.
    
    Used to verify correctness of greedy solution.
    
    Time Complexity: O(n^2)
    Space Complexity: O(1)
    """
    n = len(gas)
    
    for start in range(n):
        if can_complete_circuit_simulation(gas, cost, start):
            return start
    
    return -1


def can_complete_circuit_alternative(gas, cost):
    """
    Alternative formulation with explicit checks.
    
    Same logic, different implementation style.
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    # Quick check: if total gas < total cost, impossible
    if sum(gas) < sum(cost):
        return -1
    
    # Find valid starting point
    start = 0
    tank = 0
    
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        
        # If tank goes negative, can't start from start..i
        if tank < 0:
            start = i + 1
            tank = 0
    
    return start


def explain_greedy_proof():
    """
    Detailed mathematical proof of correctness.
    
    THEOREM: The greedy algorithm correctly finds the unique starting station,
    or determines that no solution exists.
    
    PROOF:
    
    PART 1: If total_gas < total_cost, no solution exists.
    - To complete full circuit, need: sum(gas[i] - cost[i]) >= 0
    - This is necessary condition
    - Proof: net fuel change for full circuit = sum(gas) - sum(cost)
    
    PART 2: If total_gas >= total_cost, solution exists and is unique.
    
    LEMMA 1: If we can't reach station j from station i, then we can't reach j
    from any station k where i <= k < j.
    
    Proof of Lemma 1:
    - Let tank[k] = fuel when reaching station k from station i
    - We have tank[i] = 0 (starting point)
    - For i < k < j: tank[k] = tank[k-1] + gas[k-1] - cost[k-1]
    - Since we can travel i to k-1, we have tank[k] >= 0
    - If we start at k instead, we have tank'[k] = 0 < tank[k]
    - Therefore, tank'[j] < tank[j] < 0 (since we failed from i)
    - So starting at k also fails to reach j
    
    CONSEQUENCE: When we fail at station j starting from i, we should skip
    all stations i, i+1, ..., j-1 and try starting from j.
    
    PART 3: The greedy algorithm finds the unique starting point.
    
    Algorithm maintains:
    - start_station = candidate starting point
    - current_tank = cumulative fuel from start_station
    
    When current_tank < 0 at station i:
    - We failed to reach i from start_station
    - By Lemma 1, all stations from start_station to i are invalid
    - Set new start_station = i + 1
    
    After scanning all stations:
    - If total_tank >= 0, solution exists
    - start_station is the only unchecked starting point
    - By elimination, start_station must work
    - Why? If start_station failed, we would have reset past it
    
    UNIQUENESS:
    - Problem guarantees solution is unique if it exists
    - Our algorithm finds the unique solution by elimination
    
    TIME COMPLEXITY: O(n) - single pass
    SPACE COMPLEXITY: O(1) - constant extra space
    
    This is a beautiful example of:
    1. Greedy choice: skip entire ranges at once
    2. Proof by contradiction: if greedy fails, we get contradiction
    3. Elimination: rule out invalid starts efficiently
    """
    print(__doc__)


def test_gas_station():
    """Comprehensive test cases."""
    
    # Test case 1: Example from problem
    gas = [1, 2, 3, 4, 5]
    cost = [3, 4, 5, 1, 2]
    result = can_complete_circuit(gas, cost)
    assert result == 3
    assert can_complete_circuit_simulation(gas, cost, result)
    
    # Test case 2: Impossible
    gas = [2, 3, 4]
    cost = [3, 4, 3]
    result = can_complete_circuit(gas, cost)
    assert result == -1
    
    # Test case 3: Start at beginning
    gas = [5, 1, 2, 3, 4]
    cost = [4, 4, 1, 5, 1]
    result = can_complete_circuit(gas, cost)
    assert result == 4
    assert can_complete_circuit_simulation(gas, cost, result)
    
    # Test case 4: Single station
    gas = [5]
    cost = [4]
    result = can_complete_circuit(gas, cost)
    assert result == 0
    
    # Test case 5: Single station impossible
    gas = [3]
    cost = [4]
    result = can_complete_circuit(gas, cost)
    assert result == -1
    
    # Test case 6: All equal
    gas = [3, 3, 3]
    cost = [3, 3, 3]
    result = can_complete_circuit(gas, cost)
    assert result == 0  # Any start works, return first
    
    # Test case 7: Large positive at end
    gas = [1, 1, 1, 10]
    cost = [2, 2, 2, 1]
    result = can_complete_circuit(gas, cost)
    assert result == 3
    assert can_complete_circuit_simulation(gas, cost, result)
    
    # Test case 8: Barely possible
    gas = [2, 2, 2, 2]
    cost = [2, 2, 2, 1]
    result = can_complete_circuit(gas, cost)
    assert result >= 0
    assert can_complete_circuit_simulation(gas, cost, result)
    
    # Verify all approaches give same answer
    test_cases = [
        ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]),
        ([2, 3, 4], [3, 4, 3]),
        ([5, 1, 2, 3, 4], [4, 4, 1, 5, 1]),
    ]
    
    for gas, cost in test_cases:
        r1 = can_complete_circuit(gas, cost)
        r2 = can_complete_circuit_alternative(gas, cost)
        r3 = can_complete_circuit_brute_force(gas, cost)
        assert r1 == r2 == r3, f"Mismatch for gas={gas}, cost={cost}"
    
    print("All test cases passed!")


def visualize_circuit(gas, cost):
    """
    Visualize the circular route.
    """
    n = len(gas)
    start = can_complete_circuit(gas, cost)
    
    print(f"\nCircular Route with {n} stations:")
    print("-" * 60)
    
    if start == -1:
        print("No valid starting station!")
        print(f"Total gas: {sum(gas)}, Total cost: {sum(cost)}")
        print(f"Deficit: {sum(cost) - sum(gas)}")
        return
    
    print(f"Starting from station {start}:")
    print()
    
    tank = 0
    for i in range(n):
        station = (start + i) % n
        tank += gas[station]
        print(f"Station {station}: +{gas[station]} gas → tank = {tank}")
        tank -= cost[station]
        print(f"           Travel: -{cost[station]} gas → tank = {tank}")
        print()


if __name__ == "__main__":
    test_gas_station()
    
    print("\n" + "="*60)
    print("Example 1: Possible")
    print("="*60)
    gas = [1, 2, 3, 4, 5]
    cost = [3, 4, 5, 1, 2]
    result = can_complete_circuit_verbose(gas, cost)
    visualize_circuit(gas, cost)
    
    print("\n" + "="*60)
    print("Example 2: Impossible")
    print("="*60)
    gas = [2, 3, 4]
    cost = [3, 4, 3]
    result = can_complete_circuit_verbose(gas, cost)
    visualize_circuit(gas, cost)
    
    print("\n" + "="*60)
    print("Greedy Correctness Proof:")
    print("="*60)
    explain_greedy_proof()
