from typing import List


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        shortest = min(strs, key=len)
        print(shortest)


Solution().longestCommonPrefix(["flower", "flow", "flight"])
