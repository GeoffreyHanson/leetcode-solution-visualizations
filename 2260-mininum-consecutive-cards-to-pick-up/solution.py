from collections import defaultdict
from typing import List


class Solution:
    def minimumCardPickup(self, cards: List[int]) -> int:
        seen = defaultdict(int)
        min_draws = float("inf")

        for i, card in enumerate(cards):
            if card in seen:
                draws = i - seen[card] + 1
                min_draws = min(min_draws, draws)

            seen[card] = i

        return min_draws if min_draws < float("inf") else -1
