from types import List
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for string in strs:
            sorted_string = "".join(sorted(string))
            groups[sorted_string].append(string)
        
        return list(groups.values())