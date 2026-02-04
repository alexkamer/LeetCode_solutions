class Solution:
    def isHappy(self, n: int) -> bool:
        if n == 1:
            return True
        str_n = str(n)
        str_n = [x for x in str_n]

        end = 0

        all_nums = [str_n]

        while end != 1:
            end = sum([int(x)**2 for x in str_n])
            str_n = [x for x in str(end)]
            if str_n in all_nums:
                return False
            all_nums.append(str_n)

        return True