from typing import List

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1
        
        total = len(nums1) + len(nums2)
        mid = total // 2
        l = 0
        r = len(nums1)-1
        
        while True:
            # nums1[:i+1] and nums2[:j+1] < median
            # nums1[i+1:] and nums2[j+1:] >= median
            i = (r+l) // 2
            j = mid - (i+1) - 1 # num1[i] <= num2[j+1] and (i+1)+(j+1)==mid
            
            L1 = nums1[i] if i>=0 else -float("inf")
            R1 = nums1[i+1] if i+1<len(nums1) else float("inf")
            L2 = nums2[j] if j>=0 else -float("inf")
            R2 = nums2[j+1] if j+1>=0 and j+1<len(nums2) else float("inf")

            if L1 <= R2 and L2 <= R1:
                if total % 2==0:
                    return 1./2*(max(L1, L2) + min(R1, R2))  # len(nums1[:R1]) + len(nums2[:R2]) == (i+1) + (j+1) == mid == total / 2 (second element)
                else:
                    return min(R1, R2) # len(nums1[:R1]) + len(nums2[:R2]) == (i+1) + (j+1) == mid == (total-1) / 2
            elif L1 > R2:
                r = i - 1
            else:
                l = i + 1

print(Solution().findMedianSortedArrays([], [1, 2]))

# # inefficient (long and slow)
# import bisect
# class Solution:
#     def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
#         m = len(nums1)
#         n = len(nums2)
#         if m > n:
#             tmp = m
#             m = n
#             n = tmp
#             tmp = nums1
#             nums1 = nums2
#             nums2 = tmp
        
#         if m==0:
#             if (m+n) % 2==0:
#                 return (1./2)*(nums2[(n-1)//2]+nums2[(n-1)//2+1])
#             else:
#                 return nums2[(n-1)//2]
#         else:
#             target_rank = (m+n+1)//2
#             l = 0
#             r = m
#             while l<r:
#                 mid = (l+r)//2
#                 n_less_than_val = bisect.bisect_left(nums2, nums1[mid])
#                 if n_less_than_val + mid < target_rank:
#                     l = mid + 1
#                 else:
#                     r = mid
            
#             def get_nth_value(n):
#                 n_less_than_val = bisect.bisect_left(nums2, nums1[mid])
#                 if n_less_than_val + mid + 1 == n:
#                     return nums1[mid]
#                 else:
#                     offset = n - n_less_than_val - mid - 1
#                     if offset < 0:
#                         return sorted(nums1[max(0, mid+offset-1):mid] + nums2[max(0, n_less_than_val+offset-1):n_less_than_val])[offset]
#                     else:
#                         return sorted(nums1[mid:mid + offset + 1] + nums2[n_less_than_val:n_less_than_val+offset])[offset]
                
#             if (m+n) % 2==0:
#                 return (1./2)*(get_nth_value((m+n+1)//2) + get_nth_value((m+n+1)//2+1))
#             else:
                
#                 return get_nth_value((m+n+1)//2)
