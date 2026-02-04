class Solution:
    def climbStairs(self, n: int) -> int:
        """
        climbStairs(3) = climbStairs(2) + climbStairs(1)

        """
        ways = [0,1,2]
        if n < 3:
            return ways[n]
        for i in range(2, n):
            ways.append(ways[i] + ways[i-1])
        return ways[-1]


if __name__ == '__main__':
    solution = Solution()
    
    n = 2
    print(solution.climbStairs(n))
    print("2")

    n = 3
    print(solution.climbStairs(n))
    print("3")

    n = 10
    print(solution.climbStairs(n))
    print("89")