from typing import List

class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]
        while len(nums) > 1:
            val = nums[0]
            if val in nums[1:]:
                nums = [n for n in nums if n !=val]
            else:
                return val
        return nums[0]
        


if __name__ == '__main__':
    solution = Solution()

    nums = [2,2,1]
    print(solution.singleNumber(nums))
    print('1')

    nums = [4,1,2,1,2]
    print(solution.singleNumber(nums))
    print('4')


    nums = [1]
    print(solution.singleNumber(nums))
    print('1')
    
    