def merge_list(n, m):
    answer = []
    i, j = 0, 0
    while i < len(n) and j < len(m):
        if n[i] < m[j]:
            answer.append('1')
            i += 1
        else:
            answer.append('2')
            j += 1

    if i < len(n):
        answer += ['1'] * (len(n) - i)
    if j < len(m):
        answer += ['2'] * (len(m) - j)

    return ' '.join(answer)


t = int(input())

for _ in range(t):
    n = list(map(int, input().split()))
    m = list(map(int, input().split()))
    
    result = merge_list(n, m)
    print(result)
