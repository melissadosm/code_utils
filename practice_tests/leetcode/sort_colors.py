# Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.
# We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.

def sortColors(nums) -> None:
    """
    Do not return anything, modify nums in-place instead.
    """
    return sorted(nums)



if __name__ == '__main__':

    inputstr = [2,0,2,1,1,0]
    result = sortColors(inputstr)

    print(result)
