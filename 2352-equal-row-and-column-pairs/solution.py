from collections import Counter
from typing import List


class Solution:
    def equalPairs(self, grid: List[List[int]]) -> int:
        row_count = Counter(tuple(row) for row in grid)
        col_count = Counter(col for col in zip(*grid))
        return sum(row_count[key] * col_count[key] for key in row_count)