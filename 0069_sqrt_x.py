class Solution:
    def mySqrt(self, x: int) -> int:
        if x < 2:
            return x

        left, right = 0, x

        while left <= right:
            mid = (left + right) // 2
            squared = mid * mid

            if squared == x:
                return mid
            elif squared < x:
                left = mid + 1
            else:
                right = mid - 1

        # When loop exits, right will be the floor of sqrt(x)
        return right


if __name__ == '__main__':
    solution = Solution()

    x = 4
    print(solution.mySqrt(x))
    print("Expected: 2")
    print()

    x = 8
    print(solution.mySqrt(x))
    print("Expected: 2")
    print()

    x = 0
    print(solution.mySqrt(x))
    print("Expected: 0")
    print()

    x = 1
    print(solution.mySqrt(x))
    print("Expected: 1")
    print()

    x = 2147395599
    print(solution.mySqrt(x))
    print("Expected: 46339")
    print()

    x = 2147483647
    print(solution.mySqrt(x))
    print("Expected: 46340")
