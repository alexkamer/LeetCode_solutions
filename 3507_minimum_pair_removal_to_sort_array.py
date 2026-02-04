from typing import List

class Solution:
    def minimumPairRemoval(self, nums: List[int]) -> int:
        res = 0
        isSorted = False
        fin_list = nums
        if nums == sorted(nums):
            isSorted = True
        while not isSorted:
            min_pair = [max(fin_list),max(fin_list)]
            merge_indexes = []


            for i in range(0, len(fin_list)-1):
                if sum([fin_list[i], fin_list[i+1]]) < sum(min_pair):
                    min_pair = [fin_list[i], fin_list[i+1]]
                    merge_indexes = [i, i+1]
            
            # print(merge_indexes)

            if len(merge_indexes) > 0:

                fin_list[merge_indexes[0] : merge_indexes[1]+1] = [sum(min_pair)]
                res += 1
            
            else:
                # print("EXITING VIA ELSE BRANCH")
                return res+1


            if fin_list == sorted(fin_list):
                isSorted = True

        # print("EXITING VIA SORTED CHECK")
        return res




if __name__ == '__main__':
    solution = Solution()

    nums = [5,2,3,1]
    print(solution.minimumPairRemoval(nums))
    print("Expected 2")

    nums = [350,-113,-406,764,-511,90,-372,-411,628,822,-923,-146,686,-631,-138,157,-839,302,695,-436,791,-920,-106,802,32,483,349,346,847,704,-128,-495,340,-316,-189,585,-276]
    print(solution.minimumPairRemoval(nums))
    print('Expected 36')

    nums = [564,561,543,576,-379,510,54,383,-615,468,431,601,412,-397,421,183,160,415]
    print(solution.minimumPairRemoval(nums))
    print('Expected 17')