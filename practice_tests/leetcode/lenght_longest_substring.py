# Given a string s, find the length of the longest substring without repeating characters.


def lengthOfLongestSubstring(self, s: str) -> int:
        notrepeat = True
        i = 0
        l = []
        while(notrepeat):
            if s[i] in l:
                return i+1
            i = i + 2
            l.append(s[i])


if __name__ == '__main__':

    inputstr = str(input())
    result = lengthOfLongestSubstring(inputstr)

    return(result)
