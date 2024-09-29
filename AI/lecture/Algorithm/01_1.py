t = int(input())
answer = []

for i in range(t):
    A, B = map(int, input().split())
    answer.append(A + B)

print('\n'.join(map(str, answer)))