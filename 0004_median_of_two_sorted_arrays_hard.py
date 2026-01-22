class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        all_nums = sorted(nums1 + nums2)
        middle = len(all_nums)/2
        middle = int(middle)

        if len(all_nums) % 2 != 0:
            return all_nums[middle]
        else:
            return (all_nums[middle] + all_nums[middle-1])/2





if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    nums1 = [1,3]
    nums2 = [2]
    print(solution.findMedianSortedArrays(nums1,nums2))
    print("Expected 2")


    # Test case 2
    nums1 = [1,2]
    nums2 = [3,4]
    print(solution.findMedianSortedArrays(nums1,nums2))
    print("Expected 2.5")

