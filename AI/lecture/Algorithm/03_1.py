t = int(input())

for i in range(t):
    N, M = map(int, input().split())
    graph = [[0 for _ in range(N)] for _ in range(N)]
    
    for j in range(M):
        u, v, c = map(int, input().split())
        graph[u][v] = c
    
    for row in graph:
        print(' '.join(map(str, row)))
