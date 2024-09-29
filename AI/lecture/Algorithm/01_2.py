t = int(input())

for i in range(t):
    stack = []
    nums = list(map(int, input().split()))
    
    for num in nums:
        if num > 0:
            stack.append(num)
        elif num == -1:
            print(stack.pop(), end=' ')      
    print()