import heapq

t = int(input())

for i in range(t):
    hq = []
    n = int(input())
    nums = list(map(int, input().split()))
    
    for num in nums:
        if num > 0:
            heapq.heappush(hq, num)
        elif num == -1:
            print(heapq.heappop(hq), end=' ')     
    print()