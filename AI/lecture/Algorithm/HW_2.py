from collections import deque

def bfs(start):
    queue = deque([start])
    visited[start] = True
    # print(f"Initial queue: {queue}")
    
    while queue:
        x = queue.popleft() 
        # print(f"Popped {x} from queue. Current queue: {queue}")
        print(x, end=' ')
        
        for i in sorted(graph[x]):
            if not visited[i]:
                queue.append(i)
                visited[i] = True
                # print(f"Visited {i}, added to queue. Queue is now: {queue}")

t = int(input())  
    
for i in range(t):
    N, M = map(int, input().split())
    
    graph = [[] for _ in range(N)]
    
    for j in range(M):
        # print(f"Processing case {i+1}")
        u, v = map(int, input().split())
        graph[u].append(v)
        
    # print(f"Graph for case {i+1}: {graph}")
    visited = [False] * N
    bfs(0)
    print()
