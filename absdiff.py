#code

t=int(input())
for i in range(t):
    s1=0
    s2=0
    a=[]
    n=int(input())
    s=input()
    b=s.split(" ")
    for j in range(n):
        b[j]=int(b[j])
        a.append(b[j])
    for k in range(n):
        if k%2==0:
            b[k]=1
    for h in range(n-1):
        x=b[h]-b[h+1]
        if x<0:
            x*=-1
        s1+=x
    for l in range(n):
        if l%2!=0:
            a[l]=1
    for q in range(n-1):
        z=a[q]-a[q+1]
        if z<0:
            z*=-1
        s2+=z
        
    if s1>s2:
        print(s1)
    else:
        print(s2)
