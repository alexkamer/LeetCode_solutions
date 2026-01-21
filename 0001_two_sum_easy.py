from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        One-pass hash table approach:
        - For each number, check if its complement (target - num) exists in hash map
        - If yes, return the indices
        - If no, store current number and index in hash map

        Time Complexity: O(n) - single pass through array
        Space Complexity: O(n) - hash map storage
        """
        hash_map = {}
        for i in range(len(nums)):
            complement = target - nums[i]
            if complement in hash_map:
                return [hash_map[complement], i]
            hash_map[nums[i]] = i

if __name__ == "__main__":
      solution = Solution()

      # Test case 1
      nums1 = [2, 7, 11, 15]
      target1 = 9
      print(f"Input: nums = {nums1}, target = {target1}")
      print(f"Output: {solution.twoSum(nums1, target1)}")
      print(f"Expected: [0, 1]\n")

      # Test case 2
      nums2 = [3, 2, 4]
      target2 = 6
      print(f"Input: nums = {nums2}, target = {target2}")
      print(f"Output: {solution.twoSum(nums2, target2)}")
      print(f"Expected: [1, 2]\n")

      # Test case 3
      nums3 = [3, 3]
      target3 = 6
      print(f"Input: nums = {nums3}, target = {target3}")
      print(f"Output: {solution.twoSum(nums3, target3)}")
      print(f"Expected: [0, 1]\n")

