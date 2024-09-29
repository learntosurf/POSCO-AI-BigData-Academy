t = int(input())

for i in range(t):
    N, M = map(int, input().split())
    graph = [[] for _ in range(N)]
    
    for j in range(M):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
    
    for row in graph:
        row.sort()
        print(' '.join(map(str, row)))       