from typing import List
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        merged_digits = int(''.join([str(x) for x in digits])) + 1
        return [int(x) for x in str(merged_digits)]
        


if __name__ == '__main__':
    solution = Solution()

    digits = [1,2,3]

    print(solution.plusOne(digits))
    print("Expected [1,2,4]")

    digits = [4,3,2,1]

    print(solution.plusOne(digits))
    print("Expected [4,3,2,2]")

    digits = [9]

    print(solution.plusOne(digits))
    print("Expected [1,0]")