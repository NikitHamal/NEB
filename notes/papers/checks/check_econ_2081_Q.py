# Numerical checks for 12-econ-2081-3041q
from fractions import Fraction as F
# Q2 profit = TR - TC
import sympy as sp
Q=sp.symbols('Q')
assert sp.expand((5*Q**2-4*Q+10)-(4*Q**2-6*Q+20))==Q**2+2*Q-10
# Q11 median from empirical relation mode = 3 median - 2 mean
assert F(25+2*22,3)==23
# Q14
P=[35,30,25,20]; TR=[p*(i+1) for i,p in enumerate(P)]; AR=P; MR=[TR[0]]+[TR[i]-TR[i-1] for i in range(1,4)]
assert TR==[35,60,75,80] and MR==[35,25,15,5]
# Q15
q=sp.symbols('q'); tc=100+12*q**2; tr=(200-8*q)*q
mr=sp.diff(tr,q); mc=sp.diff(tc,q); sol=sp.solve(sp.Eq(mr,mc),q)[0]
assert sol==5 and 200-8*sol==160 and (tr-tc).subs(q,sol)==400
assert sp.diff(mc,q)>sp.diff(mr,q)
# Q19
assert F(13*100,40)==F(65,2) and F(14*100,50)==28
# Q19 Or Paasche
p0=[8,9,7,6]; q0=[20,18,15,22]; p1=[10,12,11,9]; q1=[25,20,12,30]
n=sum(a*b for a,b in zip(p1,q1)); d=sum(a*b for a,b in zip(p0,q1))
assert (n,d)==(892,644) and round(n/d*100,2)==138.51
# Q20
TVC=[0,10,16,20,26,35,55,90,150]; TC=[50+v for v in TVC]
assert TC==[50,60,66,70,76,85,105,140,200]
AC=[round(TC[i]/i,2) for i in range(1,9)]; MC=[TC[i]-TC[i-1] for i in range(1,9)]
assert AC==[60,33,23.33,19,17,17.5,20,25] and MC==[10,6,4,6,9,20,35,60]
print('all econ 2081 checks pass')
