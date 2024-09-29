def binary(data, left, right, q):
    if left > right:
        return -1
    mid = (left + right) // 2
    if data[mid] == q:
        return mid
    elif data[mid] > q:
        return binary(data, left, mid-1, q)
    else:
        return binary(data, mid+1, right, q)
    
t = int(input())

for i in range(t):
    data = list(map(int, input().split()))
    query = list(map(int, input().split()))
    answer = []
    
    for q in query:
        answer.append(binary(data, 0, len(data)-1, q))
    
    print(' '.join(map(str, answer))) 