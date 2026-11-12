# Numerical checks for 12-bmath-2080-908
from fractions import Fraction as F
import sympy as sp, math, itertools
x,t,Q,h=sp.symbols('x t Q h')
assert sp.solve_univariate_inequality(abs(2*x-5)<=3,x,relational=False)==sp.Interval(1,4)
assert 16/2*(2*500+15*500)==68000
r=F(243,32)**F(1,5) if False else F(3,2); assert F(2,3)*r**5==F(81,16) and [F(2,3)*r**k for k in (1,2,3,4)]==[1,F(3,2),F(9,4),F(27,8)]
assert math.perm(6,3)==120
A=sp.Matrix([[-3,-2],[5,3]]); B=sp.Matrix([[3,2],[-5,3]]); assert (A*B).det()==19 and A.det()==1 and B.det()==19
assert (2*2-3,2*3-4)==(1,2)
assert abs(3.678**4/42.75**(1/3)-52.336)<0.01 and abs(10**(4*0.5656-0.5436333)-52.34)<0.1
assert sp.limit((x**3-27)/(x**2-5*x+6),x,3)==27 and sp.limit((x**2-16)/(x-4),x,4)==8
assert sp.simplify(sp.diff(sp.Symbol('a')*(t**2+7),t)/sp.diff(2*sp.Symbol('a')*(t+3),t)-t)==0
assert sp.simplify(sp.integrate((x**2-4)/(x+2),x)-(x**2/2-2*x))==0
R=sp.integrate(10+20*x-3*x**2,x)+148; assert R.subs(x,2)==200
d=[158,166,164,160,172,170]; m=sum(d)/6; assert m==165 and math.sqrt(sum((v-m)**2 for v in d)/6)==5
assert abs(0.40+0.75-0.61-0.54)<1e-9
assert F(30*12)/F(5,7)*F(2,7)/4-30==6
assert F(8280,90)==92 and 100*72*F(115,100)==8280
a=sp.symbols('a'); assert sp.expand(sp.Matrix([[1+a,1,1],[1,1+a,1],[1,1,1+a]]).det()-a**2*(a+3))==0
f=1/(1+x); assert sp.simplify(sp.limit((f.subs(x,x+h)-f)/h,h,0)+1/(1+x)**2)==0
assert 3*F(3,8)-4*F(3,8)**2==F(9,16)
pts=[(0,6),(2,8),(2,0)]; assert all(-p[0]+p[1]<=6 and 3*p[0]+p[1]>=6 and p[0]<=2 for p in pts) and max(8*p[0]+3*p[1] for p in pts)==40
# brute force the LP on a grid
best=max(8*i/10+3*j/10 for i in range(-50,21) for j in range(-100,200) if -i/10+j/10<=6 and 3*i/10+j/10>=6 and i/10<=2); assert abs(best-40)<0.01
X=[10,15,20,25,30]; f_=[5,4,4,4,3]; mean=sum(a*b for a,b in zip(X,f_))/sum(f_); assert mean==19
assert sum(b*abs(a-mean) for a,b in zip(X,f_))/20==6.1
assert F(7000*12)+0==84000 and F(6000*8)==48000 and F(8000*6)==48000 and F(7,15)*15000==7000 and F(4,15)*15000==4000
assert abs(2700*0.05*(1/3)-45)<0.01 and 2700-2655==45
assert abs(273*100/(3640*3)-2.5)<1e-9 and abs(3640*(1.025**3-1)-279.88)<0.01
assert abs(700*((1.05**4-1)/0.05)-3017.09)<0.01 and abs(500*134.40-67200)<0.01
assert abs(75/90*89.10/60-1.2375)<1e-9 and abs(56/25-2.24)<1e-9
print('bmath 2080 908 checks OK')
