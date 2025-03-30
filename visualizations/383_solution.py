from collections import Counter


class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:

        if len(ransomNote) > len(magazine):
            return False

        magazine_counts = Counter(magazine)

        for letter in ransomNote:
            if not magazine_counts[letter]:
                return False
            magazine_counts[letter] -= 1

        return True
