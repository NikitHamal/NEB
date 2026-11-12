# Numerical checks for 12-econ-2080-3041
import math
assert 5000-4200 == 800
assert 35*5-(10+20+40+60) == 45
price=20; units=[1,2,3,4]; TR=[price*u for u in units]; MR=[TR[0]]+[TR[i]-TR[i-1] for i in range(1,4)]
assert TR==[20,40,60,80] and MR==[20]*4 and [t/u for t,u in zip(TR,units)]==[20]*4
tvc=[0,10,18,23,32,50,80,124,180]; tc=[100+v for v in tvc]
assert tc==[100,110,118,123,132,150,180,224,280]
assert [tc[i]-tc[i-1] for i in range(1,9)]==[10,8,5,9,18,30,44,56]
ac=[tc[i]/i for i in range(1,9)]
assert all(abs(a-b)<0.01 for a,b in zip(ac,[110,59,41,33,30,30,32,35]))
x=[45,50,55,60,65]; f=[3,5,8,7,4]; N=sum(f)
m=sum(a*b for a,b in zip(x,f))/N; var=sum(b*(a-m)**2 for a,b in zip(x,f))/N
assert N==27 and abs(m-55.74)<0.01 and abs(var-36.49)<0.01 and abs(math.sqrt(var)-6.04)<0.01
A=[(6,12,10,15),(5,10,8,10),(3,8,5,12),(8,5,7,13)]
n=sum(p1*q1 for _,_,p1,q1 in A); d=sum(p0*q1 for p0,_,_,q1 in A)
assert (n,d)==(381,280) and abs(n/d*100-136.07)<0.01
assert 10-4==2+4 and 10-0.5*4==8
print("econ 2080 checks ok")
