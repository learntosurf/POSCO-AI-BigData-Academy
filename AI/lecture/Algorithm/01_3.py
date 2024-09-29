import collections 
from collections import deque

t = int(input())

for i in range(t):
    queue = collections.deque()
    nums = list(map(int, input().split()))
    
    for num in nums:
        if num > 0:
            queue.append(num)
        elif num == -1:
            print(queue.popleft(), end=' ')        
    print()

