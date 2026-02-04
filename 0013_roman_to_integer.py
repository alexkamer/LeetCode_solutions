class Solution:
    def romanToInt(self, s: str) -> int:
        num_map = {
            'I' : 1,
            'V' : 5,
            'X' : 10,
            'L' : 50,
            'C' : 100,
            'D' : 500,
            'M' : 1000,
            'IV' : 4,
            'IX' : 9,
            'XL' : 40,
            'XC' : 90,
            'CD' : 400,
            'CM' : 900,
        }

        start, end = 0, len(s)-1
        res = 0
        while start < end:
            num1 = s[start]
            if num1 not in ['I', 'X', 'C']:
                increase_by = num_map[s[start]]

                start +=1
            else:
                res_num = s[start]
                num2 = s[start+1]
                if num1 == 'I' and num2 in ['V','X']:
                    res_num = num1 + num2
                elif num1 == 'X' and num2 in ['L', 'C']:
                    res_num = num1 + num2
                elif num1 == 'C' and num2 in ['D', 'M']:
                    res_num = num1 + num2

                # print(res_num)
                increase_by = num_map[res_num]

                start += len(res_num)
            res += increase_by
        if start == end:
            res += num_map[s[-1]]
        return res


                

                    







if __name__ == '__main__':
    solution = Solution()


    s = "III"
    print(solution.romanToInt(s))
    print("Expected 3")

    s = "LVIII"
    print(solution.romanToInt(s))
    print("Expected 58")

    s = "MCMXCIV"
    print(solution.romanToInt(s))
    print("Expected 1994")
