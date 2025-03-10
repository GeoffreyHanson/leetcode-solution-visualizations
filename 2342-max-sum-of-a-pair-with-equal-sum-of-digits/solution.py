from collections import defaultdict
from typing import List


class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        def get_digit_sum(num):
            return sum(int(digit) for digit in str(num))

        sums = defaultdict(int)
        max_sum = -1
        for num in nums:
            digit_sum = get_digit_sum(num)

            if digit_sum in sums:
                cur_sum = sums[digit_sum] + num
                max_sum = max(max_sum, cur_sum)

            sums[digit_sum] = max(sums[digit_sum], num)

        return max_sum
