from typing import List

class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        window = set()

        for i in range(len(nums)):
            if nums[i] in window:
                return True

            window.add(nums[i])

            if len(window) > k:
                window.remove(nums[i - k])

        return False



if __name__ == '__main__':
    solution = Solution()


    nums = [1,2,3,1]
    k = 3

    print(solution.containsNearbyDuplicate(nums,k))
    print(True)


    nums = [1,0,1,1]
    k = 1

    print(solution.containsNearbyDuplicate(nums,k))
    print(True)

    nums = [1,2,3,1,2,3]
    k = 2

    print(solution.containsNearbyDuplicate(nums,k))
    print(False)

    nums = [99,99]
    k = 2
    print(solution.containsNearbyDuplicate(nums,k))
    print(True)