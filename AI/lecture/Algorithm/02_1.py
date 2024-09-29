def Fibo(n): 
    # if n==1 or n==2:
    #     return 1
    # elif n==0:
    #     return 0
    if n <= 2:
        return 1
    else:
        return Fibo(n-1) + Fibo(n-2)

t = int(input())
answer = []

for i in range(t):
    n = int(input())
    answer.append(Fibo(n))

print('\n'.join(map(str, answer)))