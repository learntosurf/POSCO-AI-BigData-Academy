import sys
sys.setrecursionlimit(1000000)

def dfs(x):
    visited[x] = True
    print(x, end=' ')
    for i in sorted(graph[x]):
        if not visited[i]:
            dfs(i) 
            
t = int(input())

for i in range(t):
    N, M = map(int, input().split())
    
    graph = [[] for _ in range(N)]
    
    for j in range(M):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
        
    visited = [False] * N
    dfs(0)
    print()