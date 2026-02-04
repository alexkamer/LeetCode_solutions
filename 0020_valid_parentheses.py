class Solution:
    def isValid(self, s: str) -> bool:
        opening_brackets = ['(' , '[', '{']
        closing_brackets = [')', ']', '}']

        match_brackets = {
            '}' : '{',
            ')' : '(',
            ']' : '['
        }
        opened_brackets = []

        for char in s:
            if char in opening_brackets:
                opened_brackets.append(char)
            else:
                if len(opened_brackets) == 0:
                    return False
                elif match_brackets[char] != opened_brackets[-1]:
                    return False
                else:
                    opened_brackets = opened_brackets[:-1]
        if len(opened_brackets) > 0:
            return False
        return True








if __name__ == '__main__':
    solution = Solution()


    s = "()"
    print(solution.isValid(s))
    print("Expected true")


    s = "()[]{}"
    print(solution.isValid(s))
    print("Expected true")

    s = "(]"
    print(solution.isValid(s))
    print("Expected false")


    s = "([])"
    print(solution.isValid(s))
    print("Expected true")

    s = "([)]"
    print(solution.isValid(s))
    print("Expected false")



